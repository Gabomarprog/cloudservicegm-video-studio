#!/usr/bin/env python3
"""Original Spanish male voice design using the CPU-optimised Qwen3-TTS C engine."""
from __future__ import annotations
import argparse, re, subprocess, sys, tempfile, wave
from pathlib import Path

VOICE_INSTRUCTION = (
    "Voz masculina adulta, español latinoamericano neutro y natural, sin un acento "
    "regional demasiado marcado. Timbre medio-grave, cálido, aterciopelado, suave y "
    "elegante, con resonancia natural y cercanía de micrófono. Habla con serenidad y "
    "seguridad, como alguien experto que explica algo interesante a una persona. "
    "Ritmo conversacional moderado, ligeramente pausado, con respiraciones discretas "
    "y pausas orgánicas entre ideas. Entonación expresiva pero contenida; subraya las "
    "palabras importantes con sutileza, sin sobreactuar. Articulación clara, vocales "
    "suaves y finales de frase relajados. No uses voz de locutor comercial, no suenes "
    "robótico, no exageres los graves ni la emoción. Debe resultar humana, íntima, "
    "cálida, cautivadora y agradable de escuchar durante todo el video."
)

def split_script(text: str, max_chars: int = 360) -> list[tuple[str, bool]]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()] or [text.strip()]
    result = []
    for paragraph in paragraphs:
        sentences = [s.strip() for s in re.split(r"(?<=[.!?…])\s+", paragraph) if s.strip()]
        current, size = [], 0
        for sentence in sentences:
            pieces = [p.strip() for p in re.split(r"(?<=,)\s+", sentence) if p.strip()] or [sentence]
            expanded = []
            for piece in pieces:
                if len(piece) <= max_chars:
                    expanded.append(piece)
                    continue
                words, running = piece.split(), []
                for word in words:
                    candidate = " ".join(running + [word])
                    if running and len(candidate) > max_chars:
                        expanded.append(" ".join(running))
                        running = [word]
                    else:
                        running.append(word)
                if running:
                    expanded.append(" ".join(running))
            for piece in expanded:
                if current and size + len(piece) + 1 > max_chars:
                    result.append((" ".join(current), False))
                    current, size = [], 0
                current.append(piece)
                size += len(piece) + 1
        if current:
            result.append((" ".join(current), True))
    return result

def pause_seconds(chunk: str, paragraph_end: bool) -> float:
    if paragraph_end: return 0.42
    if chunk.rstrip().endswith(("?", "!")): return 0.34
    if chunk.rstrip().endswith((".", "…")): return 0.28
    if chunk.rstrip().endswith((";", ":")): return 0.20
    return 0.16

def run_engine(engine, model_dir, text, output, seed, threads):
    command = [
        str(engine), "-d", str(model_dir), "--voice-design", "-l", "Spanish",
        "--instruct", VOICE_INSTRUCTION, "--text", text, "-o", str(output),
        "--seed", str(seed), "--temperature", "0.42", "--int8", "-j", str(threads)
    ]
    subprocess.run(command, check=True)
    if not output.exists() or output.stat().st_size < 1024:
        raise RuntimeError(f"Qwen3-TTS no generó un WAV válido: {output}")

def concatenate_wavs(parts, output):
    params, total_frames = None, 0
    with wave.open(str(output), "wb") as target:
        for path in parts:
            with wave.open(str(path), "rb") as source:
                current = source.getparams()
                if current.sampwidth != 2 or current.nchannels != 1:
                    raise RuntimeError(f"Formato WAV inesperado en {path}: {current}")
                if params is None:
                    params = current
                    target.setnchannels(current.nchannels)
                    target.setsampwidth(current.sampwidth)
                    target.setframerate(current.framerate)
                elif (current.framerate != params.framerate or
                      current.nchannels != params.nchannels or
                      current.sampwidth != params.sampwidth):
                    raise RuntimeError("Los segmentos de voz tienen formatos diferentes")
                frames = source.getnframes()
                target.writeframesraw(source.readframes(frames))
                total_frames += frames
    if params is None:
        raise RuntimeError("No hay segmentos de voz para combinar")
    return params.framerate, total_frames / params.framerate

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--engine", default="tools/qwen3-tts/qwen_tts")
    parser.add_argument("--model", default="models/qwen3-tts-voice-design")
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--seed", type=int, default=20261110)
    args = parser.parse_args()

    input_path, output_path = Path(args.input), Path(args.output)
    engine, model_dir = Path(args.engine), Path(args.model)
    if not input_path.exists(): raise FileNotFoundError(f"No existe el guion: {input_path}")
    if not engine.exists(): raise FileNotFoundError(f"No se encuentra el motor Qwen3-TTS: {engine}")
    if not (model_dir / "config.json").exists():
        raise FileNotFoundError(f"No se encuentra el modelo VoiceDesign: {model_dir}")

    chunks = split_script(input_path.read_text(encoding="utf-8").strip())
    if not chunks: raise RuntimeError("El guion está vacío o no contiene texto utilizable")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="cloudservicegm-voice-") as temp_dir:
        temp = Path(temp_dir)
        rendered = []
        for index, (chunk, paragraph_end) in enumerate(chunks):
            chunk_path = temp / f"voice-{index:03d}.wav"
            print(f"Generando voz Qwen3-TTS {index+1}/{len(chunks)} ({len(chunk.split())} palabras)…", flush=True)
            run_engine(engine, model_dir, chunk, chunk_path, args.seed, max(1, min(args.threads, 4)))
            rendered.append(chunk_path)
            pause = pause_seconds(chunk, paragraph_end)
            if pause:
                with wave.open(str(chunk_path), "rb") as source:
                    params = source.getparams()
                silence_path = temp / f"pause-{index:03d}.wav"
                with wave.open(str(silence_path), "wb") as silence:
                    silence.setnchannels(params.nchannels)
                    silence.setsampwidth(params.sampwidth)
                    silence.setframerate(params.framerate)
                    silence.writeframes(b"\x00\x00" * int(round(pause * params.framerate)))
                rendered.append(silence_path)

        raw_path = temp / "narration-designed.wav"
        sample_rate, duration = concatenate_wavs(rendered, raw_path)
        audio_filter = (
            "highpass=f=65,"
            "equalizer=f=165:t=q:w=0.9:g=0.8,"
            "equalizer=f=2900:t=q:w=1.0:g=0.6,"
            "acompressor=threshold=-22dB:ratio=1.45:attack=20:release=190:makeup=1.2,"
            "loudnorm=I=-16:TP=-1.5:LRA=7"
        )
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error", "-i", str(raw_path),
            "-af", audio_filter, "-ar", "48000", "-ac", "2",
            "-c:a", "pcm_s16le", str(output_path)
        ], check=True)

    print(
        f"Voz original Qwen3-TTS generada: {duration:.2f}s | {len(chunks)} bloques | "
        "24 kHz origen → 48 kHz final | español latinoamericano neutro",
        flush=True
    )
    return 0

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR al generar la voz Qwen3-TTS: {exc}", file=sys.stderr)
        raise
