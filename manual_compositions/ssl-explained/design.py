"""Composición independiente: qué es un certificado SSL y cómo funciona."""
from __future__ import annotations

def build_design(duration, words, groups, title):
    cuts=[0,.11,.22,.33,.44,.55,.66,.77,.88,1]
    scenes_text=[
      ("LA IDENTIDAD DE TU WEB","¿QUÉ ES UN CERTIFICADO SSL?","Es como la credencial digital que identifica a un sitio web"),
      ("UN DOCUMENTO DIGITAL","NO ES SOLO UN CANDADO","Contiene datos del dominio y una clave pública"),
      ("QUIÉN LO RESPALDA","UNA AUTORIDAD CERTIFICADORA","Una entidad de confianza firma el certificado"),
      ("EL NOMBRE IMPORTA","¿EL CERTIFICADO CORRESPONDE A LA WEB?","El navegador comprueba el dominio y la validez"),
      ("EL INICIO DE TLS","NAVEGADOR Y SERVIDOR SE VERIFICAN","El certificado ayuda a autenticar al servidor"),
      ("CLAVES Y CIFRADO","ASÍ SE PREPARA LA CONEXIÓN SEGURA","TLS establece claves para proteger los datos"),
      ("EN LA PRÁCTICA","TUS DATOS VIAJAN CIFRADOS","La conexión HTTPS protege la información en tránsito"),
      ("FECHA Y VIGENCIA","TAMBIÉN DEBE MANTENERSE ACTIVO","Revisa la expiración y renueva a tiempo"),
      ("AHORA YA LO SABES","UN CERTIFICADO, UNA IDENTIDAD DIGITAL","Configura SSL/TLS correctamente con cloudservicegm")
    ]
    scenes=[]
    for i,(label,headline,detail) in enumerate(scenes_text):
        a,b=duration*cuts[i],duration*cuts[i+1]
        scenes.append({"start":round(a,3),"end":round(b,3),"label":label,
          "headline":headline,"detail":detail,"markup":_visual(i),"animation":_animation(i,a,b)})
    sound=[
      ("whoosh-medium-soft",.16,-10),
      ("digital-power-up",duration*.115,-9),
      ("data-chart-reveal",duration*.225,-10),
      ("notification-success-soft",duration*.335,-9),
      ("digital-process-subtle",duration*.445,-10),
      ("tone-step-3",duration*.555,-11),
      ("swish-medium",duration*.665,-9),
      ("mechanical-switch-light",duration*.775,-10),
      ("shimmer-short-soft",duration*.89,-11),
      ("sting-warm-short",duration*.965,-12),
      ("click-tap-medium",duration*.50,-13),
      ("pop-medium-in",duration*.72,-13)
    ]
    events=[{"id":sid,"moment":round(t,3),"gain_db":gain,"label":sid}
      for sid,t,gain in sound if 0<=t<duration]
    return {"css":_css(),"scenes":scenes,"sfx_events":events}

