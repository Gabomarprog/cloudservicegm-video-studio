#!/usr/bin/env python3
"""Safe, data-driven HTML scene library for cloudservicegm motion graphics."""
from __future__ import annotations
import html
import re

ALLOWED_VISUALS = {
    "typography", "browser", "certificate", "network", "shield", "server",
    "dashboard", "database", "terminal", "phone", "comparison", "process",
    "chart", "timeline", "webpage", "cta"
}

def safe_text(value, limit=100):
    value = re.sub(r"\s+", " ", str(value or "")).strip()
    return html.escape(value[:limit])

def normalize_scene(scene, index):
    visual = str(scene.get("visual", "process")).lower()
    if visual not in ALLOWED_VISUALS:
        visual = "process"
    chips = scene.get("chips", [])
    if not isinstance(chips, list):
        chips = []
    chips = [safe_text(x, 28) for x in chips[:4] if str(x).strip()]
    return {
        "visual": visual,
        "label": safe_text(scene.get("label") or f"ESCENA {index + 1}", 48),
        "headline": safe_text(scene.get("headline") or "Una idea clara", 88),
        "detail": safe_text(scene.get("detail") or "", 180),
        "chips": chips,
        "stat": safe_text(scene.get("stat") or "", 24),
    }

def _chips(scene):
    values = scene["chips"] or ["Información", "Control", "Confianza"]
    return "".join(f'<span class="chip">{x}</span>' for x in values)

def render_visual(scene, index):
    v = scene["visual"]
    chips = _chips(scene)
    stat = scene["stat"] or "OK"
    if v == "browser" or v == "webpage":
        return f'''<div class="visual v-browser"><div class="browser-top"><i></i><i></i><i></i><b>https://tu-proyecto.com</b></div><div class="browser-body"><div class="browser-side"></div><div class="browser-main"><div class="skeleton wide"></div><div class="skeleton"></div><div class="skeleton short"></div><div class="browser-cards"><i></i><i></i><i></i></div><div class="browser-button">{stat}</div></div></div></div>'''
    if v == "certificate":
        return f'''<div class="visual v-certificate"><div class="cert-card"><div class="cert-top"><b>SECURE CERTIFICATE</b><span>✦</span></div><div class="cert-seal">✓</div><div class="cert-lines"><i></i><i></i><i></i></div><div class="cert-domain">HTTPS · SSL/TLS</div><div class="cert-stamp">VERIFIED</div></div><div class="orbit orbit-a"></div><div class="orbit orbit-b"></div></div>'''
    if v == "network":
        return f'''<div class="visual v-network"><svg viewBox="0 0 700 420"><path d="M110 205 L350 85 L590 205 L350 340 Z M110 205 L590 205 M350 85 L350 340" /></svg><i class="node n1">WEB</i><i class="node n2">API</i><i class="node n3">DATA</i><i class="node n4">SSL</i></div>'''
    if v == "shield":
        return f'''<div class="visual v-shield"><div class="shield-orbit"></div><svg viewBox="0 0 360 410"><path d="M180 18 L320 72 V185 C320 282 260 350 180 392 C100 350 40 282 40 185 V72 Z"/><path class="shield-check" d="M105 203 L158 255 L260 145"/></svg><div class="shield-tags">{chips}</div></div>'''
    if v == "server":
        return f'''<div class="visual v-server"><div class="server-rack"><i></i><i></i><i></i><i></i></div><div class="server-rack"><i></i><i></i><i></i><i></i></div><div class="server-rack"><i></i><i></i><i></i><i></i></div><div class="server-glow"></div></div>'''
    if v == "dashboard":
        return f'''<div class="visual v-dashboard"><div class="dash-card"><small>RENDIMIENTO</small><b>{stat}</b><i></i></div><div class="dash-card"><small>ESTADO</small><b>ACTIVO</b><i></i></div><div class="dash-card"><small>RECURSOS</small><b>OPTIMIZADOS</b><i></i></div><div class="dash-chart">{''.join(f'<i style="--h:{h}%"></i>' for h in [35,56,44,78,63,91,70,84,99])}</div></div>'''
    if v == "database":
        return f'''<div class="visual v-database"><div class="db-cylinder"><i></i><i></i><i></i></div><div class="db-flow"><span>01</span><span>02</span><span>03</span></div></div>'''
    if v == "terminal":
        return f'''<div class="visual v-terminal"><div class="terminal-head"><i></i><i></i><i></i><b>terminal — bash</b></div><div class="terminal-lines"><p><em>$</em> systemctl status service</p><p class="ok">● active (running)</p><p><em>$</em> secure connection</p><p class="ok">✓ configuration verified</p><p><em>$</em> {stat.lower()}</p></div></div>'''
    if v == "phone":
        return f'''<div class="visual v-phone"><div class="phone-shell"><div class="phone-notch"></div><div class="phone-screen"><div class="phone-url">🔒 https://web.app</div><div class="phone-hero"></div><div class="phone-copy"></div><div class="phone-copy small"></div><div class="phone-mini-cards"><i></i><i></i><i></i></div><div class="phone-ok">✓ CONEXIÓN SEGURA</div></div></div></div>'''
    if v == "comparison":
        return f'''<div class="visual v-comparison"><div class="compare-card old"><b>ANTES</b><strong>!</strong><span>Sin optimizar</span></div><div class="compare-arrow">→</div><div class="compare-card new"><b>DESPUÉS</b><strong>✓</strong><span>Preparado</span></div></div>'''
    if v == "chart":
        return f'''<div class="visual v-chart"><div class="chart-value">{stat}</div><div class="chart-bars">{''.join(f'<i style="--h:{h}%"></i>' for h in [25,42,35,58,47,78,66,92])}</div><div class="chart-base"></div></div>'''
    if v == "timeline":
        return f'''<div class="visual v-timeline"><div class="time-line"></div><div class="time-step"><i>01</i><b>PREPARAR</b></div><div class="time-step"><i>02</i><b>CONFIGURAR</b></div><div class="time-step"><i>03</i><b>VERIFICAR</b></div><div class="time-step"><i>04</i><b>PROTEGER</b></div></div>'''
    if v == "cta":
        return f'''<div class="visual v-cta"><div class="cta-emblem">C</div><div class="cta-message">CLOUDSERVICEGM</div><div class="cta-sub">VPS · CLOUD · WEB</div><div class="cta-button">HABLEMOS DE TU PROYECTO ↗</div></div>'''
    if v == "typography":
        return f'''<div class="visual v-typography"><span>{stat or "IDEA"}</span><div class="type-orbit"></div></div>'''
    if v == "process":
        return f'''<div class="visual v-process"><div class="process-card"><i>01</i><b>{scene["chips"][0] if scene["chips"] else "ANALIZAR"}</b></div><div class="process-card"><i>02</i><b>{scene["chips"][1] if len(scene["chips"])>1 else "CONFIGURAR"}</b></div><div class="process-card"><i>03</i><b>{scene["chips"][2] if len(scene["chips"])>2 else "VERIFICAR"}</b></div></div>'''
    return render_visual({**scene, "visual": "process"}, index)

