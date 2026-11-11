"""Diseño editorial cinemático: seguridad SSL/TLS para páginas web."""
from __future__ import annotations
import html
import math

def build_design(duration, words, groups, title):
    # Seven distinct visual beats. The actual imported narration controls timing.
    fractions = [0.00, 0.14, 0.29, 0.44, 0.59, 0.74, 0.88, 1.00]
    labels = [
        ("EL RIESGO", "¿TU WEB INSPIRA CONFIANZA?", "Una conexión insegura puede hacer que un visitante se marche"),
        ("LA DIFERENCIA", "HTTP VS. HTTPS", "La conexión cifrada protege el intercambio de información"),
        ("EL CERTIFICADO", "IDENTIDAD VERIFICADA", "El certificado ayuda a autenticar el sitio y habilitar TLS"),
        ("DATOS PROTEGIDOS", "CIFRADO EN TRÁNSITO", "Evita que los datos viajen expuestos entre el navegador y el servidor"),
        ("CONFIANZA", "FORMULARIOS Y PAGOS", "Protege credenciales, formularios y sesiones durante el transporte"),
        ("VIGILANCIA", "NO BASTA CON INSTALARLO", "Renovación, dominio correcto y configuración actualizada"),
        ("RESULTADO", "TU WEB, BAJO HTTPS", "Seguridad, confianza y una experiencia profesional"),
    ]
    scenes = []
    for i, (kicker, headline, detail) in enumerate(labels):
        start = duration * fractions[i]
        end = duration * fractions[i+1]
        visual = _visual(i)
        animation = _animation(i, start, end)
        scenes.append({
            "start": round(start, 3), "end": round(end, 3),
            "label": kicker, "headline": headline, "detail": detail,
            "markup": visual, "animation": animation,
        })
    sfx = [
        ("whoosh-medium-soft", .25, -9),
        ("notification-error-soft", duration*.145, -8),
        ("digital-power-up", duration*.30, -10),
        ("digital-process-subtle", duration*.45, -11),
        ("click-tap-medium", duration*.60, -10),
        ("mechanical-switch-light", duration*.755, -9),
        ("notification-success-soft", duration*.90, -7),
        ("sting-warm-short", duration*.965, -12),
    ]
    events = [
        {"id": sound_id, "moment": round(moment, 3), "gain_db": gain, "label": sound_id}
        for sound_id, moment, gain in sfx if moment < duration
    ]
    return {
        "css": _css(),
        "scenes": scenes,
        "sfx_events": events,
    }

def _css():
    return r"""
    #root{background:radial-gradient(ellipse at 50% 42%,#122c43 0%,#08111e 53%,#050910 100%)}
    .manual-scene{background:radial-gradient(ellipse at 50% 50%,rgba(18,45,67,.42),transparent 65%)}
    .manual-scene-kicker{color:#69e5c9;text-shadow:0 0 24px #28bda566}
    .manual-scene-headline{color:#f4f8ff;text-shadow:0 8px 32px #000;letter-spacing:-2px}
    .manual-scene-detail{color:#b9cddd}
    .manual-scene-index{color:#6ee6cc}
    .ssl-art{position:absolute;left:0;right:0;top:450px;height:930px;display:flex;align-items:center;justify-content:center}
    .ssl-art svg{width:100%;height:100%;overflow:visible}
    .ssl-glow{filter:drop-shadow(0 0 26px #35e4be66)}
    .ssl-card{fill:#0c1b2a;stroke:#6ee6cc;stroke-width:3}
    .ssl-muted{fill:#a8c0d3;font:600 25px Arial}
    .ssl-bright{fill:#effffb;font:800 31px Arial}
    .ssl-green{fill:#6ee6cc}
    .ssl-red{fill:#ff6477}
    .ssl-stroke{fill:none;stroke:#6ee6cc;stroke-width:9;stroke-linecap:round;stroke-linejoin:round}
    .ssl-line{fill:none;stroke:#5be1c1;stroke-width:3;stroke-dasharray:12 14}
    .ssl-node{fill:#0b1927;stroke:#65e4c5;stroke-width:4}
    .ssl-chip{fill:#112b38;stroke:#3c897c;stroke-width:2}
    .ssl-orbit{fill:none;stroke:#397d7c;stroke-width:2;stroke-dasharray:8 13}
    .ssl-redline{fill:none;stroke:#ff6477;stroke-width:7;stroke-linecap:round}
    .ssl-white{fill:#f2fbff}
    .ssl-check{fill:none;stroke:#6ee6cc;stroke-width:13;stroke-linecap:round;stroke-linejoin:round}
    .ssl-scene-label{fill:#6ee6cc;font:800 21px Arial;letter-spacing:4px}
    .ssl-tiny{fill:#b9d0df;font:700 19px Arial}
    .ssl-metric{fill:#f2fbff;font:900 44px Arial}
    .ssl-bar{fill:#183a48}
    .ssl-bar-fill{fill:#65e4c5}
    .ssl-shield{fill:#102d3a;stroke:#6ee6cc;stroke-width:8;stroke-linejoin:round}
    .ssl-lock{fill:#0a1a28;stroke:#6ee6cc;stroke-width:8}
    .ssl-glass{fill:#102b3b;stroke:#73e7ce;stroke-width:5}
    .ssl-caption{fill:#effffc;font:800 24px Arial}
    """

