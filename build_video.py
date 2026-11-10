#!/usr/bin/env python3
import argparse
import json
import html
import shutil
import subprocess
import re
import wave
import math
import random
import struct
from pathlib import Path


def get_duration(audio):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio)
    ], text=True).strip()
    return max(5.0, float(out))


def load_words(path):
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return []
    if isinstance(data, dict):
        data = data.get("words") or data.get("segments") or data.get("transcription") or []
    result = []
    for item in data:
        if not isinstance(item, dict):
            continue
        text = str(item.get("text", "")).strip()
        if not text:
            continue
        try:
            start = float(item.get("start", item.get("start_time", 0)))
            end = float(item.get("end", item.get("end_time", start + 0.35)))
        except (TypeError, ValueError):
            continue
        start = max(0.0, start)
        end = max(start + 0.12, end)
        tokens = text.split()
        if len(tokens) > 1:
            span = max(0.12, end - start)
            step = span / len(tokens)
            for index, token in enumerate(tokens):
                result.append({
                    "text": token,
                    "start": start + index * step,
                    "end": min(end, start + (index + 1) * step)
                })
        else:
            result.append({"text": text, "start": start, "end": end})
    return sorted(result, key=lambda item: item["start"])


def group_words(words, max_words=3, max_span=1.55, pause=0.28):
    groups, current = [], []
    for word in words:
        if current:
            previous = current[-1]
            gap = word["start"] - previous["end"]
            punctuation = bool(re.search(r"[.!?;:,]$", previous["text"]))
            span = word["end"] - current[0]["start"]
            if len(current) >= max_words or gap >= pause or punctuation or span >= max_span:
                groups.append(current)
                current = []
        current.append(word)
    if current:
        groups.append(current)
    return groups


