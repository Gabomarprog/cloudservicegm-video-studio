#!/usr/bin/env python3
"""Build one hand-authored manual composition package into HyperFrames HTML."""
from __future__ import annotations
import argparse
import html
import importlib.util
import re
from pathlib import Path

from build_video import (
    get_duration, load_words, group_words, make_caption,
    build_sound_effects, mix_voice_and_effects, SFX_IDS,
)

ROOT = Path(__file__).resolve().parent
BASE_TEMPLATE = ROOT / "manual_compositions" / "base.template.html"

# Captions are deliberately restrained lower-thirds. The visual composition
# owns the centre of the frame; subtitles must never compete with its objects.
CAPTION_CSS = r"""
.kinetic-clip.manual-caption{
  position:absolute;z-index:80;left:0;right:0;top:auto;bottom:158px;height:178px;
  display:flex;align-items:center;justify-content:center;
  padding:0 82px;pointer-events:none;perspective:1200px;
}
.kinetic-clip.manual-caption .type-wrap{
  width:100%;max-width:920px;min-height:82px;padding:12px 22px;
  display:flex;align-items:center;justify-content:center;
  border-radius:17px;background:linear-gradient(110deg,rgba(4,12,21,.88),rgba(7,19,29,.78));
  border:1px solid rgba(114,235,208,.24);
  box-shadow:0 12px 36px rgba(0,0,0,.34),inset 0 1px 0 rgba(255,255,255,.055);
  backdrop-filter:blur(8px);
}
.kinetic-clip.manual-caption .headline{
  width:100%;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;
  gap:.12em .28em;text-align:center;max-height:150px;overflow:hidden;
  font:800 clamp(42px,5.1vw,58px)/1.06 Arial,sans-serif !important;
  letter-spacing:-1.2px;text-transform:uppercase;color:#f7fbff;
}
.kinetic-clip.manual-caption .word{display:inline-flex;white-space:nowrap}
.kinetic-clip.manual-caption .char{display:inline-block;will-change:transform,opacity}
.kinetic-clip.manual-caption .accent-word{color:#72efcf;text-shadow:0 0 18px rgba(76,225,190,.20)}
"""

