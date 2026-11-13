"""Video vertical: cómo mantener HTTPS con certificados Let's Encrypt gratuitos."""
from __future__ import annotations

def build_design(duration, words, groups, title):
    cuts=[0,.105,.215,.325,.435,.545,.655,.765,.88,1]
    scenes_copy=[
      ("¿TE COBRAN POR EL CANDADO?","TU SSL PUEDE SALIRTE GRATIS","No pagues por el certificado sin conocer esta alternativa"),
      ("CONOCE LET'S ENCRYPT","CERTIFICADOS SIN COSTE","Una autoridad certificadora abierta y sin fines de lucro"),
      ("¿CÓMO LO CONSIGUES?","TU SERVIDOR DEMUESTRA EL DOMINIO","La validación ACME confirma que controlas el sitio"),
      ("VALIDACIÓN AUTOMÁTICA","HTTP-01 O DNS-01","El servidor responde al reto o publica un registro DNS"),
      ("INSTALACIÓN","CERTBOT HACE EL TRABAJO","Solicita el certificado y puede configurarlo en tu servidor"),
      ("TU WEB EN HTTPS","NGINX O APACHE CON SSL/TLS","El certificado se instala y el sitio sirve conexiones seguras"),
      ("OJO CON LA VIGENCIA","NO ES UN CERTIFICADO ETERNO","La validez estándar es de 90 días"),
      ("AUTOMATIZA LA RENOVACIÓN","REVISA QUE TODO SIGA FUNCIONANDO","Programa la renovación y prueba que se complete correctamente"),
      ("EL SIGUIENTE PASO","MÁS CONTROL CON TU PROPIO VPS","Mira el próximo video y aprende dónde instalarlo")
    ]
    scenes=[]
    for i,(label,headline,detail) in enumerate(scenes_copy):
        a,b=duration*cuts[i],duration*cuts[i+1]
        scenes.append({"start":round(a,3),"end":round(b,3),"label":label,
          "headline":headline,"detail":detail,"markup":_visual(i),"animation":_animation(i,a,b)})
    sounds=[
      ("whoosh-medium-soft",.16,-10),
      ("notification-error-soft",duration*.105,-8),
      ("digital-power-up",duration*.22,-10),
      ("keyboard-typing-steady-medium",duration*.33,-13),
      ("keyboard-return-medium",duration*.435,-12),
      ("data-chart-reveal",duration*.55,-11),
      ("mechanical-switch-light",duration*.665,-10),
      ("notification-success-soft",duration*.775,-8),
      ("shimmer-short-soft",duration*.89,-10),
      ("sting-warm-short",duration*.965,-12),
      ("click-tap-medium",duration*.28,-13),
      ("pop-medium-in",duration*.60,-13),
      ("swish-medium",duration*.84,-11)
    ]
    events=[{"id":sid,"moment":round(t,3),"gain_db":gain,"label":sid}
      for sid,t,gain in sounds if 0<=t<duration]
    return {"css":_css(),"scenes":scenes,"sfx_events":events}