def make_caption(group, index, start, end, duration):
    phrase = " ".join(word["text"] for word in group)
    plain = re.sub(r"\s+", " ", phrase).strip()
    longest_word = max((len(word["text"]) for word in group), default=6)
    fit_phrase = int(3500 / max(14, chars))
    fit_word = int(2050 / max(6, longest_word))
    font_size = max(130, min(330, fit_phrase, fit_word))
    layouts = ["center", "upper", "lower", "left", "center", "right"]
    modes = ["slam", "letters", "wipe", "side", "stretch", "flip"]
    accents = ["red", "mint", "yellow", "white"]
    progress = start / max(1.0, duration)
    layout = layouts[index % len(layouts)] if progress < 0.25 else ["upper", "left", "upper", "right"][index % 4]
    mode = modes[index % len(modes)]
    accent = accents[index % len(accents)]
    contrast = "contrast-light" if (0.25 <= progress < 0.39 or progress >= 0.83) else "contrast-dark"

    word_markup = []
    for wi, word in enumerate(group):
        chars_html = "".join(
            f'<span class="char">{html.escape(char)}</span>'
            for char in word["text"]
        )
        word_class = "word accent-word" if wi == len(group) - 1 else "word"
        word_markup.append(f'<span class="{word_class}">{chars_html}</span>')
    markup = " ".join(word_markup)

    clip = (
        f'<div class="kinetic-clip layout-{layout} mode-{mode} accent-{accent} {contrast}" '
        f'id="beat-{index}" '
        
        f'style="--type-size:{font_size}px">'
        f'<div class="type-ghost" aria-hidden="true">{html.escape(plain)}</div>'
        f'<div class="type-wrap"><div class="headline">{markup}</div></div></div>'
    )

    root = f'"#beat-{index}"'
    letters = f'"#beat-{index} .char"'
    if mode == "slam":
        enter = (
            f'tl.fromTo({root},{{autoAlpha:0,scale:2.6,y:150,rotationZ:-8,filter:"blur(28px)"}},'
            f'{{autoAlpha:1,scale:1,y:0,rotationZ:0,filter:"blur(0px)",duration:.58,ease:"elastic.out(1,.55)"}},{start:.3f});'
            f'tl.fromTo({letters},{{y:65,opacity:0,rotationX:-75,scale:.55}},'
            f'{{y:0,opacity:1,rotationX:0,scale:1,duration:.34,stagger:.018,ease:"back.out(1.6)"}},{start + .04:.3f});'
        )
    elif mode == "letters":
        enter = (
            f'tl.fromTo({root},{{autoAlpha:1,clipPath:"inset(0 0 100% 0)"}},'
            f'{{clipPath:"inset(0 0 0% 0)",duration:.52,ease:"expo.out"}},{start:.3f});'
            f'tl.fromTo({letters},{{y:200,opacity:0,scale:.38,rotationX:-90,filter:"blur(22px)"}},'
            f'{{y:0,opacity:1,scale:1,rotationX:0,filter:"blur(0px)",duration:.48,stagger:.025,ease:"back.out(1.65)"}},{start + .02:.3f});'
        )
    elif mode == "wipe":
        enter = (
            f'tl.fromTo({root},{{autoAlpha:1,clipPath:"inset(0 100% 0 0)",x:-75}},'
            f'{{clipPath:"inset(0 0% 0 0)",x:0,duration:.6,ease:"expo.out"}},{start:.3f});'
            f'tl.fromTo({letters},{{opacity:0,scaleX:.12,filter:"blur(12px)"}},'
            f'{{opacity:1,scaleX:1,filter:"blur(0px)",duration:.3,stagger:.02,ease:"power2.out"}},{start + .08:.3f});'
        )
    elif mode == "side":
        direction = -1 if index % 2 else 1
        enter = (
            f'tl.fromTo({root},{{autoAlpha:0,x:{direction * 1000},skewX:{direction * -24},scaleX:.65,filter:"blur(24px)"}},'
            f'{{autoAlpha:1,x:0,skewX:0,scaleX:1,filter:"blur(0px)",duration:.64,ease:"expo.out"}},{start:.3f});'
            f'tl.fromTo({letters},{{y:45,opacity:0}},'
            f'{{y:0,opacity:1,duration:.3,stagger:.015,ease:"power2.out"}},{start + .1:.3f});'
        )
    elif mode == "stretch":
        enter = (
            f'tl.fromTo({root},{{autoAlpha:0,scaleX:.06,scaleY:1.55,letterSpacing:".4em",filter:"blur(22px)"}},'
            f'{{autoAlpha:1,scaleX:1,scaleY:1,letterSpacing:"-.035em",filter:"blur(0px)",duration:.65,ease:"expo.out"}},{start:.3f});'
            f'tl.fromTo({letters},{{y:70,opacity:0,rotationY:70}},'
            f'{{y:0,opacity:1,rotationY:0,duration:.34,stagger:.018,ease:"power3.out"}},{start + .04:.3f});'
        )
    else:
        enter = (
            f'tl.fromTo({root},{{autoAlpha:0,scale:.16,rotationX:82,rotationZ:9,y:110,filter:"blur(30px)"}},'
            f'{{autoAlpha:1,scale:1,rotationX:0,rotationZ:0,y:0,filter:"blur(0px)",duration:.68,ease:"back.out(1.5)"}},{start:.3f});'
            f'tl.fromTo({letters},{{opacity:0,rotationY:90,z:-130}},'
            f'{{opacity:1,rotationY:0,z:0,duration:.4,stagger:.02,ease:"power3.out"}},{start + .06:.3f});'
        )

    exit_time = max(start + .24, end - .18)
    exit_anim = (
        f'tl.to({root},{{autoAlpha:0,scale:{1.14 if index % 2 == 0 else .82},'
        f'y:{-85 if index % 2 == 0 else 65},filter:"blur(18px)",duration:.2,ease:"power2.in"}},{exit_time:.3f});'
    )
    return clip, enter + exit_anim


