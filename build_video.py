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


def group_words(words, max_words=4, max_span=2.15, pause=0.42):
    """Group tokens into readable phrase beats, leaving a little breathing room."""
    groups, current = [], []
    for word in words:
        if current:
            previous = current[-1]
            gap = word["start"] - previous["end"]
            punctuation = bool(re.search(r"[.!?;:,]$", previous["text"]))
            span = word["end"] - current[0]["start"]
            if (len(current) >= max_words or gap >= pause or
                    (punctuation and len(current) >= 3) or span >= max_span):
                groups.append(current)
                current = []
        current.append(word)
    if current:
        groups.append(current)
    return groups


def make_caption(group, index, start, end, duration):
    phrase = " ".join(word["text"] for word in group)
    plain = re.sub(r"\s+", " ", phrase).strip()
    chars = len(plain)
    longest_word = max((len(word["text"]) for word in group), default=6)
    fit_phrase = int(3450 / max(12, chars))
    fit_word = int(1900 / max(6, longest_word))
    font_size = max(138, min(330, fit_phrase, fit_word))

    layouts = ["center", "upper", "lower", "left", "upper", "right"]
    modes = ["slam", "letters", "wipe", "side", "stretch", "flip"]
    accents = ["red", "mint", "yellow", "white"]
    progress = start / max(1.0, duration)
    if 0.12 <= progress < 0.25:
        layout = "upper"  # keep the phone's screen visible below the headline
    elif progress < 0.25:
        layout = layouts[index % len(layouts)]
    else:
        layout = ["upper", "left", "upper", "right"][index % 4]
    mode = modes[index % len(modes)]
    accent = accents[index % len(accents)]
    contrast = "contrast-light" if (0.25 <= progress < 0.39 or progress >= 0.83) else "contrast-dark"

    word_markup = []
    for word_index, word in enumerate(group):
        glyphs = "".join(
            f'<span class="char">{html.escape(char)}</span>'
            for char in word["text"]
        )
        word_class = "word accent-word" if word_index == len(group) - 1 else "word"
        word_markup.append(f'<span class="{word_class}">{glyphs}</span>')
    markup = " ".join(word_markup)

    clip = (
        f'<div class="kinetic-clip layout-{layout} mode-{mode} accent-{accent} {contrast}" '
        f'id="beat-{index}" style="--type-size:{font_size}px">'
        f'<div class="type-wrap"><div class="headline">{markup}</div></div></div>'
    )

    root = f'"#beat-{index}"'
    glyphs = f'"#beat-{index} .char"'
    if mode == "slam":
        enter = (
            f'tl.fromTo({root},{{autoAlpha:0,scale:1.55,y:58,rotationZ:-2.5}},'
            f'{{autoAlpha:1,scale:1,y:0,rotationZ:0,duration:.54,ease:"power3.out"}},{start:.3f});'
            f'tl.fromTo({glyphs},{{y:32,opacity:0,rotationX:-15,scale:.94}},'
            f'{{y:0,opacity:1,rotationX:0,scale:1,duration:.46,stagger:.024,ease:"power2.out"}},{start + .02:.3f});'
        )
    elif mode == "letters":
        enter = (
            f'tl.fromTo({root},{{autoAlpha:0,y:38,scale:.97}},'
            f'{{autoAlpha:1,y:0,scale:1,duration:.52,ease:"power3.out"}},{start:.3f});'
            f'tl.fromTo({glyphs},{{y:68,opacity:0,scale:.9,rotationX:-18}},'
            f'{{y:0,opacity:1,scale:1,rotationX:0,duration:.46,stagger:.024,ease:"power2.out"}},{start + .02:.3f});'
        )
    elif mode == "wipe":
        enter = (
            f'tl.fromTo({root},{{autoAlpha:0,x:-95,scaleX:.9}},'
            f'{{autoAlpha:1,x:0,scaleX:1,duration:.52,ease:"power3.out"}},{start:.3f});'
            f'tl.fromTo({glyphs},{{x:-18,opacity:0,scaleX:.9}},'
            f'{{x:0,opacity:1,scaleX:1,duration:.42,stagger:.022,ease:"power2.out"}},{start + .02:.3f});'
        )
    elif mode == "side":
        direction = -1 if index % 2 else 1
        enter = (
            f'tl.fromTo({root},{{autoAlpha:0,x:{direction * 460},rotationZ:{direction * -1.8},scale:.95}},'
            f'{{autoAlpha:1,x:0,rotationZ:0,scale:1,duration:.56,ease:"power3.out"}},{start:.3f});'
            f'tl.fromTo({glyphs},{{y:28,opacity:0,rotationY:12}},'
            f'{{y:0,opacity:1,rotationY:0,duration:.42,stagger:.022,ease:"power2.out"}},{start + .025:.3f});'
        )
    elif mode == "stretch":
        enter = (
            f'tl.fromTo({root},{{autoAlpha:0,scaleX:.78,scaleY:1.08}},'
            f'{{autoAlpha:1,scaleX:1,scaleY:1,duration:.54,ease:"power3.out"}},{start:.3f});'
            f'tl.fromTo({glyphs},{{x:18,y:28,opacity:0,rotationY:12,scaleX:.9}},'
            f'{{x:0,y:0,opacity:1,rotationY:0,scaleX:1,duration:.42,stagger:.022,ease:"power2.out"}},{start + .02:.3f});'
        )
    else:
        enter = (
            f'tl.fromTo({root},{{autoAlpha:0,scale:.88,rotationX:18,rotationZ:1.5,y:42}},'
            f'{{autoAlpha:1,scale:1,rotationX:0,rotationZ:0,y:0,duration:.56,ease:"power3.out"}},{start:.3f});'
            f'tl.fromTo({glyphs},{{opacity:0,rotationY:18,z:-24}},'
            f'{{opacity:1,rotationY:0,z:0,duration:.44,stagger:.022,ease:"power2.out"}},{start + .025:.3f});'
        )

    # Entry and exit stay separated for smooth, readable transitions.
    next_start = end
    exit_time = max(start + .70, end - .16)
    exit_time = min(exit_time, next_start - .05) if next_start > start + .76 else exit_time
    exit_anim = (
        f'tl.to({root},{{autoAlpha:0,scale:1.015,'
        f'y:{-28 if index % 2 == 0 else 24},duration:.24,ease:"power2.inOut"}},{exit_time:.3f});'
    )
    return clip, enter + exit_anim


