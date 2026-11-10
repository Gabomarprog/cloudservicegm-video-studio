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


def generate_sound_design(audio_path, duration, words, assets):
    """Create original, gentle electronic music and scene-specific sound effects."""
    audio_path = Path(audio_path)
    with wave.open(str(audio_path), "rb") as src:
        sample_rate = src.getframerate()
        channels = src.getnchannels()
        sample_width = src.getsampwidth()
    if sample_width != 2 or channels not in (1, 2):
        raise RuntimeError("El audio de narración debe ser PCM de 16 bits mono o estéreo")

    frames = int(round(duration * sample_rate))
    assets = Path(assets)
    assets.mkdir(parents=True, exist_ok=True)

    # Merge speech intervals. Music gently ducks under speech and opens up in pauses.
    intervals = []
    for word in words:
        start_time = max(0.0, float(word["start"]) - 0.12)
        end_time = min(duration, float(word["end"]) + 0.20)
        if end_time > start_time:
            if intervals and start_time <= intervals[-1][1] + 0.08:
                intervals[-1] = (intervals[-1][0], max(intervals[-1][1], end_time))
            else:
                intervals.append((start_time, end_time))

    chords = [
        (164.81, 196.00, 246.94, 293.66),  # Em7
        (130.81, 164.81, 196.00, 246.94),  # Cmaj7
        (196.00, 246.94, 293.66, 369.99),  # Gmaj7
        (146.83, 185.00, 220.00, 293.66),  # Dsus2
    ]
    music_path = assets / "music-bed.wav"
    music_buffer = bytearray(frames * channels * 2)
    interval_index = 0
    beat_seconds = 0.60
    chord_seconds = 4.80

    def pad_for(notes, t):
        return (
            math.sin(2 * math.pi * notes[0] * t) * 0.020
            + math.sin(2 * math.pi * notes[1] * t + 0.35) * 0.017
            + math.sin(2 * math.pi * notes[2] * t + 0.70) * 0.014
            + math.sin(2 * math.pi * notes[3] * t + 1.05) * 0.009
            + math.sin(2 * math.pi * notes[0] * 0.5 * t) * 0.012
        )

    with wave.open(str(music_path), "wb") as music:
        music.setnchannels(channels)
        music.setsampwidth(2)
        music.setframerate(sample_rate)

        for frame in range(frames):
            t = frame / sample_rate
            while interval_index < len(intervals) and t > intervals[interval_index][1]:
                interval_index += 1
            talking = (
                interval_index < len(intervals)
                and intervals[interval_index][0] <= t <= intervals[interval_index][1]
            )

            chord_number = int(t / chord_seconds) % len(chords)
            chord = chords[chord_number]
            chord_phase = t % chord_seconds
            pad = pad_for(chord, t)
            if chord_phase < 0.45 and t >= chord_seconds:
                previous = chords[(chord_number - 1) % len(chords)]
                mix = chord_phase / 0.45
                mix = mix * mix * (3.0 - 2.0 * mix)
                pad = pad_for(previous, t) * (1.0 - mix) + pad * mix

            beat_number = int(t / beat_seconds)
            beat_age = t - beat_number * beat_seconds
            note = chord[beat_number % 4] * 2.0
            pluck = math.sin(2 * math.pi * note * beat_age) * math.exp(-beat_age * 15.0) * 0.012

            pulse_age = t % 2.40
            bass = (
                math.sin(2 * math.pi * (58.0 + 12.0 * pulse_age) * pulse_age)
                * math.exp(-pulse_age * 11.0) * 0.018
            )

            fade = min(1.0, t / 1.2) * min(1.0, max(0.0, (duration - t) / 1.4))
            duck = 0.58 if talking else 0.88
            value = (pad + pluck + bass) * duck * fade
            pan = 0.035 * math.sin(2 * math.pi * t / 13.0)
            left = max(-0.95, min(0.95, value * (1.0 - pan)))
            right = max(-0.95, min(0.95, value * (1.0 + pan)))
            if channels == 1:
                struct.pack_into("<h", music_buffer, frame * 2, int(((left + right) * 0.5) * 32767))
            else:
                struct.pack_into("<hh", music_buffer, frame * 4, int(left * 32767), int(right * 32767))

        music.writeframes(music_buffer)

    # Effects are a restrained scene layer, not one sound per spoken word.
    sfx_values = [0.0] * frames

    def add_sweep(start_time, length, low_hz, high_hz, gain):
        begin = max(0, int(start_time * sample_rate))
        count = min(int(length * sample_rate), frames - begin)
        if count <= 0:
            return
        for offset in range(count):
            local = offset / sample_rate
            progress = offset / max(1, count)
            envelope = math.sin(math.pi * progress) ** 1.45
            phase = 2 * math.pi * (
                low_hz * local + (high_hz - low_hz) * local * local / (2 * length)
            )
            tone = math.sin(phase) * 0.72 + math.sin(phase * 1.51 + 0.4) * 0.18
            sfx_values[begin + offset] += tone * envelope * gain

    def add_chime(start_time, notes, gain=0.035, length=0.72):
        begin = max(0, int(start_time * sample_rate))
        count = min(int(length * sample_rate), frames - begin)
        if count <= 0:
            return
        for offset in range(count):
            local = offset / sample_rate
            envelope = math.exp(-local * 4.8) * min(1.0, local / 0.025)
            tone = 0.0
            for note_index, frequency in enumerate(notes):
                tone += math.sin(2 * math.pi * frequency * local) * (0.58 / (1 + note_index * 0.55))
                tone += math.sin(2 * math.pi * frequency * 2.01 * local) * (0.10 / (1 + note_index))
            sfx_values[begin + offset] += tone * envelope * gain

    def add_soft_tap(start_time, gain=0.022):
        begin = max(0, int(start_time * sample_rate))
        count = min(int(0.18 * sample_rate), frames - begin)
        for offset in range(max(0, count)):
            local = offset / sample_rate
            envelope = math.exp(-local * 24.0)
            tone = math.sin(2 * math.pi * 880.0 * local) * 0.7
            tone += math.sin(2 * math.pi * 1320.0 * local) * 0.22
            sfx_values[begin + offset] += tone * envelope * gain

    scene_starts = [duration * value for value in (0.0, 0.12, 0.25, 0.39, 0.53, 0.68, 0.83)]
    add_sweep(0.10, 0.68, 260.0, 720.0, 0.030)
    add_sweep(scene_starts[1] + 0.12, 0.56, 320.0, 820.0, 0.034)
    add_soft_tap(scene_starts[1] + 1.02)
    add_sweep(scene_starts[1] + 3.55, 0.48, 520.0, 185.0, 0.038)
    add_chime(scene_starts[2] + 0.50, (659.25, 830.61), gain=0.024, length=0.55)
    add_sweep(scene_starts[3] + 0.40, 0.92, 72.0, 118.0, 0.040)
    add_chime(scene_starts[4] + 0.46, (587.33, 739.99, 880.00), gain=0.022, length=0.76)
    add_chime(scene_starts[5] + 0.48, (493.88, 659.25, 783.99), gain=0.024, length=0.82)
    add_chime(scene_starts[6] + 0.34, (523.25, 659.25, 783.99), gain=0.028, length=0.95)

    sfx_buffer = bytearray(frames * channels * 2)
    for frame, sample in enumerate(sfx_values):
        sample = max(-0.90, min(0.90, sample))
        if channels == 1:
            struct.pack_into("<h", sfx_buffer, frame * 2, int(sample * 32767))
        else:
            struct.pack_into("<hh", sfx_buffer, frame * 4, int(sample * 32767), int(sample * 32767))

    sfx_path = assets / "scene-sfx.wav"
    with wave.open(str(sfx_path), "wb") as sfx:
        sfx.setnchannels(channels)
        sfx.setsampwidth(2)
        sfx.setframerate(sample_rate)
        sfx.writeframes(sfx_buffer)

    print("Diseño sonoro creado: música ambiental original + 9 efectos de escena (sin sonidos por palabra).")


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
