#!/usr/bin/env python3
import argparse, json, html, shutil, subprocess
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
    words = []
    for item in data:
        if not isinstance(item, dict):
            continue
        text = str(item.get("text", "")).strip()
        try:
            start = float(item.get("start", item.get("start_time", 0)))
            end = float(item.get("end", item.get("end_time", start + 0.35)))
        except (TypeError, ValueError):
            continue
        if text:
            words.append({"text": text, "start": max(0, start), "end": max(start + 0.12, end)})
    return sorted(words, key=lambda x: x["start"])

def group_words(words, max_words=3):
    groups, current = [], []
    for word in words:
        current.append(word)
        if len(current) >= max_words or word["text"].endswith((".", "!", "?", ",", ";", ":")):
            groups.append(current)
            current = []
    if current:
        groups.append(current)
    return groups


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--transcript", required=True)
    p.add_argument("--audio", required=True)
    p.add_argument("--template", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--assets", required=True)
    p.add_argument("--title", required=True)
    a = p.parse_args()

    duration = get_duration(a.audio)
    t1, t2, t3, t4 = duration*.23, duration*.43, duration*.64, duration*.80
    words = load_words(a.transcript)

    captions, anims = [], []
    groups = group_words(words, max_words=3)
    if words:
        for i, group in enumerate(groups):
            start = group[0]["start"]
            end = min(duration, group[-1]["end"] + .22)
            if end <= start:
                continue
            phrase = " ".join(f'<span class="kinetic-word">{html.escape(w["text"])}</span>' for w in group)
            captions.append(
                f'<div class="caption clip" id="cap-{i}" data-start="{start:.3f}" '
                f'data-duration="{end-start:.3f}" data-track-index="10">{phrase}</div>'
            )
            anims.append(
                f'tl.fromTo("#cap-{i} .kinetic-word",{{opacity:0,y:150,scale:.38,rotationX:-55,filter:"blur(24px)"}},'
                f'{{opacity:1,y:0,scale:1,rotationX:0,filter:"blur(0px)",duration:.42,stagger:.065,ease:"back.out(1.8)"}},{start:.3f});'
                f'tl.to("#cap-{i} .kinetic-word",{{opacity:0,y:-95,scale:1.22,filter:"blur(15px)",duration:.20,stagger:.025,ease:"power2.in"}},'
                f'{max(start, end-.22):.3f});'
            )
        pass  # Keep narration clean; no repetitive per-word sound effects.
    caption_html = "\n".join(captions)
    caption_anims = "\n".join(anims)

    template = Path(a.template).read_text(encoding="utf-8")
    replacements = {
        "{{TITLE}}": html.escape(a.title),
        "{{DURATION}}": f"{duration:.3f}",
        "{{T1}}": f"{t1:.3f}",
        "{{T2}}": f"{t2:.3f}",
        "{{T3}}": f"{t3:.3f}",
        "{{T4}}": f"{t4:.3f}",
        "{{DASH_DURATION}}": f"{(t2-t1):.3f}",
        "{{TERM_DURATION}}": f"{(t3-t2):.3f}",
        "{{DIAG_DURATION}}": f"{(t4-t3):.3f}",
        "{{CTA_DURATION}}": f"{max(0.5, duration-t4):.3f}",
        "{{CAPTIONS}}": caption_html,
        "{{CAPTION_ANIMS}}": caption_anims,
    }
    for key, value in replacements.items():
        template = template.replace(key, value)

    assets = Path(a.assets)
    assets.mkdir(parents=True, exist_ok=True)
    shutil.copy2(a.audio, assets / "narration.wav")
    out = Path(a.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(template, encoding="utf-8")
    print(f"Composición creada: {out}")
    print(f"Duración de audio: {duration:.2f}s | Subtítulos: {len(captions)}")

if __name__ == "__main__":
    main()