SFX_LIBRARY = {
    "whoosh": "https://gettakes.app/sounds/whoosh.wav",
    "swish": "https://gettakes.app/sounds/swish.wav",
    "click": "https://gettakes.app/sounds/click.wav",
    "tap": "https://gettakes.app/sounds/tap.wav",
    "pop": "https://gettakes.app/sounds/pop.wav",
    "typing": "https://gettakes.app/sounds/typing.wav",
    "notification": "https://gettakes.app/sounds/notification.wav",
    "ding": "https://gettakes.app/sounds/ding.wav",
    "quick-riser": "https://gettakes.app/sounds/quick-riser.wav",
    "sci-fi": "https://gettakes.app/sounds/sci-fi.wav",
    "glitch": "https://gettakes.app/sounds/glitch.wav",
    "water-drop": "https://gettakes.app/sounds/water-drop.wav",
    "correct-answer": "https://gettakes.app/sounds/correct-answer.wav",
    "sparkle": "https://gettakes.app/sounds/sparkle.wav",
    "logo-sting": "https://gettakes.app/sounds/logo-sting.wav",
    "downlifter": "https://gettakes.app/sounds/downlifter.wav",
}


def download_sfx_library(assets):
    """Download a small CC0/royalty-free UI and transition SFX library."""
    import urllib.request
    from urllib.error import URLError, HTTPError

    folder = Path(assets) / "sfx"
    folder.mkdir(parents=True, exist_ok=True)
    downloaded = {}
    for name, url in SFX_LIBRARY.items():
        target = folder / f"{name}.wav"
        if target.exists() and target.stat().st_size > 1024:
            downloaded[name] = target
            continue

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "cloudservicegm-video-studio/1.0"}
        )
        last_error = None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(request, timeout=30) as response:
                    data = response.read()
                if len(data) < 1024 or not data.startswith(b"RIFF"):
                    raise RuntimeError(f"Respuesta WAV inválida para {name}")
                target.write_bytes(data)
                downloaded[name] = target
                break
            except (URLError, HTTPError, TimeoutError, RuntimeError) as exc:
                last_error = exc
                if attempt == 2:
                    print(f"AVISO: no se pudo descargar SFX {name}: {exc}")
        if name not in downloaded and last_error:
            continue

    required = {"whoosh", "swish", "click", "tap", "pop", "typing", "notification", "glitch"}
    missing = sorted(required - set(downloaded))
    if missing:
        raise RuntimeError(
            "No se pudo descargar la biblioteca de efectos de sonido necesarios: "
            + ", ".join(missing)
        )
    return downloaded


