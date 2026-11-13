"""Composición editorial: el SSL gratuito, el cobro del hosting y el control del servidor."""
from __future__ import annotations

def build_design(duration, words, groups, title):
    cuts = [0, .135, .305, .485, .635, .815, .91, 1]
    copy = [
        ("UNA PREGUNTA INCÓMODA", "¿TE COBRAN POR EL CANDADITO?", "Puede que estés pagando por algo que también existe gratis"),
        ("CONOCE LA ALTERNATIVA", "LET'S ENCRYPT", "Certificados SSL/TLS gratuitos para proteger la conexión de tu web"),
        ("¿CÓMO FUNCIONA?", "TU SERVIDOR DEMUESTRA QUE CONTROLAS EL DOMINIO", "Una vez validado, puede solicitar e instalar el certificado"),
        ("PERO HAY UN DETALLE", "GRATUITO NO ES OLVIDARSE", "El certificado vence: la renovación automática debe funcionar"),
        ("NO CONFUNDAS LOS SERVICIOS", "CERTIFICADO NO ES LO MISMO QUE GESTIÓN", "Pueden cobrarte por instalarlo, administrarlo o darte soporte"),
        ("TE TOCA A TI", "¿QUÉ HACE TU HOSTING?", "¿Te incluye el SSL o te cobra por gestionarlo?"),
        ("SIGUIENTE TEMA", "¿DÓNDE TIENES MÁS CONTROL?", "En el próximo video: servidores VPS")
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
        ("whoosh-medium-soft", .15, -10),
        ("notification-error-soft", duration * .13, -8),
        ("digital-power-up", duration * .305, -10),
        ("click-tap-medium", duration * .36, -13),
        ("mechanical-switch-light", duration * .49, -10),
        ("notification-success-soft", duration * .635, -9),
        ("data-chart-reveal", duration * .70, -11),
        ("pop-medium-in", duration * .82, -12),
        ("swish-medium", duration * .91, -11),
        ("sting-warm-short", duration * .97, -12),
    ]
    events = [
        {"id": sid, "moment": round(t, 3), "gain_db": gain, "label": sid}
        for sid, t, gain in sounds if 0 <= t < duration
    ]
    return {"css": _css(), "scenes": scenes, "sfx_events": events}


def _css():
    return r"""
    #root{
      background:
        radial-gradient(ellipse at 14% 18%,rgba(57,91,184,.34),transparent 36%),
        radial-gradient(ellipse at 88% 70%,rgba(232,103,87,.20),transparent 35%),
        linear-gradient(145deg,#10152b,#111d39 52%,#0a1020);
    }
    #root:before{
      content:"";position:absolute;inset:0;pointer-events:none;opacity:.18;
      background-image:radial-gradient(rgba(255,205,125,.72) 1px,transparent 1px);
      background-size:34px 34px;
      mask-image:linear-gradient(to bottom,transparent,#000 16%,#000 84%,transparent);
    }
    .manual-scene{background:radial-gradient(ellipse at 50% 58%,rgba(52,78,139,.15),transparent 68%)}
    .manual-scene-kicker{color:#ffc879;text-shadow:0 0 24px rgba(255,174,91,.32)}
    .manual-scene-headline{color:#fff9f0;text-shadow:0 7px 34px #050914;letter-spacing:-2.6px}
    .manual-scene-detail{color:#c8d4ee;text-shadow:0 3px 14px #080d1c}
    .manual-scene-index{color:#ffc879}
    .manual-scene-index:after{content:"  ·  CLOUDSERVICEGM";font-size:13px;letter-spacing:2px;color:#aab8dc;opacity:.75}
    .sp-art{position:absolute;left:0;right:0;top:430px;height:980px;display:flex;align-items:center;justify-content:center}
    .sp-art svg{width:100%;height:100%;overflow:visible}
    .sp-orbit{fill:none;stroke:#526ba6;stroke-width:2;stroke-dasharray:7 13}
    .sp-line{fill:none;stroke:#819bd6;stroke-width:4;stroke-dasharray:12 12}
    .sp-panel{fill:#172443;stroke:#718ac1;stroke-width:4}
    .sp-card{fill:#202f55;stroke:#91a9e3;stroke-width:3}
    .sp-orange{fill:#ff9278}
    .sp-yellow{fill:#ffd17b}
    .sp-blue{fill:#8cb1ff}
    .sp-white{fill:#fff8eb}
    .sp-muted{fill:#c3cfea;font:600 24px Arial}
    .sp-small{fill:#d2ddf4;font:700 20px Arial}
    .sp-bright{fill:#fff9f0;font:900 31px Arial}
    .sp-title{fill:#ffd17b;font:900 22px Arial;letter-spacing:3px}
    .sp-stroke{fill:none;stroke:#ffad82;stroke-width:9;stroke-linecap:round;stroke-linejoin:round}
    .sp-check{fill:none;stroke:#8be0bd;stroke-width:12;stroke-linecap:round;stroke-linejoin:round}
    .sp-warning{fill:#482b3c;stroke:#ff8c83;stroke-width:4}
    .sp-glow{filter:drop-shadow(0 0 25px #829fff55)}
    .sp-glow-warm{filter:drop-shadow(0 0 24px #ff9c7555)}
    .sp-track{fill:#35466d}
    .sp-fill{fill:#8be0bd}
    """