def _css():
    return r"""
    #root{background:radial-gradient(ellipse at 50% 22%,rgba(36,93,112,.45),transparent 43%),radial-gradient(ellipse at 88% 78%,rgba(27,76,91,.22),transparent 40%),linear-gradient(150deg,#07111d,#0a1725 55%,#050a13)}
    #root:before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.19;background-image:linear-gradient(rgba(112,229,218,.11) 1px,transparent 1px),linear-gradient(90deg,rgba(112,229,218,.11) 1px,transparent 1px);background-size:76px 76px;mask-image:linear-gradient(to bottom,transparent,#000 18%,#000 84%,transparent)}
    .manual-scene{background:radial-gradient(ellipse at 50% 55%,rgba(19,70,91,.25),transparent 68%)}
    .manual-scene-kicker{color:#77efd1;text-shadow:0 0 24px rgba(55,221,188,.4)}
    .manual-scene-headline{color:#f4fbff;text-shadow:0 7px 34px #000;letter-spacing:-2.3px}
    .manual-scene-detail{color:#b7ccd9;text-shadow:0 3px 14px #000}
    .manual-scene-index{color:#75e9ce}
    .cert-art{position:absolute;left:0;right:0;top:430px;height:980px;display:flex;align-items:center;justify-content:center}
    .cert-art svg{width:100%;height:100%;overflow:visible}
    .c-orbit{fill:none;stroke:#397d7c;stroke-width:2;stroke-dasharray:8 13}
    .c-line{fill:none;stroke:#5be1c1;stroke-width:3;stroke-dasharray:12 14}
    .c-node{fill:#0b1927;stroke:#65e4c5;stroke-width:4}
    .c-panel{fill:#0d2030;stroke:#426d7d;stroke-width:4}
    .c-chip{fill:#112b38;stroke:#3c897c;stroke-width:2}
    .c-white{fill:#f2fbff}
    .c-muted{fill:#a9c3d3;font:600 23px Arial}
    .c-tiny{fill:#b9d0df;font:700 19px Arial}
    .c-bright{fill:#effffc;font:800 29px Arial}
    .c-green{fill:#70ebcd}
    .c-gold{fill:#f4c875}
    .c-red{fill:#ff7181}
    .c-stroke{fill:none;stroke:#6ee6cc;stroke-width:8;stroke-linecap:round;stroke-linejoin:round}
    .c-check{fill:none;stroke:#6ee6cc;stroke-width:12;stroke-linecap:round;stroke-linejoin:round}
    .c-shield{fill:#102d3a;stroke:#6ee6cc;stroke-width:8;stroke-linejoin:round}
    .c-glow{filter:drop-shadow(0 0 24px #35e4be77)}
    .c-paper{fill:#10283a;stroke:#7ae8d0;stroke-width:5}
    .c-lock{fill:#0a1a28;stroke:#6ee6cc;stroke-width:7}
    .c-wire{fill:none;stroke:#5be1c1;stroke-width:5;stroke-dasharray:10 12}
    """

def _svg(inner, aria):
    return f'<div class="cert-art"><svg viewBox="0 0 900 900" role="img" aria-label="{aria}">{inner}</svg></div>'

