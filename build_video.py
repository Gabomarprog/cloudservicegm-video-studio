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
        # Whisper may confuse the Spanish letter name for the acronym VPS and
        # emit BPS. Keep the canonical product/networking acronym in captions.
        text = re.sub(r"(?i)(?<!\\w)B[.\\s-]*P[.\\s-]*S(?!\\w)", "VPS", text)
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


SFX_SOURCE_COMMIT = "92780e7ab0cdfb557497a988089c47f46e8c7412"
SFX_BASE_URL = f"https://raw.githubusercontent.com/wyzowl/sfx-kit/{SFX_SOURCE_COMMIT}/"

SFX_IDS = [
    "whoosh-medium-soft",
    "swish-medium",
    "pop-medium-in",
    "pop-small-in",
    "keyboard-typing-steady-medium",
    "keyboard-return-medium",
    "click-tap-medium",
    "notification-error-soft",
    "notification-success-soft",
    "data-chart-reveal",
    "data-bar-grow",
    "data-progress-short",
    "digital-process-subtle",
    "digital-power-up",
    "digital-glitch-subtle",
    "digital-signal-drop",
    "mechanical-switch-light",
    "tone-step-1",
    "tone-step-2",
    "tone-step-3",
    "tone-step-4",
    "sting-warm-short",
    "shimmer-short-soft",
    "impact-light-soft",
    "swipe-medium-soft",
]


def download_sfx_assets(assets):
    """Download only the selected CC0 WAVs plus their source metadata."""
    import urllib.request
    from urllib.error import URLError, HTTPError

    folder = Path(assets) / "sfx"
    folder.mkdir(parents=True, exist_ok=True)
    manifest_path = folder / "sounds.json"

    def download(url, target, min_size=100):
        if target.exists() and target.stat().st_size >= min_size:
            return
        last_error = None
        for attempt in range(3):
            try:
                request = urllib.request.Request(
                    url,
                    headers={"User-Agent": "cloudservicegm-video-studio/1.0"}
                )
                with urllib.request.urlopen(request, timeout=40) as response:
                    data = response.read()
                if len(data) < min_size:
                    raise RuntimeError(f"Descarga incompleta: {url}")
                target.write_bytes(data)
                return
            except (URLError, HTTPError, TimeoutError, RuntimeError) as exc:
                last_error = exc
        raise RuntimeError(f"No se pudo descargar {url}: {last_error}")

    download(SFX_BASE_URL + "sounds.json", manifest_path, min_size=1000)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("license") != "CC0-1.0":
        raise RuntimeError("La biblioteca de efectos no confirma licencia CC0-1.0")

    sound_map = {item["id"]: item for item in manifest.get("sounds", [])}
    downloaded = {}
    for sound_id in SFX_IDS:
        item = sound_map.get(sound_id)
        if not item:
            raise RuntimeError(f"Falta el efecto requerido en SFX Kit: {sound_id}")
        relative = item["file"]
        target = folder / f"{sound_id}.wav"
        download(SFX_BASE_URL + relative, target, min_size=1024)
        downloaded[sound_id] = {
            "path": target,
            "metadata": item
        }

    # Keep the source and licence information with the generated video assets.
    (folder / "SOURCE.txt").write_text(
        "SFX Kit by Wyzowl\n"
        "Source: https://github.com/wyzowl/sfx-kit\n"
        f"Pinned commit: {SFX_SOURCE_COMMIT}\n"
        "Licence: CC0-1.0 — commercial use allowed; attribution not required.\n"
        "Only the sound files used by this video were downloaded.\n",
        encoding="utf-8"
    )
    return downloaded