def _svg(body, label):
    return f'<div class="sp-art"><svg viewBox="0 0 900 900" role="img" aria-label="{label}">{body}</svg></div>'


def _visual(i):
    if i == 0:
        return _svg("""
        <g id="bill-orbits"><circle cx="450" cy="455" r="350" class="sp-orbit"/><circle cx="450" cy="455" r="292" class="sp-orbit"/><path d="M90 455H810M450 95V815" class="sp-line" opacity=".35"/></g>
        <g id="bill" transform="translate(145 160)">
          <rect width="610" height="570" rx="34" class="sp-panel sp-glow"/>
          <path d="M0 95H610" stroke="#718ac1" stroke-width="3"/>
          <text x="48" y="62" class="sp-title">FACTURA DE HOSTING</text>
          <rect x="42" y="135" width="526" height="115" rx="20" class="sp-card"/>
          <text x="72" y="180" class="sp-small">CERTIFICADO SSL</text>
          <text x="72" y="220" class="sp-bright">CARGO ANUAL</text>
          <g id="bill-cross"><path d="M440 155L535 235M535 155L440 235" class="sp-stroke"/></g>
          <path d="M44 290H566" class="sp-line" opacity=".65"/>
          <text x="52" y="350" class="sp-muted">ALTERNATIVA DISPONIBLE</text>
          <rect x="42" y="385" width="526" height="118" rx="20" fill="#17483f" stroke="#8be0bd" stroke-width="4"/>
          <text x="78" y="435" class="sp-small">CERTIFICADO SSL</text>
          <text x="78" y="482" class="sp-bright">0 DÓLARES</text>
          <g id="zero-seal"><circle cx="505" cy="445" r="42" fill="#8be0bd"/><path d="M484 445L499 460L528 427" class="sp-check"/></g>
        </g>
        <g id="question-mark"><circle cx="755" cy="760" r="54" class="sp-warning"/><text x="755" y="782" text-anchor="middle" class="sp-bright">?</text></g>
        """, "Factura ilustrativa de hosting que contrasta un cargo SSL con una alternativa gratuita")

    if i == 1:
        return _svg("""
        <g id="le-rings"><circle cx="450" cy="430" r="330" class="sp-orbit"/><circle cx="450" cy="430" r="265" class="sp-orbit"/><path d="M120 430H780M450 100V760" class="sp-line" opacity=".35"/></g>
        <g id="le-certificate" transform="translate(225 160)">
          <path d="M0 0H355L465 110V550H0Z" fill="#1b2e53" stroke="#ffc879" stroke-width="5" class="sp-glow-warm"/>
          <path d="M355 0V110H465" fill="#344b7c" stroke="#ffc879" stroke-width="4"/>
          <text x="42" y="72" class="sp-title">CERTIFICADO DIGITAL</text>
          <circle cx="230" cy="245" r="105" fill="#273e6d" stroke="#8be0bd" stroke-width="7"/>
          <path d="M184 245L220 282L286 205" class="sp-check"/>
          <text x="232" y="405" text-anchor="middle" class="sp-bright">LET'S ENCRYPT</text>
          <text x="232" y="450" text-anchor="middle" class="sp-small">SSL / TLS</text>
          <rect x="55" y="485" width="355" height="48" rx="20" fill="#17483f"/>
          <text x="232" y="517" text-anchor="middle" class="sp-small">GRATUITO</text>
        </g>
        <g id="le-stars"><path d="M145 210L160 245L197 250L169 274L176 311L145 292L114 311L121 274L93 250L130 245Z" fill="#ffd17b"/><path d="M760 570L773 600L805 604L781 626L787 658L760 642L733 658L739 626L715 604L747 600Z" fill="#8cb1ff"/></g>
        """, "Certificado digital conceptual de Let's Encrypt con sello de gratuidad")

    if i == 2:
        return _svg("""
        <g id="domain-orbits"><circle cx="450" cy="445" r="330" class="sp-orbit"/><path d="M100 445H800M450 95V800" class="sp-line" opacity=".32"/></g>
        <g id="domain-card" transform="translate(100 230)">
          <rect width="330" height="255" rx="28" class="sp-panel sp-glow"/>
          <circle cx="165" cy="80" r="48" fill="#2b4579" stroke="#8cb1ff" stroke-width="4"/>
          <text x="165" y="92" text-anchor="middle" class="sp-bright">www</text>
          <text x="165" y="170" text-anchor="middle" class="sp-title">TU DOMINIO</text>
          <text x="165" y="210" text-anchor="middle" class="sp-small">¿ES TUYO?</text>
        </g>
        <g id="server-card" transform="translate(500 230)">
          <rect width="300" height="255" rx="28" class="sp-panel sp-glow"/>
          <rect x="60" y="43" width="180" height="50" rx="12" class="sp-card"/>
          <rect x="60" y="112" width="180" height="50" rx="12" class="sp-card"/>
          <rect x="60" y="181" width="180" height="28" rx="10" fill="#17483f"/>
          <circle cx="86" cy="68" r="8" fill="#8be0bd"/><circle cx="86" cy="137" r="8" fill="#8be0bd"/>
          <text x="150" y="238" text-anchor="middle" class="sp-small">TU SERVIDOR</text>
        </g>
        <g id="domain-connection"><path d="M430 355H500M470 330L500 355L470 380" class="sp-stroke"/><circle cx="465" cy="355" r="12" fill="#ffd17b"/></g>
        <g id="certbot-card" transform="translate(225 580)">
          <rect width="450" height="145" rx="28" fill="#17483f" stroke="#8be0bd" stroke-width="4"/>
          <circle cx="78" cy="72" r="37" fill="#8be0bd"/><path d="M59 72L73 86L99 57" class="sp-check"/>
          <text x="255" y="65" text-anchor="middle" class="sp-bright">CERTBOT</text>
          <text x="255" y="105" text-anchor="middle" class="sp-small">SOLICITA E INSTALA</text>
        </g>
        """, "Dominio y servidor conectados con una herramienta que solicita e instala el certificado")

    if i == 3:
        return _svg("""
        <g id="expiry-clock" transform="translate(450 365)">
          <circle r="260" class="sp-orbit"/><circle r="205" fill="#1c2b4e" stroke="#ffc879" stroke-width="7" class="sp-glow-warm"/>
          <path d="M0 -125V0L95 58" class="sp-stroke"/><circle r="16" fill="#ffc879"/>
        </g>
        <g id="expiry-calendar" transform="translate(205 545)">
          <rect width="490" height="225" rx="28" class="sp-panel"/>
          <path d="M0 75H490" stroke="#718ac1" stroke-width="4"/>
          <text x="245" y="52" text-anchor="middle" class="sp-title">EL CERTIFICADO VENCE</text>
          <g id="calendar-days" fill="#718ac1"><rect x="55" y="110" width="70" height="48" rx="8"/><rect x="155" y="110" width="70" height="48" rx="8"/><rect x="255" y="110" width="70" height="48" rx="8"/><rect x="355" y="110" width="70" height="48" rx="8"/></g>
          <path d="M365 112L420 158M420 112L365 158" class="sp-stroke"/>
          <text x="245" y="198" text-anchor="middle" class="sp-small">NO LO DEJES PARA DESPUÉS</text>
        </g>
        <g id="renew-switch" transform="translate(250 790)">
          <rect width="400" height="74" rx="37" fill="#17483f" stroke="#8be0bd" stroke-width="3"/>
          <text x="155" y="48" text-anchor="middle" class="sp-small">RENOVACIÓN</text>
          <rect x="282" y="12" width="105" height="50" rx="25" fill="#8be0bd"/>
          <circle cx="360" cy="37" r="20" fill="#fff8eb"/>
        </g>
        """, "Calendario de vencimiento y un interruptor de renovación automática")

    if i == 4:
        return _svg("""
        <g id="free-certificate" transform="translate(70 260)">
          <rect width="330" height="405" rx="30" fill="#17483f" stroke="#8be0bd" stroke-width="4" class="sp-glow"/>
          <circle cx="165" cy="105" r="58" fill="#8be0bd"/>
          <path d="M135 105L156 126L198 80" class="sp-check"/>
          <text x="165" y="220" text-anchor="middle" class="sp-title">CERTIFICADO</text>
          <text x="165" y="278" text-anchor="middle" class="sp-bright">0 DÓLARES</text>
          <text x="165" y="330" text-anchor="middle" class="sp-small">LET'S ENCRYPT</text>
        </g>
        <g id="service-list" transform="translate(500 250)">
          <rect width="330" height="430" rx="30" class="sp-panel sp-glow"/>
          <text x="165" y="62" text-anchor="middle" class="sp-title">SERVICIOS</text>
          <g id="service-items">
            <rect x="28" y="100" width="274" height="76" rx="16" class="sp-card"/>
            <text x="165" y="148" text-anchor="middle" class="sp-bright">INSTALACIÓN</text>
            <rect x="28" y="195" width="274" height="76" rx="16" class="sp-card"/>
            <text x="165" y="243" text-anchor="middle" class="sp-bright">GESTIÓN</text>
            <rect x="28" y="290" width="274" height="76" rx="16" class="sp-card"/>
            <text x="165" y="338" text-anchor="middle" class="sp-bright">SOPORTE</text>
          </g>
        </g>
        <g id="services-arrow"><path d="M410 470H490M465 445L490 470L465 495" class="sp-stroke"/></g>
        <g id="different-tag"><rect x="180" y="735" width="540" height="72" rx="26" fill="#493047" stroke="#ff9278" stroke-width="3"/><text x="450" y="781" text-anchor="middle" class="sp-bright">NO ES LO MISMO</text></g>
        """, "Comparación entre un certificado gratuito y servicios de instalación, gestión y soporte")

    if i == 5:
        return _svg("""
        <g id="comment-halo"><circle cx="450" cy="445" r="325" class="sp-orbit"/><circle cx="450" cy="445" r="255" class="sp-orbit"/></g>
        <g id="question-card" transform="translate(125 230)">
          <rect width="650" height="215" rx="32" class="sp-panel sp-glow"/>
          <text x="325" y="75" text-anchor="middle" class="sp-title">CUÉNTAME EN COMENTARIOS</text>
          <text x="325" y="143" text-anchor="middle" class="sp-bright">¿QUÉ HACE TU HOSTING?</text>
        </g>
        <g id="answer-one" transform="translate(90 525)">
          <rect width="340" height="125" rx="25" fill="#17483f" stroke="#8be0bd" stroke-width="4"/>
          <circle cx="55" cy="62" r="25" fill="#8be0bd"/><path d="M42 62L53 73L72 50" class="sp-check"/>
          <text x="205" y="74" text-anchor="middle" class="sp-bright">LO INCLUYE</text>
        </g>
        <g id="answer-two" transform="translate(470 525)">
          <rect width="340" height="125" rx="25" fill="#493047" stroke="#ff9278" stroke-width="4"/>
          <circle cx="55" cy="62" r="25" fill="#ff9278"/><path d="M45 52L65 72M65 52L45 72" class="sp-stroke"/>
          <text x="210" y="56" text-anchor="middle" class="sp-small">ME COBRA</text>
          <text x="210" y="89" text-anchor="middle" class="sp-bright">POR GESTIÓN</text>
        </g>
        <g id="chat-dots"><circle cx="360" cy="735" r="12" fill="#ffc879"/><circle cx="405" cy="735" r="12" fill="#ffc879"/><circle cx="450" cy="735" r="12" fill="#ffc879"/></g>
        """, "Dos burbujas de respuesta para invitar a comentar la experiencia con el hosting")

    return _svg("""
    <g id="vps-orbits"><circle cx="450" cy="430" r="350" class="sp-orbit"/><path d="M90 430H810M450 80V790M190 170L710 690M710 170L190 690" class="sp-line" opacity=".35"/></g>
    <g id="vps-rack" transform="translate(280 145)">
      <rect width="340" height="520" rx="30" class="sp-panel sp-glow"/>
      <text x="170" y="62" text-anchor="middle" class="sp-title">INFRAESTRUCTURA</text>
      <g id="rack-units">
        <rect x="38" y="100" width="264" height="92" rx="16" class="sp-card"/>
        <rect x="38" y="215" width="264" height="92" rx="16" class="sp-card"/>
        <rect x="38" y="330" width="264" height="92" rx="16" class="sp-card"/>
        <circle cx="75" cy="146" r="12" fill="#8be0bd"/><circle cx="75" cy="261" r="12" fill="#8be0bd"/><circle cx="75" cy="376" r="12" fill="#8be0bd"/>
        <path d="M110 146H270M110 261H270M110 376H270" class="sp-line"/>
      </g>
      <text x="170" y="480" text-anchor="middle" class="sp-bright">TU SERVIDOR</text>
    </g>
    <g id="control-sliders" transform="translate(110 700)">
      <rect width="680" height="145" rx="28" fill="#493047" stroke="#ff9278" stroke-width="4"/>
      <text x="340" y="47" text-anchor="middle" class="sp-title">MÁS CONTROL SOBRE TU WEB</text>
      <path d="M90 92H590" stroke="#ffb18e" stroke-width="8" stroke-linecap="round"/>
      <circle cx="190" cy="92" r="19" fill="#fff8eb"/><circle cx="390" cy="92" r="19" fill="#fff8eb"/><circle cx="550" cy="92" r="19" fill="#fff8eb"/>
    </g>
    <g id="vps-label"><rect x="260" y="865" width="380" height="58" rx="28" fill="#17483f" stroke="#8be0bd" stroke-width="3"/><text x="450" y="903" text-anchor="middle" class="sp-bright">PRÓXIMO: VPS</text></g>
    """, "Rack de servidor con controles y rótulo del próximo tema sobre VPS")