def _visual(i):
    if i==0:
      return _svg("""
      <g id="identity-orbits"><circle cx="450" cy="450" r="345" class="c-orbit"/><circle cx="450" cy="450" r="275" class="c-orbit"/><path d="M105 450H795M450 105V795" class="c-line" opacity=".35"/></g>
      <g id="identity-card" transform="translate(180 175)"><rect width="540" height="510" rx="32" class="c-panel c-glow"/><rect x="0" y="0" width="540" height="98" rx="30" fill="#173c4b"/><text x="42" y="61" class="c-green" font-size="24" font-weight="900" letter-spacing="4">DIGITAL ID</text><circle cx="445" cy="48" r="17" fill="#71e9ce"/><rect x="42" y="137" width="150" height="160" rx="20" class="c-chip"/><circle cx="117" cy="190" r="35" class="c-node"/><path d="M67 270Q117 215 167 270" class="c-stroke"/><text x="220" y="165" class="c-tiny">IDENTIDAD DEL SITIO</text><text x="220" y="210" class="c-bright">tu-dominio.com</text><text x="220" y="258" class="c-tiny">CERTIFICADO HTTPS</text><path d="M42 345H495M42 390H430M42 435H465" stroke="#496b7c" stroke-width="8" stroke-linecap="round"/><g id="identity-seal"><circle cx="445" cy="438" r="55" fill="#12423d" stroke="#6ee6cc" stroke-width="4"/><path d="M415 438L438 462L478 414" class="c-check"/></g></g>
      <g id="identity-floats"><circle cx="115" cy="255" r="20" class="c-node"/><circle cx="785" cy="655" r="25" class="c-node"/><path d="M135 255L180 290M720 625L760 655" class="c-line"/></g>
      ""","Credencial digital que identifica un sitio web")
    if i==1:
      return _svg("""
      <g id="document" transform="translate(200 125)"><path d="M0 0H360L500 135V650H0Z" class="c-paper c-glow"/><path d="M360 0V135H500" fill="#1a4050" stroke="#7ae8d0" stroke-width="4"/><text x="42" y="75" class="c-green" font-size="22" font-weight="900" letter-spacing="3">CERTIFICADO X.509</text><rect x="40" y="120" width="410" height="65" rx="12" class="c-chip"/><text x="62" y="162" class="c-bright">Dominio: tu-web.com</text><text x="42" y="245" class="c-tiny">EMISOR</text><text x="42" y="282" class="c-bright">Autoridad certificadora</text><text x="42" y="350" class="c-tiny">CLAVE PÚBLICA</text><rect x="42" y="372" width="405" height="74" rx="12" class="c-chip"/><text x="64" y="417" class="c-tiny">04:A7:9C:2F:…:D8</text><text x="42" y="505" class="c-tiny">VÁLIDO DESDE · HASTA</text><path d="M42 535H445" class="c-wire"/><g id="document-ribbon"><circle cx="425" cy="580" r="54" fill="#133e3b" stroke="#6ee6cc" stroke-width="5"/><path d="M397 580L418 601L455 556" class="c-check"/></g></g>
      <g id="document-key" transform="translate(730 600)"><circle r="82" class="c-node"/><circle cx="-18" cy="-10" r="28" fill="none" stroke="#6ee6cc" stroke-width="9"/><path d="M8 -10H55M39 -10V8M55 -10V4" class="c-stroke"/></g>
      ""","Certificado digital con dominio emisor vigencia y clave pública")
    if i==2:
      return _svg("""
      <g id="ca-chain"><path d="M450 190V330M450 485V620" class="c-wire"/><circle cx="450" cy="145" r="90" class="c-node c-glow"/><circle cx="450" cy="405" r="96" class="c-node"/><circle cx="450" cy="700" r="82" class="c-node"/></g>
      <g id="root-ca" transform="translate(450 145)"><path d="M0 -45L14 -14L48 -7L24 18L30 52L0 35L-30 52L-24 18L-48 -7L-14 -14Z" fill="#f3c875"/><text x="0" y="105" text-anchor="middle" class="c-tiny">RAÍZ DE CONFIANZA</text></g>
      <g id="intermediate-ca" transform="translate(450 405)"><rect x="-75" y="-52" width="150" height="105" rx="20" class="c-panel"/><path d="M-35 -4L-5 25L42 -30" class="c-check"/><text x="0" y="91" text-anchor="middle" class="c-tiny">INTERMEDIA</text></g>
      <g id="site-cert" transform="translate(450 700)"><path d="M-58 -68H25L60 -33V55H-58Z" class="c-paper"/><text x="0" y="8" text-anchor="middle" class="c-green" font-size="20" font-weight="900">WEB</text><path d="M-30 32L-5 52L35 4" class="c-check" stroke-width="8"/><text x="0" y="120" text-anchor="middle" class="c-tiny">TU CERTIFICADO</text></g>
      <g id="ca-stamp"><circle cx="690" cy="300" r="60" fill="#123d38" stroke="#6ee6cc" stroke-width="5"/><path d="M658 300L681 323L724 275" class="c-check"/></g>
      ""","Cadena de confianza desde autoridad raíz hasta el certificado del sitio")
    if i==3:
      return _svg("""
      <g id="browser-check" transform="translate(110 220)"><rect width="680" height="430" rx="28" class="c-panel"/><path d="M0 76H680" stroke="#456273" stroke-width="4"/><circle cx="40" cy="38" r="10" fill="#ff7181"/><circle cx="75" cy="38" r="10" fill="#f4c875"/><circle cx="110" cy="38" r="10" fill="#70ebcd"/><rect x="155" y="18" width="490" height="42" rx="13" fill="#07121e"/><text x="180" y="47" class="c-tiny">https://tu-dominio.com</text><g id="browser-fields"><rect x="35" y="110" width="610" height="72" rx="14" class="c-chip"/><text x="60" y="155" class="c-muted">Nombre del dominio</text><text x="570" y="155" text-anchor="end" class="c-green" font-size="22" font-weight="800">COINCIDE</text><rect x="35" y="205" width="610" height="72" rx="14" class="c-chip"/><text x="60" y="250" class="c-muted">Emisor de confianza</text><text x="570" y="250" text-anchor="end" class="c-green" font-size="22" font-weight="800">VÁLIDO</text><rect x="35" y="300" width="610" height="72" rx="14" class="c-chip"/><text x="60" y="345" class="c-muted">Fecha de expiración</text><text x="570" y="345" text-anchor="end" class="c-green" font-size="22" font-weight="800">VIGENTE</text></g></g>
      <g id="browser-check-seal" transform="translate(450 735)"><circle r="65" fill="#123e3a" stroke="#6ee6cc" stroke-width="5"/><path d="M-33 0L-8 27L39 -32" class="c-check"/></g>
      <g id="scan-line"><path d="M160 335H740" stroke="#72f0d0" stroke-width="5" opacity=".8"/></g>
      ""","Navegador comprobando que dominio emisor y vigencia sean válidos")
    if i==4:
      return _svg("""
      <g id="handshake-ends"><circle cx="175" cy="400" r="112" class="c-node c-glow"/><circle cx="725" cy="400" r="112" class="c-node c-glow"/><rect x="95" y="360" width="160" height="80" rx="16" class="c-panel"/><text x="175" y="410" text-anchor="middle" class="c-bright">BROWSER</text><rect x="645" y="360" width="160" height="80" rx="16" class="c-panel"/><text x="725" y="410" text-anchor="middle" class="c-bright">SERVER</text><path d="M285 400H615" class="c-orbit"/></g>
      <g id="hello-packets"><rect x="300" y="250" width="300" height="65" rx="17" class="c-chip"/><text x="450" y="291" text-anchor="middle" class="c-bright">CLIENT HELLO</text><rect x="300" y="495" width="300" height="65" rx="17" class="c-chip"/><text x="450" y="536" text-anchor="middle" class="c-bright">CERTIFICATE</text><path d="M270 330L300 315L270 300M630 475L600 495L630 515" class="c-stroke"/></g>
      <g id="cert-spotlight"><circle cx="450" cy="650" r="76" fill="#113d3a" stroke="#70ebcd" stroke-width="5"/><path d="M410 650L438 678L492 615" class="c-check"/><text x="450" y="770" text-anchor="middle" class="c-tiny">IDENTIDAD DEL SERVIDOR VERIFICADA</text></g>
      ""","Intercambio de certificado entre navegador y servidor durante el inicio de TLS")
    if i==5:
      return _svg("""
      <g id="public-key" transform="translate(230 390)"><circle r="118" class="c-node c-glow"/><circle cx="-28" cy="-10" r="38" fill="none" stroke="#70ebcd" stroke-width="10"/><path d="M10 -10H84M58 -10V18M84 -10V12" class="c-stroke"/><text x="0" y="170" text-anchor="middle" class="c-bright">CLAVE PÚBLICA</text></g>
      <g id="private-key" transform="translate(670 390)"><circle r="118" class="c-node"/><rect x="-48" y="-18" width="96" height="83" rx="14" class="c-lock"/><path d="M-28 -18V-52A28 28 0 0 1 28 -52V-18" class="c-stroke"/><text x="0" y="170" text-anchor="middle" class="c-bright">CLAVE PRIVADA</text><text x="0" y="210" text-anchor="middle" class="c-tiny">SECRETA EN EL SERVIDOR</text></g>
      <g id="key-flow"><path d="M365 390H535" class="c-wire"/><path d="M505 365L535 390L505 415" class="c-stroke"/><g id="key-packet"><rect x="405" y="335" width="90" height="58" rx="13" class="c-chip"/><text x="450" y="372" text-anchor="middle" class="c-green" font-size="20" font-weight="900">TLS</text></g></g>
      <g id="key-bottom"><rect x="180" y="715" width="540" height="76" rx="19" class="c-panel"/><text x="450" y="762" text-anchor="middle" class="c-tiny">TLS NEGOCIA CLAVES DE SESIÓN</text></g>
      ""","Clave pública incluida en el certificado y clave privada protegida en el servidor")
    if i==6:
      return _svg("""
      <g id="secure-tunnel"><ellipse cx="450" cy="440" rx="365" ry="260" class="c-orbit"/><ellipse cx="450" cy="440" rx="290" ry="200" class="c-orbit"/><ellipse cx="450" cy="440" rx="210" ry="140" class="c-orbit"/><path d="M75 440H825" class="c-line"/></g>
      <g id="encrypted-packets"><rect x="105" y="320" width="135" height="70" rx="15" class="c-chip"/><text x="172" y="365" text-anchor="middle" class="c-bright">A8#2F</text><rect x="650" y="490" width="135" height="70" rx="15" class="c-chip"/><text x="717" y="535" text-anchor="middle" class="c-bright">Q7!9X</text><rect x="355" y="205" width="190" height="70" rx="15" class="c-chip"/><text x="450" y="250" text-anchor="middle" class="c-bright">CIFRADO</text><rect x="345" y="625" width="210" height="66" rx="15" class="c-chip"/><text x="450" y="668" text-anchor="middle" class="c-tiny">DATOS EN TRÁNSITO</text></g>
      <g id="data-shield" transform="translate(350 345)"><path d="M100 0L200 38V125Q200 225 100 280Q0 225 0 125V38Z" class="c-shield c-glow"/><path d="M52 135L86 170L151 95" class="c-check"/></g>
      <g id="data-sparks"><circle cx="130" cy="555" r="18" class="c-node"/><circle cx="770" cy="300" r="18" class="c-node"/><circle cx="450" cy="115" r="13" fill="#70ebcd"/><circle cx="450" cy="770" r="13" fill="#70ebcd"/></g>
      ""","Paquetes cifrados viajando por un túnel HTTPS con escudo")
    if i==7:
      return _svg("""
      <g id="validity-dashboard" transform="translate(90 185)"><rect width="720" height="500" rx="30" class="c-panel c-glow"/><text x="45" y="70" class="c-green" font-size="22" font-weight="900" letter-spacing="3">ESTADO DEL CERTIFICADO</text><rect x="42" y="110" width="636" height="100" rx="18" class="c-chip"/><circle cx="96" cy="160" r="27" fill="#174b42" stroke="#6ee6cc" stroke-width="3"/><path d="M80 160L92 174L115 145" class="c-check" stroke-width="6"/><text x="150" y="154" class="c-bright">Certificado activo</text><text x="150" y="185" class="c-tiny">tu-dominio.com</text><text x="45" y="275" class="c-muted">Vigencia restante</text><text x="650" y="275" text-anchor="end" class="c-gold" font-size="30" font-weight="900">27 DÍAS</text><rect x="45" y="302" width="630" height="23" rx="11" fill="#183a48"/><rect id="expiry-progress" x="45" y="302" width="445" height="23" rx="11" fill="#f0c775"/><rect x="45" y="365" width="630" height="90" rx="16" fill="#302a20" stroke="#d8ad66" stroke-width="3"/><text x="80" y="405" class="c-gold" font-size="20" font-weight="900">RECORDATORIO DE RENOVACIÓN</text><text x="80" y="437" class="c-tiny">Evita que caduque y cause alertas</text></g>
      <g id="clock" transform="translate(730 735)"><circle r="75" class="c-node"/><circle r="53" fill="none" stroke="#70ebcd" stroke-width="5"/><path d="M0 -34V0L28 18" class="c-stroke"/></g>
      <g id="calendar"><rect x="135" y="735" width="170" height="92" rx="17" class="c-chip"/><path d="M135 765H305M175 720V752M265 720V752" class="c-stroke" stroke-width="6"/><text x="220" y="805" text-anchor="middle" class="c-bright">RENOVAR</text></g>
      ""","Panel de certificado vigente con calendario de renovación")
    return _svg("""
    <g id="final-orbit"><circle cx="450" cy="440" r="345" class="c-orbit"/><circle cx="450" cy="440" r="275" class="c-orbit"/><path d="M105 440H795M450 95V785M205 195L695 685M695 195L205 685" class="c-line"/></g>
    <g id="final-nodes"><circle cx="450" cy="95" r="18" class="c-node"/><circle cx="795" cy="440" r="18" class="c-node"/><circle cx="450" cy="785" r="18" class="c-node"/><circle cx="105" cy="440" r="18" class="c-node"/></g>
    <g id="final-certificate" transform="translate(265 205)"><path d="M0 0H250L350 100V390H0Z" class="c-paper c-glow"/><path d="M250 0V100H350" fill="#1a4050" stroke="#7ae8d0" stroke-width="4"/><text x="35" y="65" class="c-green" font-size="21" font-weight="900">SSL / TLS</text><path d="M35 125H290M35 175H260M35 225H285" stroke="#496b7c" stroke-width="9" stroke-linecap="round"/><circle cx="175" cy="315" r="55" fill="#123e3b" stroke="#6ee6cc" stroke-width="5"/><path d="M145 315L166 338L207 288" class="c-check"/></g>
    <g id="final-shield" transform="translate(315 570)"><path d="M135 0L245 42V145Q245 280 135 355Q25 280 25 145V42Z" class="c-shield c-glow"/><path d="M77 170L117 210L193 125" class="c-check"/></g>
    <g id="final-stars"><path d="M150 235V295M120 265H180M750 565V625M720 595H780" class="c-stroke" stroke-width="5"/></g>
    <g id="final-url"><rect x="235" y="850" width="430" height="58" rx="29" class="c-chip"/><text x="450" y="888" text-anchor="middle" class="c-bright">https://tu-web.com</text></g>
    ""","Certificado digital junto a escudo de conexión HTTPS")