def load_design(package_dir: Path):
    source = package_dir / "design.py"
    if not source.is_file():
        raise RuntimeError(f"El paquete '{package_dir.name}' no contiene design.py.")
    spec = importlib.util.spec_from_file_location("manual_design_" + package_dir.name, source)
    if spec is None or spec.loader is None:
        raise RuntimeError("No se pudo cargar el módulo de diseño manual.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not callable(getattr(module, "build_design", None)):
        raise RuntimeError("design.py debe implementar build_design(duration, words, groups, title).")
    return module

def validate_design(design, duration):
    if not isinstance(design, dict):
        raise RuntimeError("build_design debe devolver un diccionario.")
    css = design.get("css")
    scenes = design.get("scenes")
    events = design.get("sfx_events")
    if not isinstance(css, str) or not css.strip():
        raise RuntimeError("El diseño necesita CSS propio.")
    if not isinstance(scenes, list) or not 3 <= len(scenes) <= 10:
        raise RuntimeError("El diseño debe incluir entre 3 y 10 escenas.")
    if not isinstance(events, list) or len(events) < len(scenes):
        raise RuntimeError("Cada escena necesita al menos un efecto de sonido sincronizado.")

    previous_end = 0.0
    html_parts = []
    animation_parts = []
    for index, scene in enumerate(scenes):
        if not isinstance(scene, dict):
            raise RuntimeError(f"La escena {index + 1} no es válida.")
        start = float(scene.get("start", -1))
        end = float(scene.get("end", -1))
        if start < 0 or end <= start or end > duration + 0.05:
            raise RuntimeError(f"Los tiempos de la escena {index + 1} no son válidos.")
        if index == 0 and start > 0.05:
            raise RuntimeError("La primera escena debe comenzar al inicio del audio.")
        if index and start < previous_end - 0.02:
            raise RuntimeError(f"Las escenas se solapan en la escena {index + 1}.")
        if index and start - previous_end > 0.55:
            raise RuntimeError(f"Hay un hueco demasiado largo antes de la escena {index + 1}.")
        previous_end = end

        visual = scene.get("markup")
        animation = scene.get("animation")
        if not isinstance(visual, str) or not visual.strip() or len(visual) > 100000:
            raise RuntimeError(f"La escena {index + 1} no contiene un objeto visual HTML/SVG.")
        if not isinstance(animation, str) or not animation.strip() or len(animation) > 30000:
            raise RuntimeError(f"La escena {index + 1} necesita animación GSAP propia.")

        scene_id = f"manual-scene-{index}"
        label = html.escape(str(scene.get("label") or f"ESCENA {index + 1}")[:60])
        headline = html.escape(str(scene.get("headline") or "")[:100])
        detail = html.escape(str(scene.get("detail") or "")[:180])
        html_parts.append(
            f'<section class="manual-scene" id="{scene_id}" data-start="{start:.3f}" data-duration="{end-start:.3f}">'
            f'<div class="manual-scene-kicker">{label}</div>'
            f'<div class="manual-scene-headline">{headline}</div>'
            f'<div class="manual-scene-detail">{detail}</div>'
            f'<div class="manual-scene-inner">{visual}</div>'
            f'<div class="manual-scene-index">{index+1:02d} / {len(scenes):02d}</div>'
            f'</section>'
        )
        animation_parts.append(
            f'tl.set("#{scene_id}",{{autoAlpha:1,scale:1}},{start:.3f});' + animation
        )
        if index < len(scenes) - 1:
            next_start = float(scenes[index + 1].get("start", end))
            animation_parts.append(
                f'tl.to("#{scene_id}",{{autoAlpha:0,scale:.975,duration:.34,ease:"power2.in"}},{max(start,next_start-.22):.3f});'
            )

    if previous_end < duration - 0.55:
        raise RuntimeError("El diseño termina demasiado antes de que termine la narración.")

    checked_events = []
    for item in events:
        if not isinstance(item, dict):
            raise RuntimeError("Hay un efecto de sonido con formato incorrecto.")
        sound_id = str(item.get("id", ""))
        moment = float(item.get("moment", -1))
        gain = float(item.get("gain_db", -2))
        if sound_id not in SFX_IDS:
            raise RuntimeError(f"Efecto no disponible en la biblioteca CC0: {sound_id}")
        if moment < 0 or moment >= duration or gain < -18 or gain > 6:
            raise RuntimeError(f"Tiempo o volumen no válido para el efecto {sound_id}.")
        checked_events.append({
            "id": sound_id,
            "moment": round(moment, 3),
            "label": str(item.get("label") or sound_id)[:100],
            "gain_db": gain,
        })

    return css, "\n".join(html_parts), "\n".join(animation_parts), checked_events

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--composition", required=True)
    parser.add_argument("--transcript", required=True)
    parser.add_argument("--audio", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--assets", required=True)
    parser.add_argument("--title", required=True)
    args = parser.parse_args()

    if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{1,48}", args.composition):
        raise RuntimeError("ID de composición no válido.")
    package_dir = ROOT / "manual_compositions" / args.composition
    if not package_dir.is_dir():
        raise RuntimeError(f"No existe el diseño manual '{args.composition}'.")

    duration = get_duration(args.audio)
    words = load_words(args.transcript, canonicalize=False)
    if not words:
        raise RuntimeError("La transcripción aprobada no contiene palabras.")
    groups = group_words(words)

    module = load_design(package_dir)
    design = module.build_design(duration, words, groups, args.title)
    css, scene_html, scene_anims, events = validate_design(design, duration)

    captions = []
    caption_anims = []
    for index, group in enumerate(groups):
        start = group[0]["start"]
        next_start = groups[index + 1][0]["start"] if index + 1 < len(groups) else duration
        end = min(duration, group[-1]["end"] + 0.10, max(start + 0.20, next_start - 0.02))
        markup, animation = make_caption(group, index, start, end, duration, dynamic=True)
        markup = markup.replace("dynamic-caption", "manual-caption")
        captions.append(markup)
        caption_anims.append(animation)

    assets = Path(args.assets)
    assets.mkdir(parents=True, exist_ok=True)
    sfx_path = build_sound_effects(
        duration, words, groups, assets, events_override=events
    )
    mix_voice_and_effects(args.audio, sfx_path, assets / "narration.wav")

    template = BASE_TEMPLATE.read_text(encoding="utf-8")
    replacements = {
        "{{DURATION}}": f"{duration:.3f}",
        "{{DESIGN_CSS}}": css,
        "{{SCENES}}": scene_html,
        "{{SCENE_ANIMS}}": scene_anims,
        "{{CAPTIONS}}": "\n".join(captions),
        "{{CAPTION_ANIMS}}": "\n".join(caption_anims),
        "{{CAPTION_CSS}}": CAPTION_CSS,
    }
    for key, value in replacements.items():
        template = template.replace(key, value)
    unresolved = re.findall(r"\{\{[A-Z_]+\}\}", template)
    if unresolved:
        raise RuntimeError("Marcadores sin sustituir: " + ", ".join(unresolved))

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(template, encoding="utf-8")
    print(
        f"Diseño manual '{args.composition}': {len(design['scenes'])} escenas, "
        f"{len(words)} palabras, {duration:.1f}s."
    )

if __name__ == "__main__":
    main()
