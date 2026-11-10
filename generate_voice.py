#!/usr/bin/env python3
"""
Generate the cloudservicegm narration with an original designed Spanish voice.

Model: Qwen3-TTS-12Hz-1.7B-VoiceDesign (Apache-2.0).
The voice is designed from a written description; no reference-person voice is cloned.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
import torch
from qwen_tts import Qwen3TTSModel


MODEL_ID = "Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign"

VOICE_INSTRUCTION = (
    "Voz masculina adulta, español latinoamericano neutro, sin regionalismos marcados. "
    "Timbre medio-grave, cálido, aterciopelado y cercano, con resonancia natural y "
    "sonido elegante. Habla con serenidad y seguridad, como una persona experta que "
    "explica algo interesante a alguien de confianza. Ritmo moderado, ligeramente "
    "pausado, con respiración discreta y pausas orgánicas entre ideas. Entonación "
    "conversacional expresiva pero contenida; destaca las palabras importantes sin "
    "sobreactuar. Articulación clara, vocales suaves y finales de frase relajados. "
    "No uses tono de locutor publicitario, no suenes robótico, no exageres los graves "
    "ni la emoción. Mantén una presencia humana, íntima, cálida y agradable de escuchar."
)


def split_script(text: str, max_chars: int = 260) -> list[tuple[str, bool, str]]:
    """Group complete sentences into manageable chunks and preserve paragraph ends."""
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paragraphs:
        paragraphs = [text.strip()]

    chunks: list[tuple[str, bool, str]] = []
    for paragraph in paragraphs:
        sentences = [
            item.strip()
            for item in re.split(r"(?<=[.!?])\s+", paragraph)
            if item.strip()
        ]
        if not sentences:
            continue

        current: list[str] = []
        current_chars = 0
        for sentence in sentences:
            if len(sentence) > max_chars:
                # Split unusually long sentences on commas, then on word boundaries.
                parts = [
                    part.strip()
                    for part in re.split(r"(?<=,)\s+", sentence)
                    if part.strip()
                ]
                if len(parts) == 1:
                    words = sentence.split()
                    parts, piece = [], []
                    for word in words:
                        candidate = " ".join(piece + [word])
                        if piece and len(candidate) > max_chars:
                            parts.append(" ".join(piece))
                            piece = [word]
                        else:
                            piece.append(word)
                    if piece:
                        parts.append(" ".join(piece))
                for part in parts:
                    if current and current_chars + len(part) + 1 > max_chars:
                        joined = " ".join(current)
                        chunks.append((joined, False, joined[-1:] if joined else ""))
                        current, current_chars = [], 0
                    current.append(part)
                    current_chars += len(part) + 1
                continue

            if current and current_chars + len(sentence) + 1 > max_chars:
                joined = " ".join(current)
                chunks.append((joined, False, joined[-1:] if joined else ""))
                current, current_chars = [], 0
            current.append(sentence)
            current_chars += len(sentence) + 1

        if current:
            joined = " ".join(current)
            chunks.append((joined, True, joined[-1:] if joined else ""))

    return chunks


def pause_after(punctuation: str, paragraph_end: bool) -> float:
    if paragraph_end:
        return 0.42
    if punctuation in ("?", "!"):
        return 0.34
    if punctuation in (".", "…"):
        return 0.27
    if punctuation in (",", ";", ":"):
        return 0.16
    return 0.20


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    if not input_path.exists():
        raise FileNotFoundError(f"No existe el guion: {input_path}")

    script = input_path.read_text(encoding="utf-8").strip()
    chunks = split_script(script)
    if not chunks:
        raise RuntimeError("El guion está vacío o no contiene texto utilizable")

    # The public GitHub runner has 4 CPU cores; do not oversubscribe it.
    torch.set_num_threads(4)
    try:
        torch.set_num_interop_threads(2)
    except RuntimeError:
        pass
    torch.manual_seed(20261110)

    print(f"Cargando {MODEL_ID} en CPU…", flush=True)
    model = Qwen3TTSModel.from_pretrained(
        MODEL_ID,
        device_map="cpu",
        dtype=torch.float32,
    )

    audio_parts: list[np.ndarray] = []
    sample_rate: int | None = None
    for index, (chunk, paragraph_end, punctuation) in enumerate(chunks):
        # A fixed seed keeps the same designed voice character between segments/runs.
        torch.manual_seed(20261110 + index)
        print(
            f"Generando bloque {index + 1}/{len(chunks)} "
            f"({len(chunk.split())} palabras)…",
            flush=True,
        )
        with torch.inference_mode():
            waveforms, rate = model.generate_voice_design(
                text=chunk,
                language="Spanish",
                instruct=VOICE_INSTRUCTION,
                max_new_tokens=1800,
            )

        if not waveforms:
            raise RuntimeError(f"Qwen3-TTS no devolvió audio para el bloque {index + 1}")
        waveform = np.asarray(waveforms[0], dtype=np.float32).reshape(-1)
        if waveform.size == 0:
            raise RuntimeError(f"El bloque {index + 1} produjo audio vacío")
        if sample_rate is None:
            sample_rate = int(rate)
        elif int(rate) != sample_rate:
            raise RuntimeError("Qwen3-TTS devolvió frecuencias de muestreo inconsistentes")

        audio_parts.append(waveform)
        pause_frames = int(round(pause_after(punctuation, paragraph_end) * sample_rate))
        if pause_frames:
            audio_parts.append(np.zeros(pause_frames, dtype=np.float32))

    assert sample_rate is not None
    raw = np.concatenate(audio_parts)
    raw_path = output_path.with_name("narration_qwen_raw.wav")
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(str(raw_path), raw, sample_rate, subtype="PCM_16")

    # Gentle studio finishing: warmth and presence, light compression, consistent
    # online loudness. No artificial pitch shifting or aggressive processing.
    audio_filter = (
        "highpass=f=65,"
        "equalizer=f=170:t=q:w=0.9:g=0.8,"
        "equalizer=f=3000:t=q:w=1.0:g=0.7,"
        "acompressor=threshold=-22dB:ratio=1.55:attack=18:release=180:makeup=1.5,"
        "loudnorm=I=-16:TP=-1.5:LRA=7"
    )
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", str(raw_path),
            "-af", audio_filter,
            "-ar", "48000", "-ac", "2",
            "-c:a", "pcm_s16le",
            str(output_path),
        ],
        check=True,
    )
    raw_path.unlink(missing_ok=True)

    duration = len(raw) / sample_rate
    print(
        f"Voz diseñada generada: {duration:.2f}s | "
        f"{len(chunks)} bloques | español latinoamericano neutro | CPU",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR al generar la voz Qwen3-TTS: {exc}", file=sys.stderr)
        raise
