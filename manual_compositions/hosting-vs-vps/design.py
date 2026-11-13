"""Composición manual: hosting compartido frente a VPS."""
from __future__ import annotations

def build_design(duration, words, groups, title):
    cuts = [0, .145, .30, .425, .575, .735, .865, 1]
    copy = [
        ("UNA PREGUNTA", "¿CIENTOS DE WEBS EN UN SERVIDOR?", "Tu página podría compartir recursos con muchos otros sitios"),
        ("HOSTING COMPARTIDO", "VARIOS SITIOS, UN MISMO SERVIDOR", "Todos utilizan parte de los recursos de una misma máquina"),
        ("PARA EMPEZAR", "PUEDE SER MÁS QUE SUFICIENTE", "Si tu proyecto es pequeño, no necesitas complicarte"),
        ("CUANDO CRECES", "MÁS VISITAS, MÁS NECESIDADES", "Quizá quieras instalar aplicaciones y controlar la configuración"),
        ("AQUÍ APARECE EL VPS", "TU PROPIO ENTORNO VIRTUAL", "Recursos asignados y más libertad para configurar el servidor"),
        ("PERO RECUERDA", "UN VPS NO HACE MAGIA", "El rendimiento también depende de cómo esté configurado"),
        ("VAMOS A CONVERSAR", "¿HOSTING O VPS?", "Cuéntame qué utilizas. Próximo tema: qué pasa al abrir una web"),
    ]
    scenes=[]
    for i,(label,headline,detail) in enumerate(copy):
        a,b=duration*cuts[i],duration*cuts[i+1]
        scenes.append({"start":round(a,3),"end":round(b,3),"label":label,
                       "headline":headline,"detail":detail,
                       "markup":_visual(i),"animation":_animation(i,a,b)})
    cues=[
        ("impact-light-soft",.035,-10),("whoosh-medium-soft",.15,-11),
        ("pop-medium-in",.30,-12),("data-chart-reveal",.425,-10),
        ("digital-power-up",.575,-10),("mechanical-switch-light",.735,-11),
        ("shimmer-short-soft",.865,-12),("sting-warm-short",.965,-13)
    ]
    events=[{"id":sid,"moment":round(duration*f,3),"gain_db":gain,"label":sid}
            for sid,f,gain in cues if duration*f < duration]
    return {"css":_css(),"scenes":scenes,"sfx_events":events}

def _css():
    return r"""
    #root{
      background:
        radial-gradient(ellipse at 15% 18%,rgba(255,126,62,.24),transparent 36%),
        radial-gradient(ellipse at 84% 78%,rgba(92,214,190,.19),transparent 38%),
        linear-gradient(145deg,#10151c,#17212b 52%,#0b1118);
    }
    #root:before{content:"";position:absolute;inset:0;opacity:.12;pointer-events:none;
      background-image:linear-gradient(rgba(255,255,255,.08) 1px,transparent 1px),
      linear-gradient(90deg,rgba(255,255,255,.08) 1px,transparent 1px);
      background-size:54px 54px;mask-image:linear-gradient(to bottom,transparent,#000 15%,#000 85%,transparent)}
    .manual-scene{background:radial-gradient(ellipse at 50% 60%,rgba(255,255,255,.035),transparent 65%)}
    .manual-scene-kicker{color:#ffad78;text-shadow:0 0 24px #ff8b4b55}
    .manual-scene-headline{color:#f7fbff;text-shadow:0 8px 35px #05090e;letter-spacing:-2.8px}
    .manual-scene-detail{color:#c4d1d8;text-shadow:0 3px 15px #080d12}
    .manual-scene-index{color:#75dfc2}
    .manual-scene-index:after{content:"  ·  CLOUDSERVICEGM";font-size:13px;letter-spacing:2px;color:#b9c8cf;opacity:.72}
    .v-art{position:absolute;left:0;right:0;top:430px;height:980px;display:flex;align-items:center;justify-content:center}
    .v-art svg{width:100%;height:100%;overflow:visible}
    .v-orbit{fill:none;stroke:#637987;stroke-width:2;stroke-dasharray:8 13;opacity:.65}
    .v-panel{fill:#202e38;stroke:#77909d;stroke-width:4}
    .v-card{fill:#2a3b46;stroke:#8ba4af;stroke-width:3}
    .v-orange{fill:#ff9864}.v-mint{fill:#73dfc2}.v-yellow{fill:#ffd27f}
    .v-white{fill:#f5fbfc}.v-muted{fill:#c2d1d7;font:600 25px Arial}
    .v-small{fill:#d5e1e5;font:700 22px Arial}
    .v-bold{fill:#f7fbff;font:900 34px Arial}
    .v-kicker{fill:#ffb17f;font:900 22px Arial;letter-spacing:3px}
    .v-line{fill:none;stroke:#a3bac4;stroke-width:5;stroke-linecap:round;stroke-linejoin:round}
    .v-dash{fill:none;stroke:#8fa8b4;stroke-width:4;stroke-dasharray:10 12}
    .v-check{fill:none;stroke:#73dfc2;stroke-width:12;stroke-linecap:round;stroke-linejoin:round}
    .v-glow{filter:drop-shadow(0 0 26px #70d8bf33)}
    .v-warm-glow{filter:drop-shadow(0 0 28px #ff986444)}
    """
