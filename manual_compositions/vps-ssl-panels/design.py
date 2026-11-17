"""Composición editorial: conseguir un SSL gratuito gestionado desde un VPS y un panel web."""
from __future__ import annotations

def build_design(duration, words, groups, title):
    cuts = [0, .14, .29, .43, .60, .76, .89, 1]
    copy = [
        ("DEL VIDEO ANTERIOR", "EL SSL PUEDE COSTAR $0", "Ahora veamos cómo conseguirlo y administrarlo"),
        ("UNA ALTERNATIVA", "UN VPS TE DA CONTROL", "Un servidor virtual que puedes configurar y administrar"),
        ("PARA HACERLO MÁS FÁCIL", "UTILIZA UN PANEL WEB", "Gestiona sitios, dominios y servicios desde una interfaz"),
        ("ALGUNOS PANELES CONOCIDOS", "CPANEL · AAPANEL", "ISPConfig · HestiaCP"),
        ("EL CERTIFICADO", "LET'S ENCRYPT", "Solicita el SSL y facilita su instalación y renovación"),
        ("NO ES OBLIGATORIO", "¿TU HOSTING YA INCLUYE SSL?", "También puedes activarlo allí, sin contratar un VPS"),
        ("QUE NO SE CONFUNDAN LOS COSTOS", "VPS ≠ CERTIFICADO", "El servidor puede costar; el certificado puede ser gratuito"),
    ]
    scenes = []
    for i, (label, headline, detail) in enumerate(copy):
        a, b = duration * cuts[i], duration * cuts[i + 1]
        scenes.append({
            "start": round(a, 3), "end": round(b, 3),
            "label": label, "headline": headline, "detail": detail,
            "markup": _visual(i), "animation": _animation(i, a, b)
        })

    sounds = [
        ("pop-medium-in", duration * .015, -11),
        ("digital-power-up", duration * .14, -10),
        ("whoosh-medium-soft", duration * .29, -12),
        ("click-tap-medium", duration * .43, -12),
        ("notification-success-soft", duration * .60, -10),
        ("mechanical-switch-light", duration * .76, -11),
        ("data-chart-reveal", duration * .89, -11),
        ("sting-warm-short", duration * .975, -13),
    ]
    events = [
        {"id": sid, "moment": round(moment, 3), "gain_db": gain, "label": sid}
        for sid, moment, gain in sounds if 0 <= moment < duration
    ]
    return {"css": _css(), "scenes": scenes, "sfx_events": events}


def _css():
    return r"""
    #root{
      background:
        radial-gradient(ellipse at 16% 20%,rgba(137,105,255,.26),transparent 37%),
        radial-gradient(ellipse at 85% 78%,rgba(117,231,171,.17),transparent 39%),
        linear-gradient(145deg,#10121d,#17192a 52%,#0a1018);
    }
    #root:before{
      content:"";position:absolute;inset:0;pointer-events:none;opacity:.15;
      background-image:radial-gradient(rgba(211,204,255,.72) 1px,transparent 1px);
      background-size:38px 38px;
      mask-image:linear-gradient(to bottom,transparent,#000 14%,#000 86%,transparent);
    }
    .manual-scene{background:radial-gradient(ellipse at 50% 58%,rgba(132,111,220,.12),transparent 67%)}
    .manual-scene-kicker{color:#c1aaff;text-shadow:0 0 24px rgba(161,133,255,.35)}
    .manual-scene-headline{color:#f8f7ff;text-shadow:0 7px 34px #050711;letter-spacing:-2.7px}
    .manual-scene-detail{color:#cbd0e4;text-shadow:0 3px 14px #080b17}
    .manual-scene-index{color:#83e6b3}
    .manual-scene-index:after{content:"  ·  CLOUDSERVICEGM";font-size:13px;letter-spacing:2px;color:#afb6cf;opacity:.76}
    .p-art{position:absolute;left:0;right:0;top:430px;height:980px;display:flex;align-items:center;justify-content:center}
    .p-art svg{width:100%;height:100%;overflow:visible}
    .p-orbit{fill:none;stroke:#706e9c;stroke-width:2;stroke-dasharray:8 14;opacity:.72}
    .p-panel{fill:#20243a;stroke:#777ca9;stroke-width:4}
    .p-card{fill:#2a304b;stroke:#9299c8;stroke-width:3}
    .p-violet{fill:#aa92ff}.p-green{fill:#83e6b3}.p-yellow{fill:#f7d47d}
    .p-white{fill:#f8f7ff}.p-muted{fill:#cbd0e4;font:600 24px Arial}
    .p-small{fill:#d9dcf0;font:700 21px Arial}
    .p-bold{fill:#faf9ff;font:900 33px Arial}
    .p-kicker{fill:#c1aaff;font:900 21px Arial;letter-spacing:3px}
    .p-line{fill:none;stroke:#a4a7ce;stroke-width:5;stroke-linecap:round;stroke-linejoin:round}
    .p-dash{fill:none;stroke:#9695c5;stroke-width:4;stroke-dasharray:10 12}
    .p-check{fill:none;stroke:#83e6b3;stroke-width:12;stroke-linecap:round;stroke-linejoin:round}
    .p-glow{filter:drop-shadow(0 0 26px #aa92ff44)}
    .p-green-glow{filter:drop-shadow(0 0 26px #83e6b344)}
    """