def sound_effect_schedule(duration, groups):
    """On-screen action moments: timings are scene-relative and intentionally varied."""
    s = [duration * fraction for fraction in (0.0, 0.12, 0.25, 0.39, 0.53, 0.68, 0.83)]
    events = []

    def cue(sound_id, moment, label, gain_db=0.0):
        if moment < duration - 0.02:
            events.append({
                "id": sound_id,
                "moment": round(float(moment), 3),
                "label": label,
                "gain_db": float(gain_db)
            })

    # 01 — Hook and ribbon: light movement and a rounded title arrival.
    cue("whoosh-medium-soft", 0.56, "intro title movement")
    cue("pop-medium-in", 3.52, "headline lands")
    cue("swish-medium", 3.78, "yellow infrastructure ribbon")

    # 02 — Phone close-up: entry, actual URL typing, submit, scroll, loading and failure.
    cue("whoosh-medium-soft", s[1] + 0.42, "phone enters close-up")
    cue("keyboard-typing-steady-medium", s[1] + 0.72, "URL is typed into the phone")
    cue("keyboard-return-medium", s[1] + 1.88, "URL submit")
    cue("click-tap-medium", s[1] + 0.62, "focus the address bar before typing")
    cue("swipe-medium-soft", s[1] + 2.08, "page scrolls")
    cue("data-progress-short", s[1] + 1.05, "loading progress begins")
    cue("digital-process-subtle", s[1] + 1.12, "server waits for response")
    cue("digital-glitch-subtle", s[1] + 3.48, "connection starts to stutter")
    cue("digital-signal-drop", s[1] + 3.56, "connection drops")
    cue("notification-error-soft", s[1] + 3.72, "timeout warning appears")

    # 03 — Dashboard: interface controls, metrics and chart draw-in.
    cue("whoosh-medium-soft", s[2] + 0.48, "dashboard arrives")
    cue("tone-step-1", s[2] + 1.15, "CPU metric appears")
    cue("tone-step-2", s[2] + 1.28, "RAM metric appears")
    cue("tone-step-3", s[2] + 1.41, "server status appears")
    cue("data-chart-reveal", s[2] + 1.55, "performance chart appears")
    cue("data-bar-grow", s[2] + 2.03, "chart bars reach their values")
    cue("notification-success-soft", s[2] + 2.62, "healthy server status")

    # 04 — Server hardware: power-up plus light, mechanical status sounds.
    cue("digital-power-up", s[3] + 0.20, "server racks power up")
    cue("whoosh-medium-soft", s[3] + 0.39, "camera moves across the racks")
    for offset in (1.36, 1.56, 1.76, 1.96):
        cue("mechanical-switch-light", s[3] + offset, "server activity LED")

    # 05 — Network: four ascending node arrivals, then data flows.
    cue("whoosh-medium-soft", s[4] + 0.18, "network scene enters")
    cue("tone-step-1", s[4] + 0.24, "web node appears")
    cue("tone-step-2", s[4] + 0.41, "VPS node appears")
    cue("tone-step-3", s[4] + 0.58, "database node appears")
    cue("tone-step-4", s[4] + 0.75, "SSL node appears")
    cue("digital-process-subtle", s[4] + 0.70, "connections transmit data")
    cue("swish-medium", s[4] + 1.10, "network lines complete")

    # 06 — Security: shield, controls, confirmations.
    cue("whoosh-medium-soft", s[5] + 0.66, "security shield appears")
    cue("shimmer-short-soft", s[5] + 1.24, "shield highlight")
    for offset in (1.12, 1.26, 1.40, 1.54):
        cue("click-tap-medium", s[5] + offset, "security control activates")
    cue("notification-success-soft", s[5] + 1.92, "security checklist complete")

    # 07 — Brand reveal: one warm signature and a discreet CTA interaction.
    cue("sting-warm-short", s[6] + 0.35, "cloudservicegm logo reveal")
    cue("pop-medium-in", s[6] + 1.80, "closing CTA lands")
    cue("shimmer-short-soft", s[6] + 1.92, "brand highlight")
    cue("click-tap-medium", s[6] + 2.05, "CTA button")

    # Emphasise only selected phrase transitions, never every word.
    occupied = [event["moment"] for event in events]
    accent_ids = ("pop-small-in", "swish-medium", "impact-light-soft")
    accents_added = 0
    for index, group in enumerate(groups):
        if index % 5 != 2:
            continue
        moment = float(group[0]["start"]) + 0.02
        if moment >= duration:
            continue
        if any(abs(moment - existing) < 0.42 for existing in occupied):
            continue
        sound_id = accent_ids[accents_added % len(accent_ids)]
        cue(sound_id, moment, "selected kinetic phrase accent", gain_db=-1.5)
        occupied.append(moment)
        accents_added += 1

    events.sort(key=lambda item: item["moment"])
    return events