def _svg(body,label):
    return f'<div class="v-art"><svg viewBox="0 0 900 900" role="img" aria-label="{label}">{body}</svg></div>'

def _visual(i):
    if i==0:
        return _svg("""
        <g id="crowd-orbit"><circle cx="450" cy="445" r="350" class="v-orbit"/><circle cx="450" cy="445" r="280" class="v-orbit"/></g>
        <g id="crowd-rack" transform="translate(330 150)">
          <rect width="240" height="590" rx="28" class="v-panel v-glow"/>
          <g fill="#2d424e" stroke="#91aab5" stroke-width="3">
            <rect x="28" y="45" width="184" height="95" rx="15"/><rect x="28" y="165" width="184" height="95" rx="15"/>
            <rect x="28" y="285" width="184" height="95" rx="15"/><rect x="28" y="405" width="184" height="95" rx="15"/>
          </g>
          <g fill="#73dfc2"><circle cx="58" cy="92" r="10"/><circle cx="58" cy="212" r="10"/><circle cx="58" cy="332" r="10"/><circle cx="58" cy="452" r="10"/></g>
          <g stroke="#a3bac4" stroke-width="7" stroke-linecap="round"><path d="M88 92H185M88 212H185M88 332H185M88 452H185"/></g>
          <text x="120" y="555" text-anchor="middle" class="v-kicker">UN SERVIDOR</text>
        </g>
        <g id="crowd-sites" fill="#ff9864" stroke="#ffd0b5" stroke-width="3">
          <rect x="85" y="245" width="150" height="115" rx="18"/><rect x="665" y="245" width="150" height="115" rx="18"/>
          <rect x="85" y="525" width="150" height="115" rx="18"/><rect x="665" y="525" width="150" height="115" rx="18"/>
        </g>
        <g fill="#17212b"><path d="M110 280H210V340H110Z M690 280H790V340H690Z M110 560H210V620H110Z M690 560H790V620H690Z"/></g>
        <g id="crowd-links" class="v-dash"><path d="M235 300L330 250M570 250L665 300M235 580L330 640M570 640L665 580"/></g>
        <g fill="#f5fbfc" font-family="Arial" font-weight="900" font-size="24" text-anchor="middle"><text x="160" y="415">WEB A</text><text x="740" y="415">WEB B</text><text x="160" y="695">WEB C</text><text x="740" y="695">WEB D</text></g>
        ""","Varias páginas web conectadas a un mismo servidor compartido")

    if i==1:
        return _svg("""
        <g id="shared-frame"><circle cx="450" cy="440" r="340" class="v-orbit"/></g>
        <g id="shared-host" transform="translate(155 190)">
          <rect width="590" height="500" rx="34" class="v-panel v-glow"/>
          <text x="295" y="65" text-anchor="middle" class="v-kicker">MISMA MÁQUINA</text>
          <g id="shared-sites">
            <rect x="42" y="105" width="235" height="135" rx="20" fill="#ff9864" stroke="#ffd0b5" stroke-width="3"/>
            <rect x="313" y="105" width="235" height="135" rx="20" fill="#73dfc2" stroke="#c5fff0" stroke-width="3"/>
            <rect x="42" y="270" width="235" height="135" rx="20" fill="#ffd27f" stroke="#fff0c8" stroke-width="3"/>
            <rect x="313" y="270" width="235" height="135" rx="20" fill="#8fb7ff" stroke="#d7e5ff" stroke-width="3"/>
          </g>
          <g fill="#17212b" font-family="Arial" font-size="28" font-weight="900" text-anchor="middle">
            <text x="159" y="183">WEB 01</text><text x="430" y="183">WEB 02</text><text x="159" y="348">WEB 03</text><text x="430" y="348">WEB 04</text>
          </g>
          <path d="M295 85V430" stroke="#8299a4" stroke-width="3" stroke-dasharray="8 10"/>
          <text x="295" y="465" text-anchor="middle" class="v-small">RECURSOS COMPARTIDOS</text>
        </g>
        ""","Cuatro páginas web comparten los recursos de un mismo servidor")

    if i==2:
        return _svg("""
        <g id="small-orbit"><circle cx="450" cy="440" r="320" class="v-orbit"/></g>
        <g id="small-window" transform="translate(190 190)">
          <rect width="520" height="480" rx="28" class="v-panel v-warm-glow"/>
          <path d="M0 75H520" stroke="#77909d" stroke-width="4"/>
          <circle cx="42" cy="38" r="10" fill="#ff9864"/><circle cx="76" cy="38" r="10" fill="#ffd27f"/><circle cx="110" cy="38" r="10" fill="#73dfc2"/>
          <rect x="55" y="120" width="410" height="190" rx="18" fill="#304652"/>
          <rect x="85" y="150" width="150" height="130" rx="12" fill="#ff9864"/>
          <rect x="260" y="150" width="175" height="22" rx="9" fill="#d6e1e5"/><rect x="260" y="190" width="145" height="15" rx="7" fill="#8ca4af"/><rect x="260" y="222" width="165" height="15" rx="7" fill="#8ca4af"/>
          <rect x="55" y="345" width="410" height="72" rx="18" fill="#17483f" stroke="#73dfc2" stroke-width="3"/>
          <path d="M88 382L112 400L150 360" class="v-check"/>
          <text x="285" y="392" text-anchor="middle" class="v-bold">TODO BIEN</text>
        </g>
        <g id="small-stars" fill="#ffd27f"><path d="M140 170L155 205L193 210L164 235L172 273L140 253L108 273L116 235L87 210L125 205Z"/><path d="M745 570L758 600L790 604L766 625L773 658L745 641L717 658L724 625L700 604L732 600Z"/></g>
        ""","Página web pequeña funcionando correctamente en un hosting compartido")

    if i==3:
        return _svg("""
        <g id="growth-chart" transform="translate(130 185)">
          <rect width="640" height="500" rx="30" class="v-panel v-glow"/>
          <text x="320" y="65" text-anchor="middle" class="v-kicker">EL PROYECTO CRECE</text>
          <path d="M85 390V125M85 390H565" class="v-line"/>
          <g id="growth-bars" fill="#ff9864">
            <rect x="135" y="305" width="72" height="85" rx="10"/><rect x="245" y="260" width="72" height="130" rx="10"/>
            <rect x="355" y="190" width="72" height="200" rx="10"/><rect x="465" y="110" width="72" height="280" rx="10"/>
          </g>
          <path d="M165 280L280 230L390 160L500 85" fill="none" stroke="#73dfc2" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>
          <g fill="#73dfc2"><circle cx="165" cy="280" r="12"/><circle cx="280" cy="230" r="12"/><circle cx="390" cy="160" r="12"/><circle cx="500" cy="85" r="12"/></g>
          <text x="320" y="455" text-anchor="middle" class="v-small">MÁS VISITAS · MÁS DEMANDAS</text>
        </g>
        <g id="growth-tags">
          <rect x="45" y="735" width="245" height="78" rx="22" fill="#ff9864"/><rect x="330" y="735" width="245" height="78" rx="22" fill="#73dfc2"/><rect x="615" y="735" width="245" height="78" rx="22" fill="#8fb7ff"/>
          <g fill="#17212b" font-family="Arial" font-size="23" font-weight="900" text-anchor="middle"><text x="167" y="783">VISITAS</text><text x="452" y="783">APLICACIONES</text><text x="737" y="783">CONTROL</text></g>
        </g>
        ""","Gráfico ascendente de visitas y necesidades de un proyecto web")

    if i==4:
        return _svg("""
        <g id="vps-orbits"><circle cx="450" cy="435" r="355" class="v-orbit"/><circle cx="450" cy="435" r="285" class="v-orbit"/></g>
        <g id="vps-physical" transform="translate(120 210)">
          <rect width="660" height="470" rx="32" class="v-panel"/>
          <text x="330" y="62" text-anchor="middle" class="v-kicker">SERVIDOR FÍSICO</text>
          <rect x="55" y="100" width="550" height="300" rx="22" fill="#16232c" stroke="#78929e" stroke-width="3"/>
          <g id="vps-virtuals">
            <rect x="80" y="125" width="240" height="110" rx="17" fill="#ff9864" stroke="#ffd0b5" stroke-width="3"/>
            <rect x="345" y="125" width="240" height="110" rx="17" fill="#73dfc2" stroke="#c5fff0" stroke-width="3"/>
            <rect x="80" y="260" width="240" height="110" rx="17" fill="#8fb7ff" stroke="#d7e5ff" stroke-width="3"/>
            <rect x="345" y="260" width="240" height="110" rx="17" fill="#ffd27f" stroke="#fff0c8" stroke-width="3"/>
          </g>
          <g fill="#17212b" font-family="Arial" font-size="30" font-weight="900" text-anchor="middle"><text x="200" y="192">VPS 1</text><text x="465" y="192">VPS 2</text><text x="200" y="327">VPS 3</text><text x="465" y="327">VPS 4</text></g>
        </g>
        <g id="vps-badges">
          <rect x="185" y="735" width="240" height="85" rx="23" fill="#17483f" stroke="#73dfc2" stroke-width="3"/>
          <rect x="475" y="735" width="240" height="85" rx="23" fill="#253c57" stroke="#8fb7ff" stroke-width="3"/>
          <text x="305" y="790" text-anchor="middle" class="v-bold">RECURSOS</text><text x="595" y="790" text-anchor="middle" class="v-bold">CONTROL</text>
        </g>
        ""","Un servidor físico dividido en varios entornos de servidores virtuales")

    if i==5:
        return _svg("""
        <g id="magic-cloud"><circle cx="450" cy="420" r="320" class="v-orbit"/></g>
        <g id="magic-gauge" transform="translate(450 390)">
          <circle r="230" fill="#202e38" stroke="#ff9864" stroke-width="7" class="v-warm-glow"/>
          <path d="M-145 95A175 175 0 0 1 145 95" fill="none" stroke="#607985" stroke-width="24" stroke-linecap="round"/>
          <path d="M-145 95A175 175 0 0 1 0 -80" fill="none" stroke="#73dfc2" stroke-width="24" stroke-linecap="round"/>
          <path d="M0 20L110 -100" class="v-line"/><circle r="20" fill="#ffd27f"/>
          <text x="0" y="155" text-anchor="middle" class="v-bold">RENDIMIENTO</text>
        </g>
        <g id="magic-tools" transform="translate(190 700)">
          <rect width="520" height="130" rx="28" class="v-panel"/>
          <g fill="#ff9864"><circle cx="95" cy="65" r="28"/><circle cx="260" cy="65" r="28"/><circle cx="425" cy="65" r="28"/></g>
          <g fill="#17212b" font-family="Arial" font-size="19" font-weight="900" text-anchor="middle"><text x="95" y="72">CPU</text><text x="260" y="72">RAM</text><text x="425" y="72">WEB</text></g>
          <text x="260" y="115" text-anchor="middle" class="v-small">RECURSOS + CONFIGURACIÓN</text>
        </g>
        <g id="magic-cross"><path d="M710 170L785 245M785 170L710 245" stroke="#ff9864" stroke-width="15" stroke-linecap="round"/></g>
        ""","Medidor de rendimiento y recursos para mostrar que un VPS no garantiza velocidad por sí solo")

    return _svg("""
    <g id="community-orbit"><circle cx="450" cy="440" r="340" class="v-orbit"/></g>
    <g id="community-phone" transform="translate(285 125)">
      <rect width="330" height="610" rx="42" fill="#17232c" stroke="#9bb0b9" stroke-width="7" class="v-glow"/>
      <rect x="20" y="65" width="290" height="480" rx="24" fill="#243640"/>
      <rect x="50" y="105" width="230" height="100" rx="18" fill="#ff9864"/>
      <text x="165" y="165" text-anchor="middle" fill="#17212b" font-size="30" font-weight="900">HOSTING</text>
      <rect x="50" y="235" width="230" height="100" rx="18" fill="#73dfc2"/>
      <text x="165" y="295" text-anchor="middle" fill="#17212b" font-size="34" font-weight="900">VPS</text>
      <g fill="#d5e1e5"><circle cx="100" cy="395" r="9"/><circle cx="165" cy="395" r="9"/><circle cx="230" cy="395" r="9"/></g>
      <rect x="118" y="565" width="94" height="9" rx="5" fill="#8299a4"/>
    </g>
    <g id="community-bubbles">
      <path d="M95 300H245Q270 300 270 325V425Q270 450 245 450H165L115 490V450H95Q70 450 70 425V325Q70 300 95 300Z" fill="#ff9864" stroke="#ffd0b5" stroke-width="3"/>
      <path d="M655 515H805Q830 515 830 540V640Q830 665 805 665H785V705L735 665H655Q630 665 630 640V540Q630 515 655 515Z" fill="#73dfc2" stroke="#c5fff0" stroke-width="3"/>
      <g fill="#17212b" font-size="23" font-weight="900" text-anchor="middle"><text x="170" y="365">¿QUÉ</text><text x="170" y="400">USAS?</text><text x="730" y="580">CUÉNTAME</text><text x="730" y="615">ABAJO</text></g>
    </g>
    <g id="community-next"><rect x="165" y="775" width="570" height="78" rx="25" fill="#253c57" stroke="#8fb7ff" stroke-width="3"/><text x="450" y="825" text-anchor="middle" class="v-bold">PRÓXIMO: ¿CÓMO VIAJA UNA WEB?</text></g>
    ""","Teléfono con opciones de hosting y VPS y burbujas para invitar a comentar")