def add_transition_sfx(audio_path, duration):
    """A few quiet scene-transition sweeps; intentionally no per-word ticks."""
    audio = Path(audio_path)
    normalized = audio.with_name("narration_sfx_base.wav")
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-i", str(audio),
        "-acodec", "pcm_s16le", str(normalized)
    ], check=True)
    with wave.open(str(normalized), "rb") as src:
        channels = src.getnchannels()
        rate = src.getframerate()
        frames = src.getnframes()
        width = src.getsampwidth()
        raw = src.readframes(frames)
    normalized.unlink(missing_ok=True)
    if width != 2:
        return
    sfx = [0.0] * frames
    rng = random.Random(91)
    # Only three understated sweeps across the whole piece; the voice stays dominant.
    for event in [0.12, duration * .39, duration * .70]:
        begin = max(0, int(event * rate))
        length = int(.34 * rate)
        for j in range(length):
            idx = begin + j
            if idx >= frames:
                break
            t = j / rate
            env = math.sin(math.pi * min(1.0, j / max(1, length))) ** 1.5
            frequency = 150 - 85 * (j / max(1, length))
            sweep = math.sin(2 * math.pi * frequency * t) * .035
            air = (rng.random() * 2 - 1) * .012
            sfx[idx] += (sweep + air) * env
    packed = bytearray()
    for frame_index in range(frames):
        base = frame_index * channels * 2
        for channel in range(channels):
            original = struct.unpack_from("<h", raw, base + channel * 2)[0] / 32768.0
            mixed = max(-1.0, min(1.0, original + sfx[frame_index]))
            packed.extend(struct.pack("<h", int(mixed * 32767)))
    with wave.open(str(audio), "wb") as out:
        out.setnchannels(channels)
        out.setsampwidth(2)
        out.setframerate(rate)
        out.writeframes(packed)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript", required=True)
    parser.add_argument("--audio", required=True)
    parser.add_argument("--template", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--assets", required=True)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()

    duration = get_duration(args.audio)
    words = load_words(args.transcript)
    groups = group_words(words)
    captions, caption_anims = [], []
    for index, group in enumerate(groups):
        start = group[0]["start"]
        next_start = groups[index + 1][0]["start"] if index + 1 < len(groups) else duration
        end = min(duration, group[-1]["end"] + .10, max(start + .2, next_start - .02))
        markup, animation = make_caption(group, index, start, end, duration)
        captions.append(markup)
        caption_anims.append(animation)

    # Three low-level scene transitions only. No sound is attached to individual words.
    add_transition_sfx(args.audio, duration)

    fractions = [0.0, 0.12, 0.25, 0.39, 0.53, 0.68, 0.83, 1.0]
    replacements = {
        "{{TITLE}}": html.escape(args.title),
        "{{DURATION}}": f"{duration:.3f}",
        "{{CAPTIONS}}": "\n".join(captions),
        "{{CAPTION_ANIMS}}": "\n".join(caption_anims),
    }
    for index in range(7):
        start = duration * fractions[index]
        end = duration * fractions[index + 1]
        replacements[f"{{{{S{index}_START}}}}"] = f"{start:.3f}"
        replacements[f"{{{{S{index}_DURATION}}}}"] = f"{end-start:.3f}"
        replacements[f"{{{{S{index}_END}}}}"] = f"{end:.3f}"

    template = Path(args.template).read_text(encoding="utf-8")
    for key, value in replacements.items():
        template = template.replace(key, value)
    if "{{S" in template or "{{CAPTION" in template or "{{DURATION}}" in template:
        raise RuntimeError("Quedaron marcadores sin sustituir en la plantilla")

    assets = Path(args.assets)
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.audio, assets / "narration.wav")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(template, encoding="utf-8")
    print(f"Composición creada: {output}")
    print(f"Duración: {duration:.2f}s | Palabras: {len(words)} | Bloques cinéticos: {len(captions)}")


if __name__ == "__main__":
    main()