def _css():
    return r"""
    #root{background:radial-gradient(ellipse at 50% 20%,rgba(28,103,103,.43),transparent 43%),radial-gradient(ellipse at 88% 80%,rgba(17,64,93,.24),transparent 40%),linear-gradient(150deg,#06111b,#0a1923 55%,#050a12)}
    #root:before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.18;background-image:linear-gradient(rgba(114,231,201,.11) 1px,transparent 1px),linear-gradient(90deg,rgba(114,231,201,.11) 1px,transparent 1px);background-size:74px 74px;mask-image:linear-gradient(to bottom,transparent,#000 15%,#000 85%,transparent)}
    .manual-scene{background:radial-gradient(ellipse at 50% 56%,rgba(21,78,83,.23),transparent 66%)}
    .manual-scene-kicker{color:#7bf0ce;text-shadow:0 0 22px rgba(64,229,190,.42)}
    .manual-scene-headline{color:#f3fbff;text-shadow:0 7px 32px #000;letter-spacing:-2.4px}
    .manual-scene-detail{color:#bad0dc;text-shadow:0 3px 14px #000}
    .manual-scene-index{color:#7cebd0}
    .le-art{position:absolute;left:0;right:0;top:430px;height:980px;display:flex;align-items:center;justify-content:center}
    .le-art svg{width:100%;height:100%;overflow:visible}
    .le-orbit{fill:none;stroke:#39837d;stroke-width:2;stroke-dasharray:9 13}
    .le-wire{fill:none;stroke:#67e6c8;stroke-width:4;stroke-dasharray:12 12}
    .le-node{fill:#0d1e2a;stroke:#6ee6cb;stroke-width:4}
    .le-panel{fill:#0d202e;stroke:#47747a;stroke-width:4}
    .le-card{fill:#102a34;stroke:#63d8be;stroke-width:3}
    .le-green{fill:#74edcf}
    .le-gold{fill:#ffd078}
    .le-red{fill:#ff7182}
    .le-muted{fill:#abc4d0;font:600 23px Arial}
    .le-small{fill:#b9d2dc;font:700 19px Arial}
    .le-bright{fill:#f1fffb;font:800 29px Arial}
    .le-title{fill:#70e8cb;font:900 22px Arial;letter-spacing:3px}
    .le-stroke{fill:none;stroke:#70e8cb;stroke-width:8;stroke-linecap:round;stroke-linejoin:round}
    .le-check{fill:none;stroke:#70e8cb;stroke-width:12;stroke-linecap:round;stroke-linejoin:round}
    .le-lock{fill:#0a1a27;stroke:#6fe8cd;stroke-width:7}
    .le-glow{filter:drop-shadow(0 0 24px #35e4be77)}
    .le-warn{fill:#301d29;stroke:#ff7182;stroke-width:4}
    .le-bar{fill:#1a3d47}
    .le-barfill{fill:#72e8cb}
    """

def _svg(inner,aria):
    return f'<div class="le-art"><svg viewBox="0 0 900 900" role="img" aria-label="{aria}">{inner}</svg></div>'

