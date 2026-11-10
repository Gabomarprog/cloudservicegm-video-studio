#!/usr/bin/env python3
import argparse
import json
import html
import shutil
import subprocess
import re
from pathlib import Path


def get_duration(audio):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(audio)
    ], text=True).strip()
    return max(5.0, float(out))


def load_words(path):
    """Accept either Whisper word timestamps or segment-level transcripts."""
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
        # If Whisper returns a sentence segment rather than individual words,
        # distribute its time span across its tokens to preserve phrase rhythm.
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


def group_words(words, max_words=4, max_span=1.75, pause=0.31):
    """Build readable phrase beats using punctuation, pauses and duration."""
    groups, current = [], []
    for word in words:
        if current:
            previous = current[-1]
            gap = word["start"] - previous["end"]
            punctuation = bool(re.search(r"[.!?;:,]$", previous["text"]))
            span = word["end"] - current[0]["start"]
            if (len(current) >= max_words or gap >= pause or punctuation or span >= max_span):
                groups.append(current)
                current = []
        current.append(word)
    if current:
        groups.append(current)
    return groups


def make_caption(group, index, start, end):
    text = " ".join(word["text"] for word in group)
    plain = re.sub(r"\s+", " ", text).strip()
    chars = len(plain)
    # Large display typography, auto-sized for each phrase rather than one tiny fixed subtitle size.
    font_size = max(178, min(340, int(3450 / max(10, chars))))
    layout = ["center", "upper", "center", "lower", "left", "center"][index % 6]
    mode = ["slam", "letters", "wipe", "side", "stretch", "flip"][index % 6]
    accent = ["red", "mint", "yellow", "white"][index % 4]
    word_markup = []
    for word_index, word in enumerate(group):
        char_markup = "".join(
            f'<span class="char">{html.escape(char)}</span>'
            for char in word["text"]
        )
        word_class = "word accent" if word_index == len(group) - 1 else "word"
        word_markup.append(f'<span class="{word_class}">{char_markup}</span>')
    markup = " ".join(word_markup)
    clip = (
        f'<div class="kinetic-clip clip layout-{layout} mode-{mode} accent-{accent}" '
        f'id="beat-{index}" data-start="{start:.3f}" data-duration="{max(.18, end-start):.3f}" '
        f'data-track-index="20" style="--type-size:{font_size}px">'
        f'<div class="type-ghost" aria-hidden="true">{html.escape(plain)}</div>'
        f'<div class="type-wrap"><div class="headline">{markup}</div></div>'
        f'</div>'
    )
    selector = f'"#beat-{index}"'
    chars_selector = f'"#beat-{index} .char"'
    if mode == "slam":
        enter = (
            f'tl.fromTo({selector},{{autoAlpha:0,scale:2.45,y:170,rotationZ:-7,filter:"blur(30px)"}},'
            f'{{autoAlpha:1,scale:1,y:0,rotationZ:0,filter:"blur(0px)",duration:.58,ease:"elastic.out(1,.58)"}},{start:.3f});'
            f'tl.fromTo({chars_selector},{{y:55,opacity:0,rotationX:-65}},'
            f'{{y:0,opacity:1,rotationX:0,duration:.34,stagger:.012,ease:"power3.out"}},{start + .08:.3f});'
        )
    elif mode == "letters":
        enter = (
            f'tl.fromTo({selector},{{autoAlpha:1,clipPath:"inset(0 0 100% 0)"}},'
            f'{{clipPath:"inset(0 0 0% 0)",duration:.48,ease:"expo.out"}},{start:.3f});'
            f'tl.fromTo({chars_selector},{{y:190,opacity:0,scale:.45,rotationX:-90,filter:"blur(18px)"}},'
            f'{{y:0,opacity:1,scale:1,rotationX:0,filter:"blur(0px)",duration:.48,stagger:.018,ease:"back.out(1.65)"}},{start:.02f});'
        )
    elif mode == "wipe":
        enter = (
            f'tl.fromTo({selector},{{autoAlpha:1,clipPath:"inset(0 100% 0 0)",x:-65}},'
            f'{{clipPath:"inset(0 0% 0 0)",x:0,duration:.55,ease:"expo.out"}},{start:.3f});'
            f'tl.fromTo({chars_selector},{{opacity:0,scaleX:.2}},'
            f'{{opacity:1,scaleX:1,duration:.26,stagger:.016,ease:"power2.out"}},{start + .08:.3f});'
        )
    elif mode == "side":
        direction = -1 if index % 2 else 1
        enter = (
            f'tl.fromTo({selector},{{autoAlpha:0,x:{direction * 900},skewX:{direction * -22},scaleX:.68,filter:"blur(22px)"}},'
            f'{{autoAlpha:1,x:0,skewX:0,scaleX:1,filter:"blur(0px)",duration:.62,ease:"expo.out"}},{start:.3f});'
            f'tl.fromTo({chars_selector},{{y:35,opacity:0}},'
            f'{{y:0,opacity:1,duration:.28,stagger:.01,ease:"power2.out"}},{start + .12:.3f});'
        )
    elif mode == "stretch":
        enter = (
            f'tl.fromTo({selector},{{autoAlpha:0,scaleX:.08,scaleY:1.5,letterSpacing:".35em",filter:"blur(20px)"}},'
            f'{{autoAlpha:1,scaleX:1,scaleY:1,letterSpacing:"-.035em",filter:"blur(0px)",duration:.62,ease:"expo.out"}},{start:.3f});'
            f'tl.fromTo({chars_selector},{{y:60,opacity:0}},'
            f'{{y:0,opacity:1,duration:.34,stagger:.012,ease:"power3.out"}},{start + .04:.3f});'
        )
    else:
        enter = (
            f'tl.fromTo({selector},{{autoAlpha:0,scale:.24,rotationX:75,rotationZ:8,y:90,filter:"blur(26px)"}},'
            f'{{autoAlpha:1,scale:1,rotationX:0,rotationZ:0,y:0,filter:"blur(0px)",duration:.65,ease:"back.out(1.45)"}},{start:.3f});'
            f'tl.fromTo({chars_selector},{{opacity:0,rotationY:90,z:-100}},'
            f'{{opacity:1,rotationY:0,z:0,duration:.4,stagger:.014,ease:"power3.out"}},{start + .06:.3f});'
        )
    exit_time = max(start + .22, end - .17)
    exit_anim = (
        f'tl.to({selector},{{autoAlpha:0,scale:{1.12 if index % 2 == 0 else .84},'
        f'y:{-65 if index % 2 == 0 else 45},filter:"blur(16px)",duration:.19,ease:"power2.in"}},{exit_time:.3f});'
    )
    return clip, enter + exit_anim


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
        raw_end = group[-1]["end"] + 0.12
        next_start = groups[index + 1][0]["start"] if index + 1 < len(groups) else duration
        end = min(duration, raw_end, max(start + 0.18, next_start - 0.015))
        markup, animation = make_caption(group, index, start, end)
        captions.append(markup)
        caption_anims.append(animation)

    # Seven distinct visual chapters, each with its own colour language and object animation.
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

    assets = Path(args.assets)
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copy2(args.audio, assets / "narration.wav")
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(template, encoding="utf-8")
    print(f"Composición creada: {output}")
    print(f"Duración: {duration:.2f}s | Palabras detectadas: {len(words)} | Bloques cinéticos: {len(captions)}")


if __name__ == "__main__":
    main()