def build_sound_effects(duration, words, groups, assets):
    """Compose frequent but restrained scene/action SFX. No continuous music bed."""
    downloaded = download_sfx_library(assets)
    fractions = (0.0, 0.12, 0.25, 0.39, 0.53, 0.68, 0.83)
    scene = [duration * value for value in fractions]
    events = []

    def add(name, at, gain=0.18, label=""):
        at = max(0.0, float(at))
        if at < duration and name in downloaded:
            events.append({
                "name": name,
                "time": at,
                "gain": gain,
                "label": label
            })

    # 01 · Intro: a soft lift, then two accents tied to the large title/ribbon.
    add("quick-riser", 0.00, 0.16, "intro lift")
    add("whoosh", 0.34, 0.19, "first title arrives")
    add("swish", 2.00, 0.17, "yellow ribbon slides in")
    add("pop", 3.55, 0.19, "main hook lands")

    # 02 · Phone: entrance, URL typing, touch, loading, timeout and error reveal.
    add("whoosh", scene[1] + 0.12, 0.22, "phone enters close-up")
    add("typing", scene[1] + 0.58, 0.20, "URL types into phone")
    add("tap", scene[1] + 1.28, 0.20, "page is opened")
    add("swish", scene[1] + 2.35, 0.14, "phone page scrolls")
    add("glitch", scene[1] + 3.52, 0.17, "website connection fails")
    add("notification", scene[1] + 3.78, 0.18, "timeout warning appears")

    # 03 · Dashboard: screen comes forward, interface controls and metrics activate.
    add("whoosh", scene[2] + 0.20, 0.17, "dashboard arrives")
    add("click", scene[2] + 1.18, 0.18, "CPU metric appears")
    add("click", scene[2] + 1.34, 0.16, "RAM metric appears")
    add("click", scene[2] + 1.50, 0.16, "server status appears")
    add("water-drop", scene[2] + 1.72, 0.14, "chart completes")
    add("ding", scene[2] + 2.45, 0.13, "healthy server confirmation")

    # 04 · Server racks: a restrained power-up, followed by several LED/UI ticks.
    add("sci-fi", scene[3] + 0.24, 0.17, "server racks power on")
    add("quick-riser", scene[3] + 0.92, 0.13, "rack animation builds")
    for offset in (1.42, 1.63, 1.84, 2.05):
        add("click", scene[3] + offset, 0.13, "server status light")

    # 05 · Network: each node receives a distinct small sound; lines sweep between them.
    add("whoosh", scene[4] + 0.16, 0.16, "network scene enters")
    add("pop", scene[4] + 0.36, 0.17, "web node")
    add("notification", scene[4] + 0.55, 0.16, "VPS node")
    add("water-drop", scene[4] + 0.74, 0.16, "database node")
    add("pop", scene[4] + 0.93, 0.15, "SSL node")
    add("swish", scene[4] + 1.14, 0.14, "data links draw")

    # 06 · Security: shield reveal and a short sequence of confirmation clicks.
    add("whoosh", scene[5] + 0.20, 0.15, "security shield reveals")
    add("ding", scene[5] + 0.52, 0.17, "protection activates")
    for offset in (1.16, 1.30, 1.44, 1.58):
        add("click", scene[5] + offset, 0.14, "security control enabled")
    add("correct-answer", scene[5] + 1.92, 0.15, "security checklist complete")

    # 07 · Brand close: logo arrival and warm final shimmer.
    add("logo-sting", scene[6] + 0.24, 0.17, "brand mark appears")
    add("sparkle", scene[6] + 1.18, 0.16, "final call to action")
    add("tap", scene[6] + 1.72, 0.14, "CTA button")

    # A soft swish on selected phrase changes, never on every word.
    major_times = [event["time"] for event in events]
    phrase_events = 0
    for index, group in enumerate(groups):
        if index % 3 != 1:
            continue
        at = group[0]["start"] + 0.035
        if any(abs(at - major) < 0.34 for major in major_times):
            continue
        add("swish" if index % 2 else "pop", at, 0.105, "phrase emphasis")
        phrase_events += 1

    events.sort(key=lambda item: item["time"])
    if not events:
        raise RuntimeError("No se generaron eventos de sonido")

    # Each short WAV is positioned on its exact scene/event frame by FFmpeg.
    args = ["ffmpeg", "-y", "-loglevel", "error"]
    for event in events:
        args.extend(["-i", str(downloaded[event["name"]])])

    filters = []
    labels = []
    for index, event in enumerate(events):
        delay_ms = int(round(event["time"] * 1000))
        filters.append(
            f"[{index}:a]aresample=44100,volume={event['gain']:.3f},"
            f"adelay={delay_ms}:all=1,apad=pad_dur={duration:.3f},"
            f"atrim=duration={duration:.3f}[s{index}]"
        )
        labels.append(f"[s{index}]")

    filters.append(
        "".join(labels)
        + f"amix=inputs={len(events)}:duration=longest:normalize=0,"
        + f"alimiter=limit=0.88,atrim=duration={duration:.3f}[out]"
    )
    sfx_path = Path(assets) / "scene-sfx.wav"
    args.extend([
        "-filter_complex", ";".join(filters),
        "-map", "[out]", "-ar", "44100", "-ac", "2",
        "-c:a", "pcm_s16le", str(sfx_path)
    ])
    subprocess.run(args, check=True)

    manifest = {
        "background_music": False,
        "voice": "separate foreground track",
        "event_count": len(events),
        "phrase_accent_count": phrase_events,
        "events": events,
        "source": "Takes free sound effects; stated free for any use, no credit required"
    }
    (Path(assets) / "sound-design.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(
        f"Diseño sonoro creado: {len(events)} efectos sincronizados, "
        f"{phrase_events} acentos de frase y SIN música de fondo."
    )
    return sfx_path