def _visual(i):
    if i==0:
      return _svg("""
      <g id="money-orbits"><circle cx="450" cy="440" r="340" class="le-orbit"/><circle cx="450" cy="440" r="260" class="le-orbit"/></g>
      <g id="invoice" transform="translate(155 170)"><rect width="590" height="520" rx="30" class="le-panel le-glow"/><rect x="0" y="0" width="590" height="90" rx="28" fill="#173a45"/><text x="42" y="58" class="le-title">HOSTING · FACTURA</text><text x="45" y="155" class="le-muted">Certificado SSL anual</text><text x="535" y="160" text-anchor="end" class="le-bright">€79.00</text><path d="M45 190H545" class="le-orbit"/><text x="45" y="255" class="le-muted">Instalación</text><text x="535" y="260" text-anchor="end" class="le-bright">€20.00</text><path d="M45 290H545" class="le-orbit"/><text x="45" y="355" class="le-green" font-size="25" font-weight="900">TOTAL SSL</text><text x="535" y="360" text-anchor="end" class="le-red" font-size="46" font-weight="900">€99</text><g id="invoice-stamp"><circle cx="295" cy="440" r="65" class="le-warn"/><path d="M255 400L335 480M335 400L255 480" class="le-stroke" style="stroke:#ff7182"/></g></g>
      <g id="free-coin"><circle cx="735" cy="715" r="72" fill="#16483f" stroke="#72e8cb" stroke-width="5"/><text x="735" y="730" text-anchor="middle" class="le-green" font-size="49" font-weight="900">0€</text></g>
      ""","Factura de hosting mostrando coste de certificado SSL y alternativa sin coste")
    if i==1:
      return _svg("""
      <g id="le-globe"><circle cx="450" cy="420" r="300" class="le-orbit"/><circle cx="450" cy="420" r="230" class="le-orbit"/><path d="M150 420H750M450 120V720" class="le-wire" opacity=".45"/></g>
      <g id="le-logo" transform="translate(450 400)"><circle r="160" fill="#103b3b" stroke="#74edcf" stroke-width="7" class="le-glow"/><path d="M-80 -10Q-70 -110 0 -110Q75 -110 82 -10Q85 68 0 116Q-85 68 -80 -10Z" fill="#1b6251" stroke="#83efd4" stroke-width="6"/><path d="M-39 -4L-7 28L49 -43" class="le-check"/><text x="0" y="205" text-anchor="middle" class="le-bright">LET'S ENCRYPT</text></g>
      <g id="le-badges"><rect x="100" y="690" width="190" height="60" rx="18" class="le-card"/><text x="195" y="729" text-anchor="middle" class="le-small">GRATUITO</text><rect x="610" y="690" width="190" height="60" rx="18" class="le-card"/><text x="705" y="729" text-anchor="middle" class="le-small">AUTOMÁTICO</text></g>
      ""","Emblema conceptual de Let's Encrypt con etiquetas gratuito y automático")
    if i==2:
      return _svg("""
      <g id="domain-screen" transform="translate(100 210)"><rect width="700" height="440" rx="28" class="le-panel le-glow"/><path d="M0 75H700" stroke="#426574" stroke-width="4"/><circle cx="40" cy="38" r="10" fill="#ff7182"/><circle cx="75" cy="38" r="10" fill="#ffd078"/><circle cx="110" cy="38" r="10" fill="#72e8cb"/><rect x="160" y="18" width="490" height="42" rx="12" fill="#06111a"/><text x="185" y="47" class="le-small">https://tu-dominio.com</text><text x="45" y="145" class="le-title">PRUEBA DE CONTROL DEL DOMINIO</text><rect x="45" y="180" width="610" height="80" rx="16" class="le-card"/><text x="78" y="230" class="le-bright">/.well-known/acme-challenge/...</text><rect x="45" y="290" width="610" height="80" rx="16" class="le-card"/><text x="78" y="340" class="le-small">RESPUESTA CORRECTA DEL SERVIDOR</text><g id="domain-check"><circle cx="600" cy="400" r="48" fill="#15483e" stroke="#72e8cb" stroke-width="4"/><path d="M575 400L592 418L626 379" class="le-check"/></g></g>
      <g id="domain-dns"><circle cx="170" cy="735" r="40" class="le-node"/><circle cx="450" cy="735" r="40" class="le-node"/><circle cx="730" cy="735" r="40" class="le-node"/><path d="M210 735H410M490 735H690" class="le-wire"/><text x="450" y="810" text-anchor="middle" class="le-small">DOMINIO · DNS · SERVIDOR</text></g>
      ""","Servidor demostrando que controla el dominio mediante una validación ACME")
    if i==3:
      return _svg("""
      <g id="http-validation" transform="translate(80 245)"><rect width="340" height="375" rx="26" class="le-panel"/><text x="170" y="65" text-anchor="middle" class="le-green" font-size="31" font-weight="900">HTTP-01</text><rect x="38" y="115" width="264" height="170" rx="16" class="le-card"/><text x="170" y="160" text-anchor="middle" class="le-small">ARCHIVO DE</text><text x="170" y="194" text-anchor="middle" class="le-bright">VALIDACIÓN</text><path d="M85 232H255" class="le-wire"/><path d="M170 285V325" class="le-stroke"/><text x="170" y="355" text-anchor="middle" class="le-small">PUERTO 80</text></g>
      <g id="dns-validation" transform="translate(480 245)"><rect width="340" height="375" rx="26" class="le-panel"/><text x="170" y="65" text-anchor="middle" class="le-green" font-size="31" font-weight="900">DNS-01</text><g id="dns-record"><rect x="38" y="115" width="264" height="170" rx="16" class="le-card"/><text x="170" y="160" text-anchor="middle" class="le-small">REGISTRO TXT</text><text x="170" y="205" text-anchor="middle" class="le-bright">_acme-challenge</text><path d="M85 242H255" class="le-wire"/></g><path d="M170 285V325" class="le-stroke"/><text x="170" y="355" text-anchor="middle" class="le-small">ZONA DNS</text></g>
      <g id="validation-arrow"><path d="M420 425H480M455 400L480 425L455 450" class="le-stroke"/></g>
      ""","Comparativa visual de validación ACME HTTP-01 y DNS-01")
    if i==4:
      return _svg("""
      <g id="terminal" transform="translate(90 205)"><rect width="720" height="500" rx="28" fill="#07141d" stroke="#5b958e" stroke-width="4" class="le-glow"/><path d="M0 75H720" stroke="#426574" stroke-width="4"/><circle cx="40" cy="38" r="10" fill="#ff7182"/><circle cx="75" cy="38" r="10" fill="#ffd078"/><circle cx="110" cy="38" r="10" fill="#72e8cb"/><text x="45" y="135" class="le-green" font-size="25" font-weight="900">root@vps:~# certbot --nginx</text><g id="terminal-lines"><text x="45" y="200" class="le-small">Solicitando certificado...</text><text x="45" y="255" class="le-small">Validando dominio...</text><text x="45" y="310" class="le-small">Instalando en Nginx...</text><text x="45" y="380" class="le-green" font-size="25" font-weight="900">✓ HTTPS CONFIGURADO</text></g><rect id="terminal-cursor" x="45" y="420" width="18" height="32" fill="#72e8cb"/></g>
      <g id="certbot-badge"><circle cx="720" cy="740" r="70" fill="#123f3b" stroke="#72e8cb" stroke-width="5"/><path d="M720 690V790M670 740H770" class="le-stroke"/><text x="720" y="840" text-anchor="middle" class="le-small">CERTBOT</text></g>
      ""","Terminal mostrando Certbot instalando un certificado SSL")
    if i==5:
      return _svg("""
      <g id="web-server" transform="translate(120 195)"><rect width="660" height="490" rx="30" class="le-panel le-glow"/><text x="45" y="65" class="le-title">SERVIDOR WEB</text><g id="nginx"><rect x="45" y="100" width="260" height="275" rx="18" class="le-card"/><text x="175" y="155" text-anchor="middle" class="le-bright">NGINX</text><rect x="95" y="195" width="160" height="36" rx="9" fill="#185446"/><rect x="95" y="250" width="160" height="36" rx="9" fill="#185446"/><path d="M115 320H235" class="le-wire"/></g><g id="apache"><rect x="355" y="100" width="260" height="275" rx="18" class="le-card"/><text x="485" y="155" text-anchor="middle" class="le-bright">APACHE</text><circle cx="485" cy="250" r="55" class="le-node"/><path d="M455 250L477 272L520 223" class="le-check"/></g><rect x="45" y="405" width="570" height="55" rx="14" fill="#174b42"/><text x="330" y="442" text-anchor="middle" class="le-bright">CERTIFICADO INSTALADO</text></g>
      <g id="https-browser"><rect x="260" y="755" width="380" height="65" rx="18" class="le-card"/><circle cx="300" cy="788" r="11" fill="#72e8cb"/><text x="330" y="798" class="le-small">https://tu-web.com</text><path d="M450 685V755" class="le-wire"/></g>
      ""","Certificado instalado en Nginx o Apache y sitio web sirviendo HTTPS")
    if i==6:
      return _svg("""
      <g id="expiry-clock" transform="translate(450 405)"><circle r="245" class="le-orbit"/><circle r="185" fill="#102a34" stroke="#75e9cf" stroke-width="8"/><path d="M0 -112V0L90 58" class="le-stroke"/><circle r="15" fill="#75e9cf"/></g>
      <g id="expiry-calendar" transform="translate(250 620)"><rect width="400" height="190" rx="24" class="le-panel"/><path d="M0 65H400" stroke="#4c777c" stroke-width="4"/><text x="200" y="45" text-anchor="middle" class="le-title">VIGENCIA ESTÁNDAR</text><text x="200" y="145" text-anchor="middle" class="le-gold" font-size="65" font-weight="900">90 DÍAS</text></g>
      <g id="expiry-alert"><circle cx="735" cy="235" r="54" class="le-warn"/><path d="M735 202V245M735 267V270" stroke="#ff7182" stroke-width="11" stroke-linecap="round"/></g>
      ""","Reloj y calendario mostrando la validez estándar de 90 días")
    if i==7:
      return _svg("""
      <g id="renew-panel" transform="translate(105 210)"><rect width="690" height="450" rx="30" class="le-panel le-glow"/><text x="45" y="68" class="le-title">RENOVACIÓN AUTOMÁTICA</text><rect x="45" y="105" width="600" height="100" rx="18" class="le-card"/><circle cx="100" cy="155" r="28" fill="#16483e" stroke="#72e8cb" stroke-width="4"/><path d="M85 155L98 169L119 140" class="le-check"/><text x="155" y="150" class="le-bright">Certificado renovado</text><text x="155" y="180" class="le-small">Tarea programada activa</text><text x="45" y="275" class="le-muted">Próxima comprobación</text><rect x="45" y="300" width="600" height="25" rx="12" class="le-bar"/><rect id="renew-progress" x="45" y="300" width="440" height="25" rx="12" class="le-barfill"/><text x="45" y="390" class="le-small">Prueba de renovación · alertas · monitorización</text></g>
      <g id="renew-cycle"><path d="M450 735A90 90 0 1 1 535 675" class="le-stroke"/><path d="M535 640L542 685L500 674" class="le-stroke"/><circle cx="450" cy="735" r="30" class="le-node"/></g>
      ""","Panel que muestra renovación automática y monitorización del certificado")
    return _svg("""
    <g id="vps-grid"><circle cx="450" cy="415" r="340" class="le-orbit"/><path d="M110 415H790M450 75V755M210 175L690 655M690 175L210 655" class="le-wire" opacity=".55"/></g>
    <g id="vps-rack" transform="translate(285 170)"><rect width="330" height="500" rx="28" class="le-panel le-glow"/><g id="rack-units"><rect x="35" y="45" width="260" height="95" rx="15" class="le-card"/><rect x="35" y="165" width="260" height="95" rx="15" class="le-card"/><rect x="35" y="285" width="260" height="95" rx="15" class="le-card"/><circle cx="80" cy="92" r="12" fill="#72e8cb"/><circle cx="80" cy="212" r="12" fill="#72e8cb"/><circle cx="80" cy="332" r="12" fill="#72e8cb"/><path d="M115 92H260M115 212H260M115 332H260" class="le-wire"/></g><text x="165" y="445" text-anchor="middle" class="le-bright">TU PROPIO VPS</text></g>
    <g id="vps-shield" transform="translate(350 555)"><path d="M100 0L195 35V125Q195 220 100 275Q5 220 5 125V35Z" fill="#123d39" stroke="#72e8cb" stroke-width="7"/><path d="M52 135L87 170L150 95" class="le-check"/></g>
    <g id="vps-cta"><rect x="185" y="835" width="530" height="62" rx="31" class="le-card"/><text x="450" y="875" text-anchor="middle" class="le-bright">PRÓXIMO VIDEO: VPS</text></g>
    ""","Servidor VPS con escudo de seguridad y llamada al próximo video")

