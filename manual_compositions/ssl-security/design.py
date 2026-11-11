"""Composición SSL/TLS con escenas propias, motion graphics y microanimaciones."""
from __future__ import annotations

def build_design(duration, words, groups, title):
    cuts=[0,.105,.215,.325,.435,.545,.655,.765,.88,1]
    copy=[
      ("ALERTA WEB","¿TU WEB PARECE INSEGURA?","Una advertencia puede hacer que el visitante se marche"),
      ("DOS CAMINOS","HTTP NO ES LO MISMO QUE HTTPS","La conexión segura protege los datos durante el trayecto"),
      ("IDENTIDAD DIGITAL","¿QUIÉN ESTÁ DETRÁS DE TU WEB?","El certificado ayuda a verificar la identidad del sitio"),
      ("CONEXIÓN TLS","NAVEGADOR Y SERVIDOR SE IDENTIFICAN","El protocolo negocia una conexión cifrada"),
      ("DATOS CIFRADOS","TUS DATOS VIAJAN PROTEGIDOS","La información no circula como texto legible"),
      ("FORMULARIOS","PROTEGE LOS DATOS EN TRÁNSITO","Contraseñas y formularios viajan por HTTPS"),
      ("CONFIGURACIÓN","INSTALARLO NO ES TODO","Dominio, redirección y configuración deben estar correctos"),
      ("MANTENIMIENTO","QUE NO TE PILLE LA FECHA","Vigila la caducidad y automatiza la renovación"),
      ("CIERRE","DALE A TU WEB UNA CONEXIÓN SEGURA","Configura HTTPS con cloudservicegm")
    ]
    scenes=[]
    for i,(label,headline,detail) in enumerate(copy):
        a,b=duration*cuts[i],duration*cuts[i+1]
        scenes.append({"start":round(a,3),"end":round(b,3),"label":label,
          "headline":headline,"detail":detail,"markup":_visual(i),"animation":_animation(i,a,b)})
    sounds=[
      ("whoosh-medium-soft",.15,-10),("notification-error-soft",duration*.105,-7),
      ("digital-glitch-subtle",duration*.16,-12),("swish-medium",duration*.22,-9),
      ("digital-power-up",duration*.33,-9),("shimmer-short-soft",duration*.39,-12),
      ("tone-step-2",duration*.445,-12),("digital-process-subtle",duration*.51,-10),
      ("data-chart-reveal",duration*.555,-11),("click-tap-medium",duration*.665,-10),
      ("mechanical-switch-light",duration*.775,-9),("notification-success-soft",duration*.89,-8),
      ("sting-warm-short",duration*.965,-12)]
    events=[{"id":sid,"moment":round(t,3),"gain_db":gain,"label":sid}
            for sid,t,gain in sounds if 0<=t<duration]
    return {"css":_css(),"scenes":scenes,"sfx_events":events}