def _svg(body, label):
    return f'<div class="p-art"><svg viewBox="0 0 900 900" role="img" aria-label="{label}">{body}</svg></div>'


def _visual(i):
    if i == 0:
        return _svg("""
        <g id="ssl-return-orbit"><circle cx="450" cy="440" r="345" class="p-orbit"/><circle cx="450" cy="440" r="275" class="p-orbit"/></g>
        <g id="ssl-return-cert" transform="translate(235 170)">
          <path d="M0 0H340L445 105V550H0Z" class="p-panel p-glow"/>
          <path d="M340 0V105H445" fill="#35365a" stroke="#a99aff" stroke-width="4"/>
          <text x="220" y="75" text-anchor="middle" class="p-kicker">CERTIFICADO SSL</text>
          <circle cx="220" cy="245" r="105" fill="#2e3c49" stroke="#83e6b3" stroke-width="7"/>
          <path d="M174 245L207 278L272 202" class="p-check"/>
          <text x="220" y="420" text-anchor="middle" class="p-bold">HTTPS</text>
          <rect x="65" y="465" width="310" height="58" rx="24" fill="#164d3b" stroke="#83e6b3" stroke-width="3"/>
          <text x="220" y="505" text-anchor="middle" class="p-bold">0 DÓLARES</text>
        </g>
        <g id="ssl-return-sparkles" fill="#f7d47d">
          <path d="M155 230L170 265L207 270L179 294L187 330L155 311L123 330L131 294L103 270L140 265Z"/>
          <path d="M755 565L768 595L800 599L776 620L782 651L755 635L728 651L734 620L710 599L742 595Z"/>
        </g>
        """, "Certificado HTTPS con un sello que indica cero dólares, retomando el video anterior")

    if i == 1:
        return _svg("""
        <g id="vps-orbit"><ellipse cx="450" cy="455" rx="350" ry="285" class="p-orbit"/><path d="M100 455H800M450 120V790" class="p-dash" opacity=".45"/></g>
        <g id="vps-rack" transform="translate(285 155)">
          <rect width="330" height="560" rx="32" class="p-panel p-glow"/>
          <text x="165" y="65" text-anchor="middle" class="p-kicker">SERVIDOR VIRTUAL</text>
          <g id="vps-units">
            <rect x="40" y="110" width="250" height="92" rx="17" class="p-card"/>
            <rect x="40" y="225" width="250" height="92" rx="17" class="p-card"/>
            <rect x="40" y="340" width="250" height="92" rx="17" class="p-card"/>
            <circle cx="78" cy="156" r="12" fill="#83e6b3"/><circle cx="78" cy="271" r="12" fill="#83e6b3"/><circle cx="78" cy="386" r="12" fill="#83e6b3"/>
            <path d="M112 156H255M112 271H255M112 386H255" class="p-line"/>
          </g>
          <rect x="42" y="465" width="246" height="58" rx="20" fill="#3b315e" stroke="#aa92ff" stroke-width="3"/>
          <text x="165" y="504" text-anchor="middle" class="p-bold">TU VPS</text>
        </g>
        <g id="vps-control" transform="translate(92 730)">
          <rect width="716" height="108" rx="28" fill="#263048" stroke="#aa92ff" stroke-width="3"/>
          <text x="358" y="45" text-anchor="middle" class="p-kicker">CONFIGURA Y ADMINISTRA</text>
          <path d="M110 75H606" class="p-dash"/>
          <circle cx="205" cy="75" r="11" fill="#83e6b3"/><circle cx="450" cy="75" r="11" fill="#f7d47d"/>
        </g>
        """, "Servidor VPS ilustrado como una máquina virtual administrable")

    if i == 2:
        return _svg("""
        <g id="panel-orbit"><circle cx="450" cy="445" r="345" class="p-orbit"/></g>
        <g id="panel-browser" transform="translate(105 205)">
          <rect width="690" height="490" rx="30" class="p-panel p-glow"/>
          <path d="M0 78H690" stroke="#777ca9" stroke-width="4"/>
          <circle cx="43" cy="39" r="11" fill="#aa92ff"/><circle cx="78" cy="39" r="11" fill="#f7d47d"/><circle cx="113" cy="39" r="11" fill="#83e6b3"/>
          <rect x="28" y="105" width="170" height="350" rx="18" fill="#171b2c"/>
          <g fill="#62658d"><rect x="53" y="145" width="120" height="17" rx="8"/><rect x="53" y="190" width="100" height="17" rx="8"/><rect x="53" y="235" width="120" height="17" rx="8"/><rect x="53" y="280" width="90" height="17" rx="8"/></g>
          <g id="panel-windows">
            <rect x="225" y="112" width="430" height="145" rx="18" class="p-card"/>
            <rect x="250" y="140" width="115" height="85" rx="13" fill="#3c3763"/>
            <path d="M272 180L290 198L340 155" class="p-check"/>
            <rect x="390" y="145" width="220" height="17" rx="8" fill="#d9dcf0"/>
            <rect x="390" y="182" width="180" height="13" rx="6" fill="#777ca9"/>
            <rect x="225" y="280" width="205" height="150" rx="18" class="p-card"/>
            <rect x="450" y="280" width="205" height="150" rx="18" class="p-card"/>
            <g fill="#83e6b3"><circle cx="260" cy="325" r="10"/><circle cx="485" cy="325" r="10"/></g>
            <g fill="#d9dcf0"><rect x="285" y="318" width="110" height="14" rx="7"/><rect x="510" y="318" width="110" height="14" rx="7"/></g>
          </g>
          <text x="440" y="470" text-anchor="middle" class="p-small">PANEL DE ADMINISTRACIÓN WEB</text>
        </g>
        <g id="panel-pointer"><path d="M760 690L810 765L786 770L778 808Z" fill="#83e6b3" stroke="#17202d" stroke-width="5"/></g>
        """, "Interfaz web de administración de servidores con sitios y herramientas")

    if i == 3:
        return _svg("""
        <g id="panel-grid-orbit"><circle cx="450" cy="450" r="355" class="p-orbit"/></g>
        <g id="panel-card-cpanel" transform="translate(75 190)">
          <rect width="350" height="210" rx="28" fill="#253347" stroke="#ff9f78" stroke-width="4" class="p-glow"/>
          <circle cx="75" cy="75" r="40" fill="#ff9f78"/>
          <text x="75" y="86" text-anchor="middle" fill="#1a2030" font-family="Arial" font-size="28" font-weight="900">cP</text>
          <text x="220" y="92" text-anchor="middle" class="p-bold">cPanel</text>
          <path d="M45 145H305" class="p-dash"/>
          <text x="175" y="180" text-anchor="middle" class="p-small">GESTIÓN WEB</text>
        </g>
        <g id="panel-card-aapanel" transform="translate(475 190)">
          <rect width="350" height="210" rx="28" fill="#243c39" stroke="#83e6b3" stroke-width="4"/>
          <circle cx="75" cy="75" r="40" fill="#83e6b3"/>
          <text x="75" y="86" text-anchor="middle" fill="#172a29" font-family="Arial" font-size="24" font-weight="900">aa</text>
          <text x="220" y="92" text-anchor="middle" class="p-bold">aaPanel</text>
          <path d="M45 145H305" class="p-dash"/>
          <text x="175" y="180" text-anchor="middle" class="p-small">GESTIÓN WEB</text>
        </g>
        <g id="panel-card-isp" transform="translate(75 465)">
          <rect width="350" height="210" rx="28" fill="#302d4d" stroke="#aa92ff" stroke-width="4"/>
          <circle cx="75" cy="75" r="40" fill="#aa92ff"/>
          <text x="75" y="85" text-anchor="middle" fill="#211d36" font-family="Arial" font-size="25" font-weight="900">ISP</text>
          <text x="220" y="92" text-anchor="middle" class="p-bold">ISPConfig</text>
          <path d="M45 145H305" class="p-dash"/>
          <text x="175" y="180" text-anchor="middle" class="p-small">GESTIÓN WEB</text>
        </g>
        <g id="panel-card-hestia" transform="translate(475 465)">
          <rect width="350" height="210" rx="28" fill="#40334b" stroke="#f7d47d" stroke-width="4"/>
          <circle cx="75" cy="75" r="40" fill="#f7d47d"/>
          <text x="75" y="85" text-anchor="middle" fill="#282238" font-family="Arial" font-size="25" font-weight="900">H</text>
          <text x="220" y="92" text-anchor="middle" class="p-bold">HestiaCP</text>
          <path d="M45 145H305" class="p-dash"/>
          <text x="175" y="180" text-anchor="middle" class="p-small">GESTIÓN WEB</text>
        </g>
        """, "Cuatro tarjetas con los nombres cPanel, aaPanel, ISPConfig y HestiaCP")

    if i == 4:
        return _svg("""
        <g id="le-orbit"><circle cx="450" cy="440" r="345" class="p-orbit"/><circle cx="450" cy="440" r="270" class="p-orbit"/></g>
        <g id="le-dashboard" transform="translate(105 190)">
          <rect width="690" height="520" rx="30" class="p-panel p-glow"/>
          <text x="345" y="62" text-anchor="middle" class="p-kicker">CERTIFICADO DEL DOMINIO</text>
          <rect x="45" y="105" width="600" height="125" rx="20" class="p-card"/>
          <circle cx="112" cy="168" r="38" fill="#83e6b3"/>
          <path d="M92 168L107 183L135 150" class="p-check"/>
          <text x="390" y="160" text-anchor="middle" class="p-bold">LET'S ENCRYPT</text>
          <text x="390" y="195" text-anchor="middle" class="p-small">SSL / TLS GRATUITO</text>
          <g id="le-settings">
            <rect x="45" y="260" width="600" height="92" rx="18" fill="#242d43" stroke="#777ca9" stroke-width="3"/>
            <text x="85" y="315" class="p-small">INSTALAR EN EL DOMINIO</text>
            <rect x="535" y="280" width="75" height="48" rx="24" fill="#83e6b3"/>
            <circle cx="585" cy="304" r="19" fill="#f8f7ff"/>
            <rect x="45" y="375" width="600" height="92" rx="18" fill="#242d43" stroke="#777ca9" stroke-width="3"/>
            <text x="85" y="430" class="p-small">RENOVACIÓN AUTOMÁTICA</text>
            <rect x="535" y="395" width="75" height="48" rx="24" fill="#83e6b3"/>
            <circle cx="585" cy="419" r="19" fill="#f8f7ff"/>
          </g>
        </g>
        """, "Panel web que solicita Let's Encrypt e ilustra instalación y renovación automática")

    if i == 5:
        return _svg("""
        <g id="choice-orbit"><circle cx="450" cy="445" r="350" class="p-orbit"/></g>
        <g id="choice-hosting" transform="translate(80 245)">
          <rect width="330" height="390" rx="30" class="p-panel"/>
          <circle cx="165" cy="105" r="63" fill="#2b4050" stroke="#83e6b3" stroke-width="5"/>
          <path d="M134 105L157 128L200 80" class="p-check"/>
          <text x="165" y="220" text-anchor="middle" class="p-bold">TU HOSTING</text>
          <text x="165" y="270" text-anchor="middle" class="p-small">¿INCLUYE SSL?</text>
          <rect x="42" y="305" width="246" height="52" rx="20" fill="#164d3b"/>
          <text x="165" y="340" text-anchor="middle" class="p-small">PUEDES ACTIVARLO</text>
        </g>
        <g id="choice-vps" transform="translate(490 245)">
          <rect width="330" height="390" rx="30" class="p-panel"/>
          <rect x="65" y="48" width="200" height="125" rx="18" class="p-card"/>
          <g fill="#83e6b3"><circle cx="95" cy="85" r="9"/><circle cx="95" cy="125" r="9"/></g>
          <g stroke="#cbd0e4" stroke-width="6" stroke-linecap="round"><path d="M120 85H235M120 125H235"/></g>
          <text x="165" y="220" text-anchor="middle" class="p-bold">TU VPS</text>
          <text x="165" y="270" text-anchor="middle" class="p-small">MÁS CONTROL</text>
          <rect x="42" y="305" width="246" height="52" rx="20" fill="#3b315e"/>
          <text x="165" y="340" text-anchor="middle" class="p-small">OTRA ALTERNATIVA</text>
        </g>
        <g id="choice-not-required"><rect x="210" y="700" width="480" height="78" rx="26" fill="#4b3c2b" stroke="#f7d47d" stroke-width="3"/><text x="450" y="750" text-anchor="middle" class="p-bold">VPS NO ES OBLIGATORIO</text></g>
        """, "Comparativa entre activar SSL en un hosting que ya lo incluye o administrarlo desde un VPS")

    return _svg("""
    <g id="cost-orbit"><circle cx="450" cy="450" r="350" class="p-orbit"/></g>
    <g id="cost-equation" transform="translate(85 245)">
      <rect width="330" height="345" rx="30" fill="#164d3b" stroke="#83e6b3" stroke-width="4" class="p-green-glow"/>
      <circle cx="165" cy="95" r="60" fill="#83e6b3"/>
      <path d="M135 95L155 115L198 72" fill="none" stroke="#164d3b" stroke-width="12" stroke-linecap="round"/>
      <text x="165" y="215" text-anchor="middle" class="p-kicker">CERTIFICADO</text>
      <text x="165" y="280" text-anchor="middle" class="p-bold">0 DÓLARES</text>
    </g>
    <g id="cost-server" transform="translate(485 245)">
      <rect width="330" height="345" rx="30" class="p-panel"/>
      <rect x="70" y="45" width="190" height="150" rx="20" class="p-card"/>
      <g fill="#83e6b3"><circle cx="105" cy="90" r="10"/><circle cx="105" cy="140" r="10"/></g>
      <g stroke="#cbd0e4" stroke-width="7" stroke-linecap="round"><path d="M135 90H230M135 140H230"/></g>
      <text x="165" y="235" text-anchor="middle" class="p-kicker">SERVIDOR VPS</text>
      <text x="165" y="290" text-anchor="middle" class="p-bold">PUEDE COSTAR</text>
    </g>
    <g id="cost-community"><rect x="145" y="660" width="610" height="120" rx="28" fill="#302d4d" stroke="#aa92ff" stroke-width="3"/><text x="450" y="710" text-anchor="middle" class="p-kicker">AHORA TE PREGUNTO</text><text x="450" y="755" text-anchor="middle" class="p-bold">¿QUÉ PANEL UTILIZAS?</text></g>
    """, "Comparación entre el precio cero del certificado y el posible costo del VPS con pregunta a la comunidad")