def _animation(i, start, end):
    scope = f"#manual-scene-{i} "
    plans = [
        [
            ("#bill-orbits", "scale:.65,rotation:-18,autoAlpha:0", "scale:1,rotation:0,autoAlpha:1,duration:.9,ease:'power3.out'", 0),
            ("#bill", "y:170,rotationY:14,scale:.86,autoAlpha:0", "y:0,rotationY:0,scale:1,autoAlpha:1,duration:.85,ease:'back.out(1.5)'", .18),
            ("#bill-cross", "scale:0,rotation:-30", "scale:1,rotation:0,duration:.55,ease:'back.out(2)'", 1.0),
            ("#zero-seal", "scale:0,rotation:-90", "scale:1,rotation:0,duration:.7,ease:'elastic.out(1,.5)'", 1.5),
            ("#question-mark", "scale:0,autoAlpha:0", "scale:1,autoAlpha:1,duration:.55,ease:'back.out(2)'", 2.0),
        ],
        [
            ("#le-rings", "scale:.65,rotation:-20,autoAlpha:0", "scale:1,rotation:0,autoAlpha:1,duration:.9,ease:'power3.out'", 0),
            ("#le-certificate", "y:180,rotation:-8,scale:.8,autoAlpha:0", "y:0,rotation:0,scale:1,autoAlpha:1,duration:1,ease:'back.out(1.4)'", .22),
            ("#le-stars", "scale:0,autoAlpha:0", "scale:1,autoAlpha:1,duration:.65,stagger:.18,ease:'elastic.out(1,.5)'", 1.25),
            ("#le-rings", "rotation:8,duration:2.2,ease:'none'", "", 1.6),
        ],
        [
            ("#domain-orbits", "scale:.65,autoAlpha:0", "scale:1,autoAlpha:1,duration:.8,ease:'power3.out'", 0),
            ("#domain-card", "x:-170,autoAlpha:0", "x:0,autoAlpha:1,duration:.75,ease:'back.out(1.6)'", .2),
            ("#server-card", "x:170,autoAlpha:0", "x:0,autoAlpha:1,duration:.75,ease:'back.out(1.6)'", .35),
            ("#domain-connection", "scaleX:0,transformOrigin:'left center'", "scaleX:1,duration:.55,ease:'power2.out'", 1.05),
            ("#certbot-card", "y:120,scale:.85,autoAlpha:0", "y:0,scale:1,autoAlpha:1,duration:.75,ease:'back.out(1.5)'", 1.5),
        ],
        [
            ("#expiry-clock", "scale:.55,rotation:-70,autoAlpha:0", "scale:1,rotation:0,autoAlpha:1,duration:.85,ease:'power3.out'", 0),
            ("#expiry-calendar", "y:120,autoAlpha:0", "y:0,autoAlpha:1,duration:.7,ease:'back.out(1.5)'", .7),
            ("#calendar-days", "scaleY:0,transformOrigin:'center bottom'", "scaleY:1,duration:.55,stagger:.08,ease:'power2.out'", 1.0),
            ("#renew-switch", "y:80,scale:.8,autoAlpha:0", "y:0,scale:1,autoAlpha:1,duration:.65,ease:'back.out(1.6)'", 1.55),
            ("#expiry-clock", "rotation:7,duration:.2,repeat:4,yoyo:true,ease:'sine.inOut'", "", 1.8),
        ],
        [
            ("#free-certificate", "x:-150,rotation:-8,autoAlpha:0", "x:0,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'", 0),
            ("#service-list", "x:150,rotation:8,autoAlpha:0", "x:0,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'", .18),
            ("#service-items rect", "scaleX:0,transformOrigin:'left center'", "scaleX:1,duration:.48,stagger:.2,ease:'power2.out'", .85),
            ("#services-arrow", "scale:0,autoAlpha:0", "scale:1,autoAlpha:1,duration:.55,ease:'back.out(2)'", 1.25),
            ("#different-tag", "y:70,autoAlpha:0", "y:0,autoAlpha:1,duration:.6,ease:'back.out(1.7)'", 1.7),
        ],
        [
            ("#comment-halo", "scale:.55,rotation:-20,autoAlpha:0", "scale:1,rotation:0,autoAlpha:1,duration:.85,ease:'power3.out'", 0),
            ("#question-card", "y:140,scale:.9,autoAlpha:0", "y:0,scale:1,autoAlpha:1,duration:.8,ease:'back.out(1.5)'", .15),
            ("#answer-one", "x:-150,autoAlpha:0", "x:0,autoAlpha:1,duration:.65,ease:'back.out(1.6)'", .9),
            ("#answer-two", "x:150,autoAlpha:0", "x:0,autoAlpha:1,duration:.65,ease:'back.out(1.6)'", 1.08),
            ("#chat-dots circle", "scale:0", "scale:1,duration:.4,stagger:.12,repeat:1,yoyo:true,ease:'back.out(2)'", 1.7),
        ],
        [
            ("#vps-orbits", "scale:.6,rotation:-20,autoAlpha:0", "scale:1,rotation:0,autoAlpha:1,duration:.9,ease:'power3.out'", 0),
            ("#vps-rack", "y:180,scale:.8,autoAlpha:0", "y:0,scale:1,autoAlpha:1,duration:.9,ease:'back.out(1.5)'", .18),
            ("#rack-units rect", "x:-35,autoAlpha:0", "x:0,autoAlpha:1,duration:.42,stagger:.14,ease:'power2.out'", .8),
            ("#control-sliders", "y:100,autoAlpha:0", "y:0,autoAlpha:1,duration:.7,ease:'back.out(1.5)'", 1.45),
            ("#vps-label", "scale:0,autoAlpha:0", "scale:1,autoAlpha:1,duration:.6,ease:'elastic.out(1,.5)'", 2.0),
        ],
    ]
    out = []
    for selector, frm, to, offset in plans[i]:
        if to:
            out.append(f'tl.fromTo("{scope}{selector}",{{{frm}}},{{{to}}},{start + offset:.3f});')
        else:
            out.append(f'tl.to("{scope}{selector}",{{{frm}}},{start + offset:.3f});')
    return "".join(out)