def _css():
    return r"""
    #root{background:radial-gradient(ellipse at 50% 22%,rgba(25,79,92,.5),transparent 42%),radial-gradient(ellipse at 12% 74%,rgba(19,63,84,.22),transparent 38%),linear-gradient(155deg,#07111d,#081522 52%,#050a13)}
    #root:before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.2;background-image:linear-gradient(rgba(108,221,209,.1) 1px,transparent 1px),linear-gradient(90deg,rgba(108,221,209,.1) 1px,transparent 1px);background-size:72px 72px;mask-image:linear-gradient(to bottom,transparent,#000 18%,#000 86%,transparent)}
    .manual-scene{background:radial-gradient(ellipse at 50% 58%,rgba(22,75,91,.3),transparent 66%)}
    .manual-scene-kicker{color:#77f0d1;text-shadow:0 0 25px rgba(55,221,188,.48)}
    .manual-scene-headline{color:#f4fbff;text-shadow:0 7px 34px #000;letter-spacing:-2.4px}
    .manual-scene-detail{color:#b7ccd9;text-shadow:0 3px 14px #000}
    .manual-scene-index{color:#75e9ce}
    .ssl-art{position:absolute;left:0;right:0;top:430px;height:980px;display:flex;align-items:center;justify-content:center}
    .ssl-art svg{width:100%;height:100%;overflow:visible}
    .ssl-orbit{fill:none;stroke:#397d7c;stroke-width:2;stroke-dasharray:8 13}
    .ssl-line{fill:none;stroke:#5be1c1;stroke-width:3;stroke-dasharray:12 14}
    .ssl-node{fill:#0b1927;stroke:#65e4c5;stroke-width:4}
    .ssl-panel{fill:#0d2030;stroke:#426d7d;stroke-width:4}
    .ssl-chip{fill:#112b38;stroke:#3c897c;stroke-width:2}
    .ssl-warning{fill:#311b29;stroke:#ff6b7c;stroke-width:4}
    .ssl-red{fill:#ff6a7d}.ssl-green{fill:#70ebcd}
    .ssl-white{fill:#f2fbff}
    .ssl-muted{fill:#a9c3d3;font:600 24px Arial}
    .ssl-tiny{fill:#b9d0df;font:700 19px Arial}
    .ssl-bright{fill:#effffc;font:800 30px Arial}
    .ssl-scene-label{fill:#6ee6cc;font:800 21px Arial;letter-spacing:4px}
    .ssl-stroke{fill:none;stroke:#6ee6cc;stroke-width:9;stroke-linecap:round;stroke-linejoin:round}
    .ssl-check{fill:none;stroke:#6ee6cc;stroke-width:13;stroke-linecap:round;stroke-linejoin:round}
    .ssl-redline{fill:none;stroke:#ff6477;stroke-width:7;stroke-linecap:round}
    .ssl-shield{fill:#102d3a;stroke:#6ee6cc;stroke-width:8;stroke-linejoin:round}
    .ssl-lock{fill:#0a1a28;stroke:#6ee6cc;stroke-width:8}
    .ssl-packet{fill:#173949;stroke:#80efda;stroke-width:3}
    .ssl-glow{filter:drop-shadow(0 0 26px #35e4be77)}
    .ssl-glow-red{filter:drop-shadow(0 0 22px #ff647766)}
    .ssl-bar{fill:#183a48}.ssl-bar-fill{fill:#65e4c5}
    """

def _svg(body, label):
    return f'<div class="ssl-art"><svg viewBox="0 0 900 900" role="img" aria-label="{label}">{body}</svg></div>'