def _animation(i,start,end):
    s=f"#manual-scene-{i} "
    span=max(.6,end-start)
    plans=[
      [("#money-orbits","scale:.65,rotation:-25,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:1.0,ease:'power3.out'",0),
       ("#invoice","y:160,rotationY:18,scale:.85,autoAlpha:0","y:0,rotationY:0,scale:1,autoAlpha:1,duration:.9,ease:'back.out(1.4)'",.2),
       ("#invoice-stamp","scale:0,rotation:-90","scale:1,rotation:0,duration:.65,ease:'elastic.out(1,.5)'",1.0),
       ("#free-coin","scale:0,y:80,autoAlpha:0","scale:1,y:0,autoAlpha:1,duration:.7,ease:'back.out(2)'",1.7)],
      [("#le-globe","scale:.55,rotation:-25,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:1.0,ease:'power3.out'",0),
       ("#le-logo","scale:.2,rotation:-35,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:1.0,ease:'elastic.out(1,.5)'",.3),
       ("#le-badges","y:60,autoAlpha:0","y:0,autoAlpha:1,duration:.55,stagger:.15,ease:'back.out(2)'",1.5),
       ("#le-globe","rotation:12,duration:"+str(max(1,span-2))+",ease:'none'","",1.0)],
      [("#domain-screen","y:130,scale:.9,autoAlpha:0","y:0,scale:1,autoAlpha:1,duration:.85,ease:'power3.out'",0),
       ("#domain-check","scale:0,rotation:-60","scale:1,rotation:0,duration:.65,ease:'elastic.out(1,.5)'",1.25),
       ("#domain-dns","y:55,autoAlpha:0","y:0,autoAlpha:1,duration:.6,stagger:.1,ease:'power2.out'",1.6),
       ("#domain-dns circle","scale:.5","scale:1,duration:.45,repeat:1,yoyo:true,stagger:.12,ease:'sine.inOut'",2.0)],
      [("#http-validation","x:-180,rotation:-6,autoAlpha:0","x:0,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'",0),
       ("#dns-validation","x:180,rotation:6,autoAlpha:0","x:0,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'",.15),
       ("#validation-arrow","scale:0,transformOrigin:'50% 50%'","scale:1,duration:.55,ease:'back.out(2)'",1.1),
       ("#dns-record","y:35,autoAlpha:0","y:0,autoAlpha:1,duration:.5,ease:'power2.out'",1.45)],
      [("#terminal","y:150,scale:.88,autoAlpha:0","y:0,scale:1,autoAlpha:1,duration:.9,ease:'power3.out'",0),
       ("#terminal-lines text","x:-40,autoAlpha:0","x:0,autoAlpha:1,duration:.4,stagger:.35,ease:'power2.out'",.7),
       ("#terminal-cursor","opacity:0","opacity:1,duration:.35,repeat:5,yoyo:true,ease:'none'",1.3),
       ("#certbot-badge","scale:0,rotation:-30,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:.7,ease:'elastic.out(1,.5)'",1.8)],
      [("#web-server","scale:.8,y:120,autoAlpha:0","scale:1,y:0,autoAlpha:1,duration:.9,ease:'power3.out'",0),
       ("#nginx","x:-50,autoAlpha:0","x:0,autoAlpha:1,duration:.65,ease:'back.out(1.5)'",.65),
       ("#apache","x:50,autoAlpha:0","x:0,autoAlpha:1,duration:.65,ease:'back.out(1.5)'",.85),
       ("#https-browser","y:80,autoAlpha:0","y:0,autoAlpha:1,duration:.6,ease:'back.out(1.7)'",1.7)],
      [("#expiry-clock","scale:.55,rotation:-80,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:1.0,ease:'power3.out'",0),
       ("#expiry-calendar","y:100,autoAlpha:0","y:0,autoAlpha:1,duration:.7,ease:'back.out(1.6)'",1.1),
       ("#expiry-alert","scale:0,autoAlpha:0","scale:1,autoAlpha:1,duration:.6,ease:'elastic.out(1,.5)'",1.7),
       ("#expiry-clock","rotation:10,duration:.18,repeat:5,yoyo:true,ease:'sine.inOut'","",2.1)],
      [("#renew-panel","x:150,autoAlpha:0","x:0,autoAlpha:1,duration:.85,ease:'power3.out'",0),
       ("#renew-progress","scaleX:.05,transformOrigin:'left center'","scaleX:1,duration:1.1,ease:'power2.out'",.9),
       ("#renew-cycle","scale:0,rotation:-90,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:.8,ease:'elastic.out(1,.5)'",1.45),
       ("#renew-cycle","rotation:360,duration:"+str(max(1,span-2.2))+",ease:'none'","",2.0)],
      [("#vps-grid","scale:.65,rotation:-20,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:1.0,ease:'power3.out'",0),
       ("#vps-rack","y:180,scale:.8,autoAlpha:0","y:0,scale:1,autoAlpha:1,duration:.9,ease:'back.out(1.5)'",.2),
       ("#rack-units rect","x:-35,autoAlpha:0","x:0,autoAlpha:1,duration:.45,stagger:.14,ease:'power2.out'",.9),
       ("#vps-shield","scale:.2,y:85,autoAlpha:0","scale:1,y:0,autoAlpha:1,duration:.8,ease:'elastic.out(1,.5)'",1.55),
       ("#vps-cta","y:70,autoAlpha:0","y:0,autoAlpha:1,duration:.65,ease:'back.out(1.7)'",2.15)]
    ]
    out=[]
    for selector,frm,to,offset in plans[i]:
      if to:
        out.append(f'tl.fromTo("{s}{selector}",{{{frm}}},{{{to}}},{start+offset:.3f});')
      else:
        out.append(f'tl.to("{s}{selector}",{{{frm}}},{start+offset:.3f});')
    return "".join(out)
