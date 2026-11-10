#!/usr/bin/env python3
"""Original low-baritone Latin-American Spanish narration using Qwen3-TTS VoiceDesign."""
from __future__ import annotations
import argparse, re, subprocess, sys
from pathlib import Path

# Voice identity: fuller, darker, chest-resonant and confidently masculine.
# Delivery: connected conversational phrasing, not whispery and not artificially slow.
VOICE_INSTRUCTION = (
    "Voz de hombre adulto, claramente masculina, de barítono grave-medio, con "
    "resonancia de pecho marcada, cuerpo y densidad vocal. Timbre profundo, redondo, "
    "cálido y firme, con presencia al frente y una textura suave pero no aireada. "
    "Español latinoamericano neutro, pronunciación clara y natural. "
    "Debe sonar maduro, seguro y elegante: una voz con peso y autoridad tranquila, "
    "no fina, no aguda, no juvenil, no débil, no susurrada y no afeminada. "
    "Habla en frases conectadas, con ritmo conversacional fluido y ligeramente ágil. "
    "No hagas pausas artificiales al terminar cada oración: enlaza la siguiente idea "
    "con naturalidad. Usa solo las pausas breves que pide la puntuación y una pausa "
    "un poco mayor al cerrar una idea completa. No alargues vocales ni finales de "
    "frase, no dramatices ni leas palabra por palabra. "
    "La entonación debe ser cálida, envolvente y expresiva con moderación, como un "
    "narrador documental moderno hablando con cercanía y confianza, no como un "
    "locutor de publicidad. Mantén el mismo registro grave y el mismo cuerpo durante "
    "todo el texto. Una voz humana, estable, fluida y agradable de escuchar."
)


def prepare_continuous_text(raw: str) -> str:
    """Keep the complete narration in one synthesis pass to preserve prosodic flow."""
    paragraphs = [
        re.sub(r"\s+", " ", part).strip()
        for part in re.split(r"\n\s*\n", raw.strip())
        if part.strip()
    ]
    if not paragraphs:
        raise RuntimeError("El guion está vacío o no contiene texto utilizable")
    # A paragraph break is a deliberate change of thought. Ordinary newlines are
    # flattened; sentence punctuation is left for the model's natural prosody.
    return " [pause:280ms] ".join(paragraphs)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--engine", default="tools/qwen3-tts/qwen_tts")
    parser.add_argument("--model", default="models/qwen3-tts-voice-design")
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--seed", type=int, default=20261110)
    parser.add_argument("--rate", type=float, default=1.12)
    args = parser.parse_args()

    input_path, output_path = Path(args.input), Path(args.output)
    engine, model_dir = Path(args.engine), Path(args.model)
    if not input_path.exists():
        raise FileNotFoundError(f"No existe el guion: {input_path}")
    if not engine.exists():
        raise FileNotFoundError(f"No se encuentra el motor Qwen3-TTS: {engine}")
    if not (model_dir / "config.json").exists():
        raise FileNotFoundError(f"No se encuentra el modelo VoiceDesign: {model_dir}")
    if not 1.0 <= args.rate <= 1.15:
        raise ValueError("--rate debe estar entre 0.95 y 1.15 para conservar naturalidad")

    text = prepare_continuous_text(input_path.read_text(encoding="utf-8"))
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(
        "Generando una sola toma continua con voz masculina barítono "
        f"({len(text.split())} palabras, rate={args.rate:.2f})…",
        flush=True,
    )
    command = [
        str(engine),
        "-d", str(model_dir),
        "--voice-design",
        "-l", "Spanish",
        "--instruct", VOICE_INSTRUCTION,
        "--text", text,
        "-o", str(output_path),
        "--seed", str(args.seed),
        "--temperature", "0.38",
        "--rate", f"{args.rate:.2f}",
        "--int8",
        "-j", str(max(1, min(args.threads, 4))),
    ]
    subprocess.run(command, check=True)
    if not output_path.exists() or output_path.stat().st_size < 1024:
        raise RuntimeError("Qwen3-TTS no generó un WAV válido")

    # Gentle studio finishing; a small low-mid lift adds body without muddying speech.
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
        f"Voz barítono generada: {duration:.2f}s | una sola toma | "
        f"rate {args.rate:.2f} | pausas solo por puntuación/ideas",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR al generar la voz Qwen3-TTS: {exc}", file=sys.stderr)
        raise