def _visual(i):
    if i==0:
        return _svg("""
        <defs><linearGradient id="danger"><stop stop-color="#ff536c"/><stop offset="1" stop-color="#ffad68"/></linearGradient></defs>
        <g id="orbit"><circle cx="450" cy="455" r="345" class="ssl-orbit"/><circle cx="450" cy="455" r="292" class="ssl-orbit"/><path d="M95 455H805M450 100V810" class="ssl-line" opacity=".35"/></g>
        <g id="browser" transform="translate(105 190)"><rect width="690" height="450" rx="28" class="ssl-panel ssl-glow-red"/><path d="M0 75H690" stroke="#405267" stroke-width="4"/><circle cx="40" cy="38" r="11" fill="#ff6978"/><circle cx="78" cy="38" r="11" fill="#ffbf69"/><circle cx="116" cy="38" r="11" fill="#6ee6cc"/><rect x="170" y="18" width="475" height="42" rx="12" fill="#06111d"/><text x="192" y="47" class="ssl-tiny">http://tu-pagina.com</text><rect x="34" y="110" width="622" height="300" rx="20" fill="#091522"/><g id="warning"><path d="M345 155L432 307H258Z" fill="url(#danger)"/><path d="M345 197V248M345 277V280" stroke="#231a22" stroke-width="13" stroke-linecap="round"/></g><text x="345" y="362" text-anchor="middle" class="ssl-bright">SITIO NO SEGURO</text></g>
        <g id="alerts"><circle cx="165" cy="690" r="42" class="ssl-warning"/><path d="M165 667V696M165 712V715" class="ssl-redline"/><circle cx="755" cy="270" r="33" class="ssl-warning"/><path d="M755 251V274M755 288V290" class="ssl-redline"/><rect x="560" y="700" width="170" height="62" rx="18" class="ssl-chip"/><text x="645" y="740" text-anchor="middle" class="ssl-red" font-size="22" font-weight="800">HTTP ONLY</text></g>
        <path id="broken" d="M170 770H350L385 738L420 770H730" class="ssl-redline" stroke-dasharray="12 12"/>""","Navegador web con alerta de conexión no segura")
    if i==1:
        return _svg("""
        <g id="http" transform="translate(42 225)"><rect width="365" height="420" rx="30" fill="#251927" stroke="#ff6978" stroke-width="5"/><rect x="24" y="24" width="317" height="64" rx="15" fill="#3b202d"/><text x="182" y="70" text-anchor="middle" class="ssl-red" font-size="48" font-weight="900">HTTP</text><g id="leaks"><rect x="66" y="135" width="230" height="53" rx="13" class="ssl-warning"/><text x="181" y="170" text-anchor="middle" class="ssl-tiny">password=1234</text><rect x="66" y="218" width="230" height="53" rx="13" class="ssl-warning"/><text x="181" y="253" text-anchor="middle" class="ssl-tiny">email@web.com</text><rect x="66" y="301" width="230" height="53" rx="13" class="ssl-warning"/><text x="181" y="336" text-anchor="middle" class="ssl-tiny">datos visibles</text></g><path d="M110 385L255 385M110 385L145 350M110 385L145 420" class="ssl-redline"/></g>
        <g id="https" transform="translate(493 225)"><rect width="365" height="420" rx="30" fill="#102b2b" stroke="#6ee6cc" stroke-width="5"/><rect x="24" y="24" width="317" height="64" rx="15" fill="#17463f"/><text x="182" y="70" text-anchor="middle" class="ssl-green" font-size="48" font-weight="900">HTTPS</text><g id="locked-packets"><rect x="66" y="135" width="230" height="53" rx="13" class="ssl-chip"/><text x="181" y="170" text-anchor="middle" class="ssl-bright">a8F#29!x</text><rect x="66" y="218" width="230" height="53" rx="13" class="ssl-chip"/><text x="181" y="253" text-anchor="middle" class="ssl-bright">Qp7@Lm4</text><rect x="66" y="301" width="230" height="53" rx="13" class="ssl-chip"/><text x="181" y="336" text-anchor="middle" class="ssl-bright">••••••••</text></g><g id="mini-lock" transform="translate(182 385)"><rect x="-31" y="-2" width="62" height="50" rx="9" class="ssl-lock"/><path d="M-20 -2V-20A20 20 0 0 1 20 -20V-2" class="ssl-stroke" stroke-width="6"/></g></g>
        <g id="arrow"><path d="M410 440H490M465 413L492 440L465 467" class="ssl-stroke"/></g><g id="versus"><circle cx="450" cy="710" r="54" fill="#102d3a" stroke="#75ead0" stroke-width="3"/><text x="450" y="721" text-anchor="middle" class="ssl-bright">VS</text></g>""","Comparación entre HTTP y HTTPS")
    if i==2:
        return _svg("""
        <g id="cert-orbit"><circle cx="450" cy="465" r="315" class="ssl-orbit"/><circle cx="450" cy="465" r="260" class="ssl-orbit"/></g>
        <g id="certificate" transform="translate(185 125)"><path d="M0 0H390L515 125V645H0Z" fill="#10283a" stroke="#6ee6cc" stroke-width="5" class="ssl-glow"/><path d="M390 0V125H515" fill="#183d4b" stroke="#6ee6cc" stroke-width="4"/><text x="45" y="75" class="ssl-scene-label">CERTIFICADO DIGITAL</text><rect x="42" y="145" width="420" height="72" rx="14" class="ssl-chip"/><text x="66" y="190" class="ssl-bright">tu-dominio.com</text><text x="46" y="272" class="ssl-tiny">EMITIDO POR</text><text x="46" y="316" class="ssl-bright">Autoridad certificadora</text><path d="M46 352H440M46 402H380M46 452H420" stroke="#496b7c" stroke-width="8" stroke-linecap="round"/><g id="seal" transform="translate(282 545)"><circle r="80" fill="#123e3e" stroke="#77efd1" stroke-width="6"/><path d="M-37 0L-8 30L43 -32" class="ssl-check"/><path d="M-45 70L-62 120L0 96L62 120L45 70" fill="#226b60" stroke="#77efd1" stroke-width="3"/></g></g>
        <g id="fingerprint" transform="translate(730 300)"><circle r="84" class="ssl-node"/><path d="M-42 20Q-43 -45 0 -48Q43 -45 42 20M-25 39Q-28 -20 0 -22Q28 -20 25 39M0 -3V62M-54 -4Q-56 -72 0 -73Q56 -72 54 -4" class="ssl-line"/></g>
        <g id="verified"><rect x="545" y="650" width="245" height="64" rx="18" class="ssl-chip"/><text x="667" y="690" text-anchor="middle" class="ssl-tiny">IDENTIDAD VALIDADA</text><circle cx="115" cy="690" r="18" fill="#74ebcf"/><circle cx="115" cy="690" r="42" class="ssl-orbit"/></g>""","Certificado digital de identidad del sitio")
    if i==3:
        return _svg("""
        <g id="network"><path d="M190 365H710M190 425H710M190 485H710" class="ssl-orbit"/><circle cx="180" cy="425" r="112" class="ssl-node ssl-glow"/><circle cx="720" cy="425" r="112" class="ssl-node ssl-glow"/><rect x="105" y="380" width="150" height="85" rx="16" class="ssl-panel"/><text x="180" y="430" text-anchor="middle" class="ssl-bright">BROWSER</text><rect x="645" y="380" width="150" height="85" rx="16" class="ssl-panel"/><text x="720" y="430" text-anchor="middle" class="ssl-bright">SERVER</text></g>
        <g id="packets"><rect x="315" y="285" width="185" height="60" rx="16" class="ssl-chip"/><text x="407" y="324" text-anchor="middle" class="ssl-tiny">1 · HELLO</text><rect x="400" y="475" width="195" height="60" rx="16" class="ssl-chip"/><text x="497" y="514" text-anchor="middle" class="ssl-tiny">2 · CERTIFICADO</text><rect x="310" y="600" width="220" height="60" rx="16" class="ssl-chip"/><text x="420" y="639" text-anchor="middle" class="ssl-tiny">3 · CLAVES DE SESIÓN</text></g>
        <g id="lock" transform="translate(450 755)"><circle r="67" fill="#123e3e" stroke="#72ebcd" stroke-width="4"/><rect x="-30" y="-5" width="60" height="48" rx="9" class="ssl-lock"/><path d="M-19 -5V-23A19 19 0 0 1 19 -23V-5" class="ssl-stroke" stroke-width="6"/></g>
        <g id="arrows"><path d="M295 300L325 285L295 270M595 490L625 475L595 460M305 615L275 600L305 585" class="ssl-stroke" stroke-width="6"/></g>""","Intercambio seguro entre navegador y servidor durante TLS")
    if i==4:
        return _svg("""
        <g id="tunnel"><ellipse cx="450" cy="445" rx="365" ry="250" class="ssl-orbit"/><ellipse cx="450" cy="445" rx="295" ry="198" class="ssl-orbit"/><ellipse cx="450" cy="445" rx="210" ry="140" class="ssl-orbit"/><path d="M80 445H820M450 160V730" class="ssl-line"/></g>
        <g id="data-packets"><rect x="120" y="330" width="128" height="72" rx="16" class="ssl-packet"/><text x="184" y="375" text-anchor="middle" class="ssl-bright">A9#4</text><rect x="650" y="500" width="128" height="72" rx="16" class="ssl-packet"/><text x="714" y="545" text-anchor="middle" class="ssl-bright">K2!8</text><rect x="360" y="215" width="180" height="72" rx="16" class="ssl-packet"/><text x="450" y="260" text-anchor="middle" class="ssl-bright">X7#Q2</text><rect x="345" y="625" width="210" height="70" rx="16" class="ssl-packet"/><text x="450" y="670" text-anchor="middle" class="ssl-bright">ENCRYPTED</text></g>
        <g id="shield" transform="translate(350 350)"><path d="M100 0L200 38V125Q200 225 100 280Q0 225 0 125V38Z" class="ssl-shield ssl-glow"/><path d="M52 135L86 170L151 95" class="ssl-check"/></g>
        <g id="nodes"><circle cx="135" cy="560" r="20" class="ssl-node"/><circle cx="765" cy="300" r="20" class="ssl-node"/><circle cx="450" cy="115" r="14" fill="#71ebcf"/><circle cx="450" cy="775" r="14" fill="#71ebcf"/></g>
        <g id="data-lock" transform="translate(450 770)"><rect x="-43" y="-8" width="86" height="70" rx="14" class="ssl-lock"/><path d="M-28 -8V-32A28 28 0 0 1 28 -32V-8" class="ssl-stroke"/></g>""","Flujo de paquetes cifrados en un túnel de datos")
    if i==5:
        return _svg("""
        <g id="form" transform="translate(100 135)"><rect width="700" height="560" rx="30" class="ssl-panel ssl-glow"/><path d="M0 82H700" stroke="#3c6172" stroke-width="3"/><circle cx="40" cy="40" r="10" fill="#70e9cd"/><circle cx="75" cy="40" r="10" fill="#f2c16b"/><circle cx="110" cy="40" r="10" fill="#ff7180"/><text x="165" y="51" class="ssl-bright">CHECKOUT SEGURO</text><text x="48" y="145" class="ssl-muted">Correo electrónico</text><rect x="48" y="165" width="600" height="58" rx="12" class="ssl-chip"/><text x="72" y="203" class="ssl-tiny">cliente@ejemplo.com</text><text x="48" y="278" class="ssl-muted">Contraseña</text><rect x="48" y="298" width="600" height="58" rx="12" class="ssl-chip"/><text x="72" y="337" class="ssl-bright">••••••••••••</text><rect x="48" y="405" width="600" height="85" rx="16" fill="#125447"/><text x="348" y="458" text-anchor="middle" class="ssl-bright">ENVIAR DE FORMA SEGURA</text></g>
        <g id="form-lock" transform="translate(730 720)"><circle r="94" fill="#0e302e" stroke="#6ee6cc" stroke-width="5"/><rect x="-37" y="-2" width="74" height="64" rx="11" class="ssl-lock"/><path d="M-23 -2V-26A23 23 0 0 1 23 -26V-2" class="ssl-stroke"/></g>
        <g id="form-packets"><rect x="55" y="745" width="125" height="54" rx="15" class="ssl-chip"/><text x="117" y="780" text-anchor="middle" class="ssl-tiny">TLS</text><rect x="220" y="745" width="175" height="54" rx="15" class="ssl-chip"/><text x="307" y="780" text-anchor="middle" class="ssl-tiny">DATOS CIFRADOS</text></g>""","Formulario web con datos personales protegidos por HTTPS")
    if i==6:
        return _svg("""
        <g id="config" transform="translate(95 145)"><rect width="710" height="590" rx="30" class="ssl-panel"/><rect width="710" height="88" rx="25" fill="#15384a"/><text x="42" y="56" class="ssl-bright">CONFIGURACIÓN HTTPS</text><g id="checks"><rect x="38" y="125" width="634" height="95" rx="16" class="ssl-chip"/><circle cx="91" cy="172" r="23" fill="#174b42"/><path d="M78 172L88 183L105 160" class="ssl-check" stroke-width="6"/><text x="140" y="165" class="ssl-bright">Dominio correcto</text><text x="140" y="196" class="ssl-tiny">El certificado corresponde al sitio</text><rect x="38" y="245" width="634" height="95" rx="16" class="ssl-chip"/><circle cx="91" cy="292" r="23" fill="#174b42"/><path d="M78 292L88 303L105 280" class="ssl-check" stroke-width="6"/><text x="140" y="285" class="ssl-bright">Redirección a HTTPS</text><text x="140" y="316" class="ssl-tiny">HTTP dirige a la conexión segura</text><rect x="38" y="365" width="634" height="95" rx="16" class="ssl-chip"/><circle cx="91" cy="412" r="23" fill="#174b42"/><path d="M78 412L88 423L105 400" class="ssl-check" stroke-width="6"/><text x="140" y="405" class="ssl-bright">Contenido mixto revisado</text><text x="140" y="436" class="ssl-tiny">Recursos cargados de forma segura</text><rect x="38" y="490" width="634" height="62" rx="14" fill="#12473f"/><text x="355" y="530" text-anchor="middle" class="ssl-bright">CADENA SSL/TLS CORRECTA</text></g></g>
        <g id="domain-nodes"><circle cx="160" cy="790" r="28" class="ssl-node"/><circle cx="450" cy="790" r="28" class="ssl-node"/><circle cx="740" cy="790" r="28" class="ssl-node"/><path d="M188 790H422M478 790H712" class="ssl-line"/></g>""","Panel de configuración correcta de HTTPS")
    if i==7:
        return _svg("""
        <g id="dashboard" transform="translate(90 175)"><rect width="720" height="515" rx="30" class="ssl-panel ssl-glow"/><text x="45" y="68" class="ssl-scene-label">MONITOR SSL / TLS</text><rect x="42" y="100" width="636" height="105" rx="18" class="ssl-chip"/><circle cx="96" cy="152" r="27" fill="#174b42" stroke="#6ee6cc" stroke-width="3"/><path d="M81 152L92 164L113 139" class="ssl-check" stroke-width="6"/><text x="152" y="146" class="ssl-bright">Certificado activo</text><text x="152" y="180" class="ssl-tiny">tu-dominio.com · válido</text><text x="45" y="270" class="ssl-muted">Tiempo restante</text><text x="650" y="270" text-anchor="end" class="ssl-green" font-size="30" font-weight="900">27 DÍAS</text><rect x="45" y="295" width="630" height="24" rx="12" class="ssl-bar"/><rect id="progress" x="45" y="295" width="470" height="24" rx="12" class="ssl-bar-fill"/><rect x="45" y="365" width="630" height="95" rx="16" fill="#2b2630" stroke="#f0b86b" stroke-width="3"/><text x="78" y="407" class="ssl-tiny">RENOVACIÓN AUTOMÁTICA</text><text x="78" y="440" class="ssl-bright">Activada · próxima revisión programada</text></g>
        <g id="bell"><circle cx="720" cy="730" r="68" fill="#173e43" stroke="#6ee6cc" stroke-width="5"/><path d="M720 681V735M720 760V764" class="ssl-stroke"/><path d="M690 737Q690 690 720 690Q750 690 750 737L765 755H675Z" fill="#1c5b54" stroke="#6ee6cc" stroke-width="4"/></g>
        <g id="alert"><circle cx="190" cy="735" r="35" fill="#322b20" stroke="#edbd72" stroke-width="4"/><path d="M190 714V738M190 752V754" stroke="#ffdb9d" stroke-width="7" stroke-linecap="round"/></g>""","Panel de vigencia y renovación del certificado")
    return _svg("""
    <g id="globe"><circle cx="450" cy="440" r="340" class="ssl-orbit"/><circle cx="450" cy="440" r="275" class="ssl-orbit"/><circle cx="450" cy="440" r="205" class="ssl-orbit"/><path d="M110 440H790M450 100V780M210 200L690 680M690 200L210 680" class="ssl-line" opacity=".65"/></g>
    <g id="nodes"><circle cx="450" cy="100" r="20" class="ssl-node"/><circle cx="790" cy="440" r="20" class="ssl-node"/><circle cx="450" cy="780" r="20" class="ssl-node"/><circle cx="110" cy="440" r="20" class="ssl-node"/><circle cx="210" cy="200" r="13" fill="#6ee6cc"/><circle cx="690" cy="680" r="13" fill="#6ee6cc"/></g>
    <g id="shield" transform="translate(275 170)"><path d="M175 0L330 58V205Q330 395 175 500Q20 395 20 205V58Z" class="ssl-shield ssl-glow"/><path d="M95 245L150 300L258 175" class="ssl-check"/></g>
    <g id="final-lock" transform="translate(450 730)"><rect x="-42" y="-15" width="84" height="65" rx="13" class="ssl-lock"/><path d="M-27 -15V-40A27 27 0 0 1 27 -40V-15" class="ssl-stroke"/></g>
    <g id="url"><rect x="230" y="805" width="440" height="62" rx="31" class="ssl-chip"/><circle cx="270" cy="836" r="10" fill="#6ee6cc"/><text x="300" y="845" class="ssl-bright">https://tu-web.com</text></g>
    <g id="sparkles"><path d="M125 285V345M95 315H155M760 570V630M730 600H790M735 170V220M710 195H760" class="ssl-stroke" stroke-width="5"/></g>
    ""","Escudo digital y sitio protegido mediante HTTPS")