def _animation(i, start, end):
    scope = f"#manual-scene-{i} "
    plans = [
        [
            ("#ssl-return-orbit", "scale:.62,rotation:-22,autoAlpha:0", "scale:1,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'", 0),
            ("#ssl-return-cert", "y:160,rotationY:18,scale:.82,autoAlpha:0", "y:0,rotationY:0,scale:1,autoAlpha:1,duration:.9,ease:'back.out(1.4)'", .18),
            ("#ssl-return-sparkles", "scale:0,autoAlpha:0", "scale:1,autoAlpha:1,duration:.6,stagger:.18,ease:'elastic.out(1,.5)'", 1.1),
        ],
        [
            ("#vps-orbit", "scale:.6,rotation:20,autoAlpha:0", "scale:1,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'", 0),
            ("#vps-rack", "y:170,scale:.78,autoAlpha:0", "y:0,scale:1,autoAlpha:1,duration:.85,ease:'back.out(1.5)'", .18),
            ("#vps-units rect", "x:-65,autoAlpha:0", "x:0,autoAlpha:1,duration:.5,stagger:.16,ease:'power2.out'", .7),
            ("#vps-control", "y:90,autoAlpha:0", "y:0,autoAlpha:1,duration:.65,ease:'back.out(1.5)'", 1.5),
        ],
        [
            ("#panel-orbit", "scale:.65,rotation:-18,autoAlpha:0", "scale:1,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'", 0),
            ("#panel-browser", "y:150,rotationX:12,scale:.84,autoAlpha:0", "y:0,rotationX:0,scale:1,autoAlpha:1,duration:.85,ease:'power3.out'", .2),
            ("#panel-windows rect", "scale:.8,autoAlpha:0", "scale:1,autoAlpha:1,duration:.55,stagger:.13,ease:'back.out(1.6)'", .85),
            ("#panel-pointer", "x:40,y:60,rotation:-20,autoAlpha:0", "x:0,y:0,rotation:0,autoAlpha:1,duration:.55,ease:'power2.out'", 1.5),
        ],
        [
            ("#panel-grid-orbit", "scale:.6,rotation:-15,autoAlpha:0", "scale:1,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'", 0),
            ("#panel-card-cpanel", "x:-170,rotation:-8,autoAlpha:0", "x:0,rotation:0,autoAlpha:1,duration:.7,ease:'back.out(1.5)'", .12),
            ("#panel-card-aapanel", "x:170,rotation:8,autoAlpha:0", "x:0,rotation:0,autoAlpha:1,duration:.7,ease:'back.out(1.5)'", .28),
            ("#panel-card-isp", "x:-170,y:90,autoAlpha:0", "x:0,y:0,autoAlpha:1,duration:.7,ease:'back.out(1.5)'", .65),
            ("#panel-card-hestia", "x:170,y:90,autoAlpha:0", "x:0,y:0,autoAlpha:1,duration:.7,ease:'back.out(1.5)'", .82),
        ],
        [
            ("#le-orbit", "scale:.62,rotation:20,autoAlpha:0", "scale:1,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'", 0),
            ("#le-dashboard", "y:150,scale:.82,autoAlpha:0", "y:0,scale:1,autoAlpha:1,duration:.85,ease:'back.out(1.4)'", .18),
            ("#le-settings rect", "scaleX:.15,transformOrigin:'left center',autoAlpha:0", "scaleX:1,autoAlpha:1,duration:.58,stagger:.2,ease:'power2.out'", .9),
            ("#le-settings circle", "scale:0,autoAlpha:0", "scale:1,autoAlpha:1,duration:.5,stagger:.18,ease:'back.out(2)'", 1.3),
        ],
        [
            ("#choice-orbit", "scale:.62,rotation:-20,autoAlpha:0", "scale:1,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'", 0),
            ("#choice-hosting", "x:-145,autoAlpha:0", "x:0,autoAlpha:1,duration:.75,ease:'power3.out'", .15),
            ("#choice-vps", "x:145,autoAlpha:0", "x:0,autoAlpha:1,duration:.75,ease:'power3.out'", .3),
            ("#choice-not-required", "y:80,scale:.88,autoAlpha:0", "y:0,scale:1,autoAlpha:1,duration:.65,ease:'back.out(1.7)'", 1.25),
        ],
        [
            ("#cost-orbit", "scale:.62,rotation:-18,autoAlpha:0", "scale:1,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'", 0),
            ("#cost-equation", "x:-150,rotation:-7,autoAlpha:0", "x:0,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'", .16),
            ("#cost-server", "x:150,rotation:7,autoAlpha:0", "x:0,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'", .32),
            ("#cost-community", "y:80,autoAlpha:0", "y:0,autoAlpha:1,duration:.65,ease:'back.out(1.6)'", 1.45),
        ],
    ]
    result = []
    for selector, frm, to, offset in plans[i]:
        if to:
            result.append(f'tl.fromTo("{scope}{selector}",{{{frm}}},{{{to}}},{start+offset:.3f});')
        else:
            result.append(f'tl.to("{scope}{selector}",{{{frm}}},{start+offset:.3f});')
    return "".join(result)