def _visual(index):
    if index == 0:
        return r"""<div class="ssl-art"><svg viewBox="0 0 900 900" role="img" aria-label="Navegador con advertencia de conexión no segura">
        <defs><linearGradient id="risk" x1="0" x2="1"><stop stop-color="#ff536c"/><stop offset="1" stop-color="#ff9b66"/></linearGradient></defs>
        <g id="browser-risk" transform="translate(115 190)"><rect width="670" height="440" rx="28" fill="#101e2d" stroke="#ff7180" stroke-width="5"/><path d="M0 70H670" stroke="#34495b" stroke-width="4"/><circle cx="38" cy="35" r="10" fill="#ff6978"/><circle cx="72" cy="35" r="10" fill="#ffbf69"/><circle cx="106" cy="35" r="10" fill="#6ee6cc"/><rect x="155" y="17" width="465" height="38" rx="12" fill="#07111d"/><text x="180" y="43" class="ssl-tiny">http://tu-pagina.com</text><rect x="40" y="110" width="590" height="270" rx="18" fill="#0a1522"/><path d="M300 155L365 270H235Z" fill="url(#risk)"/><path d="M300 192V232M300 249V253" stroke="#07111d" stroke-width="11" stroke-linecap="round"/><text x="335" y="320" class="ssl-bright">Conexión no segura</text></g>
        <g id="risk-alert"><circle cx="700" cy="635" r="75" fill="#3b1824" stroke="#ff6978" stroke-width="6"/><path d="M700 590V650M700 677V681" stroke="#ff7a88" stroke-width="15" stroke-linecap="round"/></g>
        <path d="M100 710H800" stroke="#ff6578" stroke-width="3" stroke-dasharray="9 16" opacity=".7"/></svg></div>"""
    if index == 1:
        return r"""<div class="ssl-art"><svg viewBox="0 0 900 900" role="img" aria-label="Comparación de HTTP y HTTPS">
        <g id="http-card" transform="translate(65 220)"><rect width="350" height="390" rx="28" fill="#251927" stroke="#ff6978" stroke-width="4"/><text x="175" y="75" text-anchor="middle" class="ssl-red" font-size="47" font-weight="900">HTTP</text><path d="M95 145L255 280M255 145L95 280" class="ssl-redline"/><text x="175" y="340" text-anchor="middle" class="ssl-muted">Sin TLS</text></g>
        <g id="https-card" transform="translate(485 220)"><rect width="350" height="390" rx="28" fill="#102b2b" stroke="#6ee6cc" stroke-width="4"/><text x="175" y="75" text-anchor="middle" class="ssl-green" font-size="47" font-weight="900">HTTPS</text><path d="M115 215L160 265L250 165" class="ssl-check"/><text x="175" y="340" text-anchor="middle" class="ssl-muted">TLS activo</text></g>
        <g id="compare-arrow"><path d="M390 420H510M485 395L510 420L485 445" class="ssl-stroke"/></g><text x="450" y="730" text-anchor="middle" class="ssl-scene-label">CONEXIÓN CIFRADA</text></svg></div>"""
    if index == 2:
        return r"""<div class="ssl-art"><svg viewBox="0 0 900 900" role="img" aria-label="Certificado digital con sello de identidad">
        <g id="certificate" transform="translate(235 120)"><path d="M0 0H350L450 100V600H0Z" fill="#10283a" stroke="#6ee6cc" stroke-width="5"/><path d="M350 0V100H450" fill="#183d4b" stroke="#6ee6cc" stroke-width="4"/><text x="45" y="75" class="ssl-scene-label">CERTIFICADO</text><rect x="45" y="135" width="350" height="60" rx="12" class="ssl-chip"/><text x="65" y="174" class="ssl-bright">tu-dominio.com</text><path d="M45 245H385M45 295H345M45 345H365" stroke="#4b6b7e" stroke-width="9" stroke-linecap="round"/><circle cx="225" cy="465" r="82" fill="#153d43" stroke="#6ee6cc" stroke-width="6"/><path d="M182 465L210 495L270 427" class="ssl-check"/></g><g id="cert-seal"><circle cx="675" cy="650" r="100" fill="#102e35" stroke="#6ee6cc" stroke-width="5"/><path d="M635 650L665 680L720 615" class="ssl-check"/></g></svg></div>"""
    if index == 3:
        return r"""<div class="ssl-art"><svg viewBox="0 0 900 900" role="img" aria-label="Datos cifrados viajando por un túnel seguro">
        <g id="data-tunnel"><ellipse cx="450" cy="450" rx="355" ry="245" class="ssl-orbit"/><ellipse cx="450" cy="450" rx="275" ry="180" class="ssl-orbit"/><ellipse cx="450" cy="450" rx="190" ry="115" class="ssl-orbit"/><path d="M95 450H805" class="ssl-line"/></g>
        <g id="data-packets"><rect x="165" y="365" width="105" height="68" rx="14" class="ssl-chip"/><text x="217" y="410" text-anchor="middle" class="ssl-bright">101</text><rect x="630" y="500" width="105" height="68" rx="14" class="ssl-chip"/><text x="682" y="545" text-anchor="middle" class="ssl-bright">011</text><rect x="385" y="310" width="130" height="72" rx="14" class="ssl-chip"/><text x="450" y="356" text-anchor="middle" class="ssl-bright">X7#</text></g>
        <g id="data-shield" transform="translate(355 395)"><path d="M95 0L180 32V100Q180 190 95 235Q10 190 10 100V32Z" class="ssl-shield"/><path d="M55 110L85 140L140 78" class="ssl-check"/></g>
        <g id="encrypted-lock"><rect x="405" y="660" width="90" height="85" rx="14" class="ssl-lock"/><path d="M425 660V625A25 25 0 0 1 475 625V660" class="ssl-stroke"/></g></svg></div>"""
    if index == 4:
        return r"""<div class="ssl-art"><svg viewBox="0 0 900 900" role="img" aria-label="Formulario web y pago protegidos">
        <g id="secure-form" transform="translate(150 130)"><rect width="600" height="560" rx="30" fill="#102235" stroke="#5fe2c4" stroke-width="5"/><rect x="0" y="0" width="600" height="76" rx="25" fill="#17384a"/><circle cx="40" cy="38" r="9" fill="#6ee6cc"/><text x="78" y="49" class="ssl-bright">checkout seguro</text><text x="45" y="145" class="ssl-muted">Número de tarjeta</text><rect x="45" y="170" width="510" height="65" rx="12" class="ssl-chip"/><text x="70" y="213" class="ssl-bright">••••  ••••  ••••  4821</text><text x="45" y="295" class="ssl-muted">Datos personales</text><rect x="45" y="320" width="510" height="60" rx="12" fill="#0a1927" stroke="#385a6d" stroke-width="2"/><rect x="45" y="405" width="510" height="78" rx="16" fill="#125447"/><text x="300" y="454" text-anchor="middle" class="ssl-bright">PAGO PROTEGIDO</text></g>
        <g id="form-lock" transform="translate(640 630)"><circle r="85" fill="#0e302e" stroke="#6ee6cc" stroke-width="5"/><rect x="-34" y="-5" width="68" height="58" rx="10" class="ssl-lock"/><path d="M-22 -5V-27A22 22 0 0 1 22 -27V-5" class="ssl-stroke"/></g></svg></div>"""
    if index == 5:
        return r"""<div class="ssl-art"><svg viewBox="0 0 900 900" role="img" aria-label="Panel de control con renovación del certificado">
        <g id="ssl-dashboard" transform="translate(100 190)"><rect width="700" height="480" rx="28" fill="#0e2030" stroke="#4d7586" stroke-width="4"/><text x="45" y="70" class="ssl-scene-label">PANEL SSL / TLS</text><rect x="45" y="115" width="610" height="100" rx="18" class="ssl-chip"/><circle cx="100" cy="165" r="24" fill="#163e38" stroke="#6ee6cc" stroke-width="3"/><path d="M87 165L97 176L115 151" class="ssl-check" stroke-width="6"/><text x="150" y="157" class="ssl-bright">Certificado activo</text><text x="150" y="190" class="ssl-tiny">Dominio correcto</text><text x="45" y="285" class="ssl-muted">Renovación automática</text><rect x="45" y="310" width="610" height="22" rx="11" class="ssl-bar"/><rect id="renew-progress" x="45" y="310" width="465" height="22" rx="11" class="ssl-bar-fill"/><text x="45" y="390" class="ssl-tiny">Vigencia · cadena · redirección HTTPS</text><text x="45" y="435" class="ssl-green" font-size="23" font-weight="800">TODO BAJO CONTROL</text></g>
        <g id="renew-bell"><circle cx="720" cy="730" r="55" fill="#173e43" stroke="#6ee6cc" stroke-width="4"/><path d="M720 690V733M720 754V758" class="ssl-stroke"/></g></svg></div>"""
    return r"""<div class="ssl-art"><svg viewBox="0 0 900 900" role="img" aria-label="Sitio web protegido por un gran escudo">
        <g id="final-globe"><circle cx="450" cy="450" r="290" class="ssl-orbit"/><circle cx="450" cy="450" r="220" class="ssl-orbit"/><path d="M160 450H740M450 160V740" class="ssl-line"/></g>
        <g id="final-shield" transform="translate(285 195)"><path d="M165 0L310 55V190Q310 370 165 465Q20 370 20 190V55Z" class="ssl-shield ssl-glow"/><path d="M100 235L145 280L235 175" class="ssl-check"/></g>
        <g id="final-url"><rect x="230" y="735" width="440" height="70" rx="35" class="ssl-chip"/><circle cx="275" cy="770" r="12" fill="#6ee6cc"/><text x="310" y="779" class="ssl-bright">https://tu-web.com</text></g></svg></div>"""