def _animation(i,start,end):
    s=f"#manual-scene-{i} "
    span=max(.6,end-start)
    plans=[
      [("#identity-orbits","scale:.7,rotation:-25,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:1.0,ease:'power3.out'",0),
       ("#identity-card","y:170,rotationY:18,scale:.82,autoAlpha:0","y:0,rotationY:0,scale:1,autoAlpha:1,duration:1.0,ease:'back.out(1.4)'",.2),
       ("#identity-seal","scale:0,rotation:-100","scale:1,rotation:0,duration:.7,ease:'elastic.out(1,.55)'",1.1),
       ("#identity-floats","y:55,autoAlpha:0","y:0,autoAlpha:1,duration:.65,stagger:.13,ease:'back.out(2)'",1.5)],
      [("#document","y:190,rotationY:20,autoAlpha:0","y:0,rotationY:0,autoAlpha:1,duration:1,ease:'power3.out'",0),
       ("#document-ribbon","scale:0,rotation:-90","scale:1,rotation:0,duration:.75,ease:'elastic.out(1,.5)'",1.0),
       ("#document-key","x:100,scale:.3,autoAlpha:0","x:0,scale:1,autoAlpha:1,duration:.7,ease:'back.out(1.8)'",1.4)],
      [("#ca-chain","scale:.7,autoAlpha:0","scale:1,autoAlpha:1,duration:.8,ease:'power3.out'",0),
       ("#root-ca","y:-80,autoAlpha:0","y:0,autoAlpha:1,duration:.6,ease:'back.out(1.7)'",.2),
       ("#intermediate-ca","x:-90,autoAlpha:0","x:0,autoAlpha:1,duration:.65,ease:'power3.out'",.8),
       ("#site-cert","y:90,autoAlpha:0","y:0,autoAlpha:1,duration:.7,ease:'power3.out'",1.35),
       ("#ca-stamp","scale:0,rotation:-120","scale:1,rotation:0,duration:.7,ease:'elastic.out(1,.5)'",1.9)],
      [("#browser-check","y:130,scale:.88,autoAlpha:0","y:0,scale:1,autoAlpha:1,duration:.9,ease:'power3.out'",0),
       ("#browser-fields rect","x:-55,autoAlpha:0","x:0,autoAlpha:1,duration:.5,stagger:.2,ease:'power2.out'",.65),
       ("#browser-check-seal","scale:0,rotation:-45","scale:1,rotation:0,duration:.65,ease:'elastic.out(1,.5)'",1.75),
       ("#scan-line","y:-50,autoAlpha:0","y:50,autoAlpha:1,duration:1.0,repeat:1,yoyo:true,ease:'sine.inOut'",1.0)],
      [("#handshake-ends","scale:.7,autoAlpha:0","scale:1,autoAlpha:1,duration:.8,ease:'power3.out'",0),
       ("#hello-packets rect","x:-130,autoAlpha:0","x:0,autoAlpha:1,duration:.55,stagger:.5,ease:'power3.out'",.5),
       ("#cert-spotlight","scale:0,autoAlpha:0","scale:1,autoAlpha:1,duration:.75,ease:'elastic.out(1,.5)'",1.6),
       ("#handshake-ends circle","scale:1.08,transformOrigin:'50% 50%'","scale:1,duration:.5,repeat:2,yoyo:true,ease:'sine.inOut'",1.2)],
      [("#public-key","x:-120,autoAlpha:0","x:0,autoAlpha:1,duration:.8,ease:'power3.out'",0),
       ("#private-key","x:120,autoAlpha:0","x:0,autoAlpha:1,duration:.8,ease:'power3.out'",.15),
       ("#key-packet","scale:0,rotation:-25","scale:1,rotation:0,duration:.65,ease:'back.out(2)'",1.0),
       ("#key-bottom","y:70,autoAlpha:0","y:0,autoAlpha:1,duration:.65,ease:'power3.out'",1.7)],
      [("#secure-tunnel","scale:.55,rotation:-18,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:1,ease:'power2.out'",0),
       ("#encrypted-packets rect","x:-130,y:28,autoAlpha:0","x:0,y:0,autoAlpha:1,duration:.6,stagger:.18,ease:'power2.out'",.5),
       ("#data-shield","scale:.3,rotation:-20,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:.85,ease:'back.out(1.7)'",1.1),
       ("#data-sparks","scale:0,autoAlpha:0","scale:1,autoAlpha:1,duration:.55,stagger:.12,ease:'back.out(2)'",1.7),
       ("#encrypted-packets","x:26,duration:.5,repeat:3,yoyo:true,ease:'sine.inOut'","",1.5)],
      [("#validity-dashboard","x:150,autoAlpha:0","x:0,autoAlpha:1,duration:.85,ease:'power3.out'",0),
       ("#expiry-progress","scaleX:.08,transformOrigin:'left center'","scaleX:1,duration:1.1,ease:'power2.out'",.8),
       ("#clock","scale:0,rotation:-50,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:.7,ease:'elastic.out(1,.5)'",1.4),
       ("#calendar","y:65,autoAlpha:0","y:0,autoAlpha:1,duration:.6,ease:'back.out(1.8)'",1.9),
       ("#clock","rotation:12,duration:.16,repeat:4,yoyo:true,ease:'sine.inOut'","",2.2)],
      [("#final-orbit","scale:.6,rotation:-30,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:1.1,ease:'power3.out'",0),
       ("#final-nodes","scale:0,autoAlpha:0","scale:1,autoAlpha:1,duration:.5,stagger:.1,ease:'back.out(2)'",.45),
       ("#final-certificate","y:120,rotationY:20,autoAlpha:0","y:0,rotationY:0,autoAlpha:1,duration:.9,ease:'power3.out'",.85),
       ("#final-shield","scale:.2,y:90,autoAlpha:0","scale:1,y:0,autoAlpha:1,duration:.85,ease:'back.out(1.7)'",1.5),
       ("#final-stars","scale:.2,autoAlpha:0","scale:1,autoAlpha:1,duration:.55,ease:'back.out(2)'",2.0),
       ("#final-url","y:65,autoAlpha:0","y:0,autoAlpha:1,duration:.6,ease:'power3.out'",2.25),
       ("#final-orbit","rotation:12,duration:"+str(max(1.0,span-2.6))+",ease:'none'","",1.5)]
    ]
    out=[]
    for selector,frm,to,offset in plans[i]:
      if to:
        out.append(f'tl.fromTo("{s}{selector}",{{{frm}}},{{{to}}},{start+offset:.3f});')
      else:
        out.append(f'tl.to("{s}{selector}",{{{frm}}},{start+offset:.3f});')
    return "".join(out)
