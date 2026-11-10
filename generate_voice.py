#!/usr/bin/env python3
"""Generate warm, conversational Latin-American Spanish narration with Qwen3-TTS Ryan."""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


DELIVERY_INSTRUCTION = (
    "Speak in neutral Latin American Spanish with a warm, intimate, mature male delivery. "
    "Sound relaxed, sincere, engaging and memorable, like a trusted storyteller speaking "
    "directly to one person. Keep a smooth, connected conversational rhythm, with natural "
    "breathing pauses between complete thoughts and a slightly longer pause after the opening "
    "hook. Use subtle emotional emphasis and gentle intonation changes without exaggerating. "
    "Keep the voice steady and full, never thin, rushed, robotic, word-by-word, or like a loud "
    "commercial announcer. Preserve clear Latin American pronunciation throughout."
)


def prepare_continuous_text(raw: str) -> str:
    """Preserve one continuous take while turning paragraph breaks into intentional pauses."""
    paragraphs = [
        re.sub(r"\\s+", " ", part).strip()
        for part in re.split(r"\\n\\s*\\n", raw.strip())
        if part.strip()
    ]
    if not paragraphs:
        raise RuntimeError("El guion está vacío o no contiene texto utilizable")
    return " [pause:280ms] ".join(paragraphs)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--engine", default="tools/qwen3-tts/qwen_tts")
    parser.add_argument("--model", default="models/qwen3-tts-customvoice")
    parser.add_argument("--speaker", default="ryan")
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--seed", type=int, default=20261110)
    parser.add_argument("--rate", type=float, default=1.0)
    args = parser.parse_args()

    input_path, output_path = Path(args.input), Path(args.output)
    engine, model_dir = Path(args.engine), Path(args.model)
    if not input_path.exists():
        raise FileNotFoundError(f"No existe el guion: {input_path}")
    if not engine.exists():
        raise FileNotFoundError(f"No se encuentra el motor Qwen3-TTS: {engine}")
    if not (model_dir / "config.json").exists():
        raise FileNotFoundError(f"No se encuentra el modelo CustomVoice: {model_dir}")
    if not 0.9 <= args.rate <= 1.1:
        raise ValueError("--rate debe estar entre 0.9 y 1.1 para conservar naturalidad")

    text = prepare_continuous_text(input_path.read_text(encoding="utf-8"))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(
        f"Generando una toma continua en español latino con Qwen3-TTS "
        f"({args.speaker}, {len(text.split())} palabras, rate={args.rate:.2f})…",
        flush=True,
    )
    command = [
        str(engine),
        "-d", str(model_dir),
        "--speaker", args.speaker,
        "--language", "Spanish",
        "--instruct", DELIVERY_INSTRUCTION,
        "--text", text,
        "--output", str(output_path),
        "--seed", str(args.seed),
        "--temperature", "0.5",
        "--rate", f"{args.rate:.2f}",
        "--int8",
        "-j", str(max(1, min(args.threads, 4))),
    ]
    subprocess.run(command, check=True)
    if not output_path.exists() or output_path.stat().st_size < 1024:
        raise RuntimeError("Qwen3-TTS no generó un WAV válido")

    # Gentle studio finishing: retain vocal body and keep narration clearly upfront.
    finished = output_path.with_name(output_path.stem + "-finished.wav")
    audio_filter = (
        "highpass=f=60,"
        "equalizer=f=125:t=q:w=0.8:g=1.1,"
        "equalizer=f=2800:t=q:w=1.0:g=0.5,"
        "acompressor=threshold=-22dB:ratio=1.35:attack=22:release=210:makeup=1.1,"
        "loudnorm=I=-16:TP=-1.5:LRA=7"
    )
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(output_path),
        "-af", audio_filter,
        "-ar", "48000", "-ac", "2",
        "-c:a", "pcm_s16le",
        str(finished),
    ], check=True)
    finished.replace(output_path)

    duration = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(output_path)
    ], text=True).strip())
    print(
        f"Voz Ryan generada: {duration:.2f}s | español latino | toma continua | "
        "pausas naturales por puntuación y marcas de guion",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR al generar la voz Qwen3-TTS: {exc}", file=sys.stderr)
        raise