def build_sound_effects(duration, words, groups, assets):
    """Create a synced SFX-only mix. No continuous music bed."""
    downloaded = download_sfx_assets(assets)
    events = sound_effect_schedule(duration, groups)
    if not events:
        raise RuntimeError("No se generaron eventos sonoros")

    # Merge speech intervals for automatic level control under narration.
    speech = []
    for word in words:
        start = max(0.0, float(word["start"]) - 0.10)
        end = min(duration, float(word["end"]) + 0.16)
        if end <= start:
            continue
        if speech and start <= speech[-1][1] + 0.06:
            speech[-1] = (speech[-1][0], max(speech[-1][1], end))
        else:
            speech.append((start, end))

    ffmpeg = ["ffmpeg", "-y", "-loglevel", "error"]
    for event in events:
        ffmpeg.extend(["-i", str(downloaded[event["id"]]["path"])])

    filters = []
    labels = []
    for index, event in enumerate(events):
        item = downloaded[event["id"]]["metadata"]
        sync_at = float(item.get("sync", {}).get("at", 0.0))
        start_at = event["moment"] - sync_at
        trim_start = max(0.0, -start_at)
        delay_ms = max(0, int(round(start_at * 1000)))

        timing = item.get("timing", {})
        body_start = max(0.0, float(timing.get("onset", 0.0)) - trim_start) + delay_ms / 1000.0
        body_end = max(body_start, float(timing.get("body_end", item.get("duration", 0.2)))-trim_start) + delay_ms / 1000.0
        overlaps_voice = any(
            body_start < speech_end and body_end > speech_start
            for speech_start, speech_end in speech
        )
        gain_db = event["gain_db"]
        if overlaps_voice:
            gain_db += float(item.get("under_voiceover_db", -2.0))

        filters.append(
            f"[{index}:a]aresample=44100,"
            f"atrim=start={trim_start:.4f},asetpts=PTS-STARTPTS,"
            f"volume={gain_db:.2f}dB,"
            f"adelay={delay_ms}:all=1[s{index}]"
        )
        labels.append(f"[s{index}]")

        event["file_start"] = round(start_at, 3)
        event["sync_at"] = sync_at
        event["gain_db_applied"] = round(gain_db, 2)
        event["over_voice"] = overlaps_voice
        event["description"] = item.get("description", "")

    filters.append(
        "".join(labels)
        + f"amix=inputs={len(events)}:duration=longest:normalize=0,"
        + f"alimiter=limit=0.88,apad=pad_dur={duration:.3f},"
        + f"atrim=duration={duration:.3f}[out]"
    )
    sfx_path = Path(assets) / "scene-sfx.wav"
    ffmpeg.extend([
        "-filter_complex", ";".join(filters),
        "-map", "[out]", "-ar", "44100", "-ac", "2",
        "-c:a", "pcm_s16le", str(sfx_path)
    ])
    subprocess.run(ffmpeg, check=True)

    manifest = {
        "background_music": False,
        "source": "Wyzowl SFX Kit",
        "source_url": "https://github.com/wyzowl/sfx-kit",
        "source_commit": SFX_SOURCE_COMMIT,
        "license": "CC0-1.0",
        "attribution_required": False,
        "event_count": len(events),
        "events": events
    }
    (Path(assets) / "sound-design.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(
        f"Diseño sonoro creado: {len(events)} efectos reales sincronizados, "
        "sin música de fondo ni efectos por palabra."
    )
    return sfx_path


def mix_voice_and_effects(voice_path, sfx_path, output_path):
    """Keep the original voice upfront and layer the effects underneath."""
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(voice_path),
        "-i", str(sfx_path),
        "-filter_complex",
        "[0:a]aresample=44100,volume=1.0[voice];"
        "[1:a]aresample=44100,volume=1.0[sfx];"
        "[voice][sfx]amix=inputs=2:duration=first:dropout_transition=0:normalize=0,"
        "acompressor=threshold=0.10:ratio=1.35:attack=18:release=220:makeup=1,"
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

    # Sound-only design: no background music, just scene- and action-synchronised SFX.
    sfx_path = build_sound_effects(duration, words, groups, assets)
    mixed_audio = assets / "narration.wav"
    mix_voice_and_effects(args.audio, sfx_path, mixed_audio)

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