def mix_voice_and_effects(voice_path, sfx_path, output_path):
    """Keep narration in front while layering the timed effects underneath."""
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(voice_path),
        "-i", str(sfx_path),
        "-filter_complex",
        "[1:a]volume=1.0[sfx];"
        "[0:a][sfx]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
        "alimiter=limit=0.94[out]",
        "-map", "[out]", "-ar", "44100", "-ac", "2",
        "-c:a", "pcm_s16le", str(output_path)
    ], check=True)

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

    assets = Path(args.assets)
    assets.mkdir(parents=True, exist_ok=True)

    # Generate separate original music and scene SFX stems, then mix them under the voice.
    generate_sound_design(args.audio, duration, words, assets)
    mixed_audio = assets / "narration.wav"
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(args.audio),
        "-i", str(assets / "music-bed.wav"),
        "-i", str(assets / "scene-sfx.wav"),
        "-filter_complex",
        "[1:a]volume=1.0[music];"
        "[2:a]volume=1.0[sfx];"
        "[0:a][music][sfx]amix=inputs=3:duration=first:dropout_transition=1:normalize=0,"
        "alimiter=limit=0.95[out]",
        "-map", "[out]", "-c:a", "pcm_s16le", str(mixed_audio)
    ], check=True)

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

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(template, encoding="utf-8")
    print(f"Composición creada: {output}")
    print(f"Duración: {duration:.2f}s | Palabras: {len(words)} | Bloques cinéticos: {len(captions)}")


if __name__ == "__main__":
    main()