def render_scenes(storyboard, duration):
    raw = storyboard.get("scenes", [])
    scenes = [normalize_scene(s, i) for i, s in enumerate(raw[:8]) if isinstance(s, dict)]
    if len(scenes) < 3:
        raise ValueError("El director debe proponer al menos 3 escenas visuales.")
    if scenes[-1]["visual"] != "cta":
        scenes.append(normalize_scene({
            "visual": "cta", "label": "CIERRE", "headline": "Tu proyecto merece una mejor infraestructura",
            "detail": "Conoce más soluciones en cloudservicegm."
        }, len(scenes)))
    count = len(scenes)
    starts = [duration * i / count for i in range(count)]
    html_parts, anims = [], []
    palettes = ["red", "dark", "cream", "blue", "mint", "dark", "cream", "red"]
    for i, scene in enumerate(scenes):
        palette = palettes[i % len(palettes)]
        html_parts.append(
            f'<section class="scene scene-{palette}" id="scene-{i}" data-visual="{scene["visual"]}">'
            f'<div class="scene-kicker">{scene["label"]}</div>'
            f'<div class="scene-heading">{scene["headline"]}</div>'
            f'<div class="scene-detail">{scene["detail"]}</div>'
            f'{render_visual(scene, i)}'
            f'<div class="scene-index">{i+1:02d} / {count:02d}</div>'
            f'</section>'
        )
        at = starts[i]
        animation = (
            f'tl.fromTo("#scene-{i} .scene-kicker",{{y:28,opacity:0}},{{y:0,opacity:1,duration:.42,ease:"power3.out"}},{at:.3f});'
            f'tl.fromTo("#scene-{i} .scene-heading",{{y:70,rotationX:-16,opacity:0,scale:.92}},{{y:0,rotationX:0,opacity:1,scale:1,duration:.68,ease:"back.out(1.25)"}},{at+.12:.3f});'
            f'tl.fromTo("#scene-{i} .scene-detail",{{y:30,opacity:0}},{{y:0,opacity:1,duration:.5,ease:"power2.out"}},{at+.32:.3f});'
            f'tl.fromTo("#scene-{i} .visual",{{y:100,scale:.78,rotationZ:{-2 if i%2 else 2},opacity:0}},{{y:0,scale:1,rotationZ:0,opacity:1,duration:.8,ease:"expo.out"}},{at+.42:.3f});'
            f'tl.fromTo("#scene-{i} .visual-item",{{scale:.6,opacity:0}},{{scale:1,opacity:1,duration:.55,stagger:.12,ease:"back.out(1.4)"}},{at+.9:.3f});'
        )
        if i < count-1:
            animation += f'tl.to("#scene-{i}",{{autoAlpha:0,scale:.96,duration:.34,ease:"power2.in"}},{starts[i+1]-.20:.3f});'
        else:
            animation += f'tl.fromTo("#scene-{i} .cta-button",{{scaleX:.5,opacity:0}},{{scaleX:1,opacity:1,duration:.55,ease:"expo.out"}},{at+1.1:.3f});'
        anims.append(animation)
    return "\n".join(html_parts), "\n".join(anims), starts, [s["visual"] for s in scenes]