def _animation(i,start,end):
    s=f"#manual-scene-{i} "
    span=max(.5,end-start)
    plans=[
      [
       ('#orbit','scale:.72,rotation:-28,autoAlpha:0','scale:1,rotation:0,autoAlpha:1,duration:1.1,ease:"power3.out"',0),
       ('#browser','y:145,rotationY:18,scale:.82,autoAlpha:0','y:0,rotationY:0,scale:1,autoAlpha:1,duration:.9,ease:"back.out(1.4)"',.15),
       ('#warning','scale:0,rotation:-38,transformOrigin:"50% 50%"','scale:1,rotation:0,duration:.6,ease:"elastic.out(1,.55)"',.95),
       ('#alerts','y:55,autoAlpha:0','y:0,autoAlpha:1,duration:.6,stagger:.13,ease:"back.out(1.8)"',1.25),
       ('#broken','scaleX:.05,transformOrigin:"left center"','scaleX:1,duration:.7,ease:"power3.out"',1.65),
       ('#orbit','rotation:14,duration:'+str(max(1.1,span-1.8)) + ',ease:"none"','',1.0)
      ],
      [
       ('#http','x:-250,rotation:-8,autoAlpha:0','x:0,rotation:0,autoAlpha:1,duration:.75,ease:"power3.out"',0),
       ('#https','x:250,rotation:8,autoAlpha:0','x:0,rotation:0,autoAlpha:1,duration:.75,ease:"power3.out"',.12),
       ('#leaks rect','x:-55,autoAlpha:0','x:0,autoAlpha:1,duration:.4,stagger:.13,ease:"power2.out"',.7),
       ('#locked-packets rect','x:55,autoAlpha:0','x:0,autoAlpha:1,duration:.4,stagger:.13,ease:"power2.out"',.95),
       ('#mini-lock','scale:0,rotation:-30','scale:1,rotation:0,duration:.6,ease:"elastic.out(1,.5)"',1.65),
       ('#arrow','scale:0,transformOrigin:"50% 50%"','scale:1,duration:.5,ease:"back.out(2)"',1.35),
       ('#versus','scale:0,autoAlpha:0','scale:1,autoAlpha:1,duration:.5,ease:"back.out(2)"',2.1)
      ],
      [
       ('#cert-orbit','scale:.6,rotation:-30,autoAlpha:0','scale:1,rotation:0,autoAlpha:1,duration:1,ease:"power3.out"',0),
       ('#certificate','y:185,rotationY:22,autoAlpha:0','y:0,rotationY:0,autoAlpha:1,duration:1,ease:"power3.out"',.2),
       ('#seal','scale:0,rotation:-120','scale:1,rotation:0,duration:.75,ease:"elastic.out(1,.55)"',1.15),
       ('#fingerprint','x:95,scale:.2,autoAlpha:0','x:0,scale:1,autoAlpha:1,duration:.7,ease:"back.out(1.8)"',1.35),
       ('#verified','y:70,autoAlpha:0','y:0,autoAlpha:1,duration:.6,ease:"power3.out"',2.05),
       ('#fingerprint','rotation:360,duration:'+str(max(1,span-2.1))+',ease:"none"','',2.1)
      ],
      [
       ('#network','scale:.7,autoAlpha:0','scale:1,autoAlpha:1,duration:.8,ease:"power3.out"',0),
       ('#packets rect','x:-125,autoAlpha:0','x:0,autoAlpha:1,duration:.5,stagger:.42,ease:"power3.out"',.65),
       ('#arrows','scale:.4,autoAlpha:0,transformOrigin:"50% 50%"','scale:1,autoAlpha:1,duration:.6,ease:"back.out(1.7)"',1),
       ('#lock','scale:0,rotation:35,autoAlpha:0','scale:1,rotation:0,autoAlpha:1,duration:.7,ease:"elastic.out(1,.5)"',2),
       ('#network circle','scale:1.08,transformOrigin:"50% 50%"','scale:1,duration:.55,repeat:2,yoyo:true,ease:"sine.inOut"',1.5)
      ],
      [
       ('#tunnel','scale:.55,rotation:-18,autoAlpha:0','scale:1,rotation:0,autoAlpha:1,duration:1,ease:"power2.out"',0),
       ('#data-packets rect','x:-145,y:32,autoAlpha:0','x:0,y:0,autoAlpha:1,duration:.6,stagger:.2,ease:"power2.out"',.5),
       ('#shield','scale:.3,rotation:-22,autoAlpha:0','scale:1,rotation:0,autoAlpha:1,duration:.85,ease:"back.out(1.7)"',1.1),
       ('#nodes','scale:0,autoAlpha:0','scale:1,autoAlpha:1,duration:.5,stagger:.12,ease:"back.out(2)"',1.55),
       ('#data-lock','y:90,autoAlpha:0','y:0,autoAlpha:1,duration:.6,ease:"back.out(2)"',2),
       ('#data-packets','x:30,duration:.45,repeat:3,yoyo:true,ease:"sine.inOut"','',1.4)
      ],
      [
       ('#form','y:155,scale:.86,autoAlpha:0','y:0,scale:1,autoAlpha:1,duration:.95,ease:"power3.out"',0),
       ('#form rect','scaleX:.72,transformOrigin:"left center",autoAlpha:.5','scaleX:1,autoAlpha:1,duration:.48,stagger:.12,ease:"power2.out"',.55),
       ('#form-lock','scale:0,rotation:35','scale:1,rotation:0,duration:.72,ease:"elastic.out(1,.55)"',1.25),
       ('#form-packets','x:-90,autoAlpha:0','x:0,autoAlpha:1,duration:.6,ease:"power3.out"',1.75),
       ('#form-lock','scale:1.08,duration:.38,repeat:3,yoyo:true,ease:"sine.inOut"','',2.15)
      ],
      [
       ('#config','x:160,rotationY:-14,autoAlpha:0','x:0,rotationY:0,autoAlpha:1,duration:.9,ease:"power3.out"',0),
       ('#checks rect','x:-45,autoAlpha:0','x:0,autoAlpha:1,duration:.48,stagger:.2,ease:"power2.out"',.55),
       ('#checks circle','scale:0','scale:1,duration:.4,stagger:.2,ease:"back.out(2)"',.9),
       ('#domain-nodes circle','scale:0,autoAlpha:0','scale:1,autoAlpha:1,duration:.42,stagger:.14,ease:"elastic.out(1,.5)"',1.9),
       ('#domain-nodes path','scaleX:0,transformOrigin:"left center"','scaleX:1,duration:.6,ease:"power3.out"',2.1)
      ],
      [
       ('#dashboard','x:150,autoAlpha:0','x:0,autoAlpha:1,duration:.85,ease:"power3.out"',0),
       ('#progress','scaleX:.08,transformOrigin:"left center"','scaleX:1,duration:1.1,ease:"power2.out"',.85),
       ('#bell','scale:0,rotation:-35,autoAlpha:0','scale:1,rotation:0,autoAlpha:1,duration:.7,ease:"elastic.out(1,.5)"',1.35),
       ('#alert','scale:0,autoAlpha:0','scale:1,autoAlpha:1,duration:.5,ease:"back.out(2)"',1.8),
       ('#bell','rotation:12,duration:.16,repeat:5,yoyo:true,ease:"sine.inOut"','',2.2)
      ],
      [
       ('#globe','scale:.55,rotation:-35,autoAlpha:0','scale:1,rotation:0,autoAlpha:1,duration:1.2,ease:"power3.out"',0),
       ('#nodes','scale:0,autoAlpha:0','scale:1,autoAlpha:1,duration:.55,stagger:.1,ease:"back.out(1.7)"',.55),
       ('#shield','scale:.2,y:115,autoAlpha:0','scale:1,y:0,autoAlpha:1,duration:1,ease:"back.out(1.6)"',1.05),
       ('#final-lock','scale:0,rotation:-30,autoAlpha:0','scale:1,rotation:0,autoAlpha:1,duration:.65,ease:"elastic.out(1,.5)"',1.9),
       ('#url','y:85,autoAlpha:0','y:0,autoAlpha:1,duration:.68,ease:"power3.out"',2.25),
       ('#sparkles','scale:.2,autoAlpha:0','scale:1,autoAlpha:1,duration:.55,ease:"back.out(2)"',2.5),
       ('#globe','rotation:14,duration:'+str(max(1.1,span-2.7))+',ease:"none"','',2)
      ]
    ]
    result=[]
    for selector,frm,to,offset in plans[i]:
        if to:
            result.append(f'tl.fromTo("{s}{selector}",{{{frm}}},{{{to}}},{start+offset:.3f});')
        else:
            result.append(f'tl.to("{s}{selector}",{{{frm}}},{start+offset:.3f});')
    return "".join(result)