def _animation(index, start, end):
    sid = f"#manual-scene-{index}"
    duration = max(.5, end-start)
    common = f'tl.set("{sid} .manual-scene-inner",{{autoAlpha:1}});'
    if index == 0:
        return common + f'tl.fromTo("{sid} #browser-risk",{{y:100,rotationX:18,scale:.82,autoAlpha:0}},{{y:0,rotationX:0,scale:1,autoAlpha:1,duration:1.0,ease:"back.out(1.4)"}},{start:.3f});tl.fromTo("{sid} #risk-alert",{{scale:0,rotation:-35}},{{scale:1,rotation:0,duration:.55,ease:"elastic.out(1,.55)"}},{start+duration*.48:.3f});tl.fromTo("{sid} .ssl-redline",{{scaleX:0}},{{scaleX:1,duration:.6,ease:"power3.out"}},{start+duration*.35:.3f});'
    if index == 1:
        return common + f'tl.fromTo("{sid} #http-card",{{x:-260,autoAlpha:0,rotation:-8}},{{x:0,autoAlpha:1,rotation:0,duration:.8,ease:"power3.out"}},{start:.3f});tl.fromTo("{sid} #https-card",{{x:260,autoAlpha:0,rotation:8}},{{x:0,autoAlpha:1,rotation:0,duration:.8,ease:"power3.out"}},{start+.18:.3f});tl.fromTo("{sid} #compare-arrow",{{scale:0,transformOrigin:"50% 50%"}},{{scale:1,duration:.5,ease:"back.out(2)"}},{start+duration*.55:.3f});'
    if index == 2:
        return common + f'tl.fromTo("{sid} #certificate",{{y:180,rotationY:25,autoAlpha:0}},{{y:0,rotationY:0,autoAlpha:1,duration:1,ease:"power3.out"}},{start:.3f});tl.fromTo("{sid} #cert-seal",{{scale:0,rotation:-90}},{{scale:1,rotation:0,duration:.8,ease:"elastic.out(1,.6)"}},{start+duration*.58:.3f});'
    if index == 3:
        return common + f'tl.fromTo("{sid} #data-tunnel",{{scale:.55,autoAlpha:0}},{{scale:1,autoAlpha:1,duration:1,ease:"power2.out"}},{start:.3f});tl.fromTo("{sid} #data-packets rect",{{x:-110,autoAlpha:0}},{{x:0,autoAlpha:1,duration:.75,stagger:.18,ease:"power2.out"}},{start+.3:.3f});tl.fromTo("{sid} #data-shield",{{scale:.35,rotation:-18,autoAlpha:0}},{{scale:1,rotation:0,autoAlpha:1,duration:.9,ease:"back.out(1.7)"}},{start+duration*.48:.3f});tl.fromTo("{sid} #encrypted-lock",{{y:80,autoAlpha:0}},{{y:0,autoAlpha:1,duration:.55,ease:"back.out(2)"}},{start+duration*.68:.3f});'
    if index == 4:
        return common + f'tl.fromTo("{sid} #secure-form",{{y:150,scale:.88,autoAlpha:0}},{{y:0,scale:1,autoAlpha:1,duration:1,ease:"power3.out"}},{start:.3f});tl.fromTo("{sid} #form-lock",{{scale:0,rotation:35}},{{scale:1,rotation:0,duration:.7,ease:"elastic.out(1,.55)"}},{start+duration*.58:.3f});'
    if index == 5:
        return common + f'tl.fromTo("{sid} #ssl-dashboard",{{x:150,autoAlpha:0}},{{x:0,autoAlpha:1,duration:.8,ease:"power3.out"}},{start:.3f});tl.fromTo("{sid} #renew-progress",{{scaleX:.1,transformOrigin:"left center"}},{{scaleX:1,duration:1.1,ease:"power2.out"}},{start+duration*.38:.3f});tl.fromTo("{sid} #renew-bell",{{scale:0,rotation:-35}},{{scale:1,rotation:0,duration:.7,ease:"elastic.out(1,.5)"}},{start+duration*.65:.3f});'
    return common + f'tl.fromTo("{sid} #final-globe",{{scale:.65,rotation:-35,autoAlpha:0}},{{scale:1,rotation:0,autoAlpha:1,duration:1.3,ease:"power3.out"}},{start:.3f});tl.fromTo("{sid} #final-shield",{{scale:.25,y:100,autoAlpha:0}},{{scale:1,y:0,autoAlpha:1,duration:1.05,ease:"back.out(1.6)"}},{start+duration*.3:.3f});tl.fromTo("{sid} #final-url",{{y:80,autoAlpha:0}},{{y:0,autoAlpha:1,duration:.7,ease:"power3.out"}},{start+duration*.68:.3f});'
