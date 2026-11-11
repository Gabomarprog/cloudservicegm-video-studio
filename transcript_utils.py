#!/usr/bin/env python3
"""Word-level transcript extraction and safe timestamp-preserving edits."""
from __future__ import annotations
import difflib
import json
import re
from pathlib import Path

def flatten_transcript(data):
    if isinstance(data, dict):
        source = data.get("words") or data.get("segments") or data.get("transcription") or []
    else:
        source = data
    result = []
    if not isinstance(source, list):
        return result
    for item in source:
        if not isinstance(item, dict):
            continue
        text = str(item.get("text") or item.get("word") or "").strip()
        if not text:
            continue
        try:
            start = float(item.get("start", item.get("start_time", 0)))
            end = float(item.get("end", item.get("end_time", start + .35)))
        except (TypeError, ValueError):
            continue
        start = max(0.0, start)
        end = max(start + .12, end)
        tokens = text.split()
        span = max(.12, end-start)
        if len(tokens) == 1:
            result.append({"text": tokens[0], "start": start, "end": end})
        else:
            step = span / len(tokens)
            for i, token in enumerate(tokens):
                result.append({
                    "text": token,
                    "start": start + i*step,
                    "end": min(end, start + (i+1)*step)
                })
    return sorted(result, key=lambda x: x["start"])

def transcript_text(data):
    return " ".join(w["text"] for w in flatten_transcript(data))

def align_edited_text(edited, original_data, duration):
    tokens = re.findall(r"\S+", str(edited or "").strip())
    if not tokens:
        raise ValueError("La transcripción corregida no puede quedar vacía.")
    old = flatten_transcript(original_data)
    if not old:
        count = len(tokens)
        span = max(float(duration), count*.12)
        return [
            {"text": token, "start": i*span/count, "end": (i+1)*span/count}
            for i, token in enumerate(tokens)
        ]

    def norm(value):
        return re.sub(r"^[^\wÁÉÍÓÚÜÑáéíóúüñ]+|[^\wÁÉÍÓÚÜÑáéíóúüñ]+$", "", value.casefold())

    old_norm = [norm(x["text"]) for x in old]
    new_norm = [norm(x) for x in tokens]
    matcher = difflib.SequenceMatcher(a=old_norm, b=new_norm, autojunk=False)
    aligned = [None] * len(tokens)
    anchors = []
    for block in matcher.get_matching_blocks():
        for offset in range(block.size):
            oi, ni = block.a+offset, block.b+offset
            aligned[ni] = {
                "text": tokens[ni],
                "start": old[oi]["start"],
                "end": old[oi]["end"]
            }
            anchors.append(ni)

    # Fill edited/inserted words between preserved timestamp anchors.
    boundaries = [-1] + anchors + [len(tokens)]
    total_duration = max(float(duration), old[-1]["end"], .5)
    for left_idx, right_idx in zip(boundaries, boundaries[1:]):
        gap_start, gap_end = left_idx+1, right_idx
        if gap_start >= gap_end:
            continue
        left_time = aligned[left_idx]["end"] if left_idx >= 0 else 0.0
        right_time = aligned[right_idx]["start"] if right_idx < len(tokens) else total_duration
        if right_time <= left_time:
            right_time = left_time + (gap_end-gap_start)*.14
        weights = [max(2, min(16, len(tokens[i].strip(".,;:!?¡¿()[]{}"))) ) for i in range(gap_start,gap_end)]
        span = right_time-left_time
        unit = span / sum(weights)
        cursor = left_time
        for i, weight in zip(range(gap_start,gap_end), weights):
            end = cursor + unit*weight
            aligned[i] = {"text":tokens[i],"start":cursor,"end":max(cursor+.08,end)}
            cursor = end

    # Clamp monotonic times, preserving original word anchors whenever possible.
    final=[]
    previous=0.0
    for item in aligned:
        start=max(previous, min(total_duration, float(item["start"])))
        end=max(start+.06, min(total_duration, float(item["end"])))
        if end <= start:
            end=start+.08
        final.append({"text":item["text"],"start":round(start,4),"end":round(end,4)})
        previous=start
    return final

def write_transcript(words, path):
    Path(path).write_text(json.dumps(words, ensure_ascii=False, indent=2), encoding="utf-8")
