#!/usr/bin/env python3
"""Generate one continuous Spanish narration with Qwen3-TTS 0.6B CustomVoice / Ryan.

This intentionally uses the exact model family used by the published Spanish Ryan
sample: native Spanish language conditioning, native speaking rate, no English
voice-design prompt, no forced pause tags, and no post-generation time stretching.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


def read_narration(path: Path) -> str:
    """Flatten layout whitespace but preserve sentence punctuation and wording."""
    text = path.read_text(encoding="utf-8-sig")
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        raise RuntimeError("El guion está vacío o no contiene texto utilizable")
    return text


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--engine", default="tools/qwen3-tts/qwen_tts")
    parser.add_argument("--model", default="models/qwen3-tts-0.6b-customvoice")
    parser.add_argument("--threads", type=int, default=4)
    args = parser.parse_args()

    source = Path(args.input)
    output = Path(args.output)
    engine = Path(args.engine)
    model_dir = Path(args.model)

    if not source.is_file():
        raise FileNotFoundError(f"No existe el guion: {source}")
    if not engine.is_file():
        raise FileNotFoundError(f"No se encuentra el motor Qwen3-TTS: {engine}")
    if not (model_dir / "config.json").is_file():
        raise FileNotFoundError(f"No se encuentra el modelo CustomVoice 0.6B: {model_dir}")
    if args.threads < 1:
        raise ValueError("--threads debe ser al menos 1")

    text = read_narration(source)
    output.parent.mkdir(parents=True, exist_ok=True)

    command = [
        str(engine),
        "--model-dir", str(model_dir),
        "--speaker", "ryan",
        "--language", "Spanish",
        "--text", text,
        "--output", str(output),
        "--threads", str(min(args.threads, 4)),
    ]

    # No --instruct: this is the 0.6B model, and the Spanish sample is generated
    # by the native Spanish language path. No --rate: preserve model prosody.
    print(
        "Generando Ryan con Qwen3-TTS CustomVoice 0.6B, español nativo, "
        f"una sola toma y velocidad original ({len(text.split())} palabras)…",
        flush=True,
    )
    subprocess.run(command, check=True)

    if not output.is_file() or output.stat().st_size < 1024:
        raise RuntimeError("Qwen3-TTS no generó un WAV válido")

    duration = float(subprocess.check_output([
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(output),
    ], text=True).strip())

    print(
        f"Ryan 0.6B generado: {duration:.2f}s | español | "
        "velocidad nativa | sin pausas añadidas ni estiramiento temporal",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR al generar la voz Ryan 0.6B: {exc}", file=sys.stderr)
        raise