def _animation(i,start,end):
    s=f"#manual-scene-{i} "
    plans=[
      [("#crowd-orbit","scale:.6,rotation:-20,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'",0),
       ("#crowd-rack","y:160,scale:.8,autoAlpha:0","y:0,scale:1,autoAlpha:1,duration:.8,ease:'back.out(1.5)'",.18),
       ("#crowd-sites rect","scale:0,autoAlpha:0","scale:1,autoAlpha:1,duration:.5,stagger:.12,ease:'back.out(1.8)'",.65),
       ("#crowd-links","scaleX:0,transformOrigin:'center'","scaleX:1,duration:.65,ease:'power2.out'",1.25)],
      [("#shared-frame","scale:.65,autoAlpha:0","scale:1,autoAlpha:1,duration:.8,ease:'power3.out'",0),
       ("#shared-host","y:140,rotationX:12,autoAlpha:0","y:0,rotationX:0,autoAlpha:1,duration:.8,ease:'power3.out'",.15),
       ("#shared-sites rect","scale:.4,autoAlpha:0","scale:1,autoAlpha:1,duration:.48,stagger:.16,ease:'back.out(1.7)'",.7)],
      [("#small-orbit","scale:.6,rotation:-25,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'",0),
       ("#small-window","y:150,scale:.82,autoAlpha:0","y:0,scale:1,autoAlpha:1,duration:.85,ease:'back.out(1.5)'",.2),
       ("#small-stars","scale:0,rotation:-35,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:.6,stagger:.2,ease:'elastic.out(1,.5)'",1.15)],
      [("#growth-chart","y:120,scale:.85,autoAlpha:0","y:0,scale:1,autoAlpha:1,duration:.8,ease:'power3.out'",0),
       ("#growth-bars rect","scaleY:.08,transformOrigin:'center bottom'","scaleY:1,duration:.65,stagger:.16,ease:'power2.out'",.65),
       ("#growth-chart path","drawSVG:'0%'","drawSVG:'100%',duration:.9,ease:'power2.out'",1.1),
       ("#growth-tags rect","y:70,autoAlpha:0","y:0,autoAlpha:1,duration:.55,stagger:.13,ease:'back.out(1.6)'",1.4)],
      [("#vps-orbits","scale:.6,rotation:20,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'",0),
       ("#vps-physical","scale:.82,y:150,autoAlpha:0","scale:1,y:0,autoAlpha:1,duration:.8,ease:'back.out(1.4)'",.2),
       ("#vps-virtuals rect","scale:.55,autoAlpha:0","scale:1,autoAlpha:1,duration:.5,stagger:.13,ease:'back.out(1.8)'",.85),
       ("#vps-badges","y:80,autoAlpha:0","y:0,autoAlpha:1,duration:.65,ease:'power3.out'",1.5)],
      [("#magic-gauge","scale:.55,rotation:-35,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:.9,ease:'power3.out'",0),
       ("#magic-tools","y:120,autoAlpha:0","y:0,autoAlpha:1,duration:.7,ease:'back.out(1.5)'",.75),
       ("#magic-cross","scale:0,rotation:-50,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:.6,ease:'back.out(2)'",1.35),
       ("#magic-gauge path","rotation:12,transformOrigin:'center',duration:.5,repeat:2,yoyo:true,ease:'sine.inOut'","",1.8)],
      [("#community-orbit","scale:.65,rotation:-20,autoAlpha:0","scale:1,rotation:0,autoAlpha:1,duration:.8,ease:'power3.out'",0),
       ("#community-phone","y:150,rotation:8,scale:.82,autoAlpha:0","y:0,rotation:0,scale:1,autoAlpha:1,duration:.8,ease:'back.out(1.5)'",.18),
       ("#community-bubbles path","scale:0,autoAlpha:0","scale:1,autoAlpha:1,duration:.55,stagger:.2,ease:'back.out(1.7)'",.9),
       ("#community-next","y:80,autoAlpha:0","y:0,autoAlpha:1,duration:.65,ease:'power3.out'",1.6)]
    ]
    out=[]
    for selector,frm,to,offset in plans[i]:
        if to:
            out.append(f'tl.fromTo("{s}{selector}",{{{frm}}},{{{to}}},{start+offset:.3f});')
        else:
            out.append(f'tl.to("{s}{selector}",{{{frm}}},{start+offset:.3f});')
    return "".join(out)
