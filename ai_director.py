#!/usr/bin/env python3
"""Gemini-powered Spanish script and motion-graphics storyboard director."""
from __future__ import annotations
import json
import urllib.error
import urllib.parse
import urllib.request

MODEL = "gemini-3.6-flash"
VISUALS = [
    "typography","browser","certificate","network","shield","server","dashboard",
    "database","terminal","phone","comparison","process","chart","timeline","webpage","cta"
]
SCHEMA = {
    "type":"OBJECT",
    "properties":{
        "title":{"type":"STRING"},
        "script":{"type":"STRING"},
        "scenes":{"type":"ARRAY","minItems":4,"maxItems":7,"items":{
            "type":"OBJECT",
            "properties":{
                "visual":{"type":"STRING","enum":VISUALS},
                "label":{"type":"STRING"},
                "headline":{"type":"STRING"},
                "detail":{"type":"STRING"},
                "chips":{"type":"ARRAY","items":{"type":"STRING"}},
                "stat":{"type":"STRING"}
            },
            "required":["visual","label","headline","detail","chips","stat"]
        }}
    },
    "required":["title","script","scenes"]
}

def create_director_plan(api_key, topic, transcript=None, desired_title=None, duration=55):
    key=str(api_key or "").strip()
    if not key or len(key)>500:
        raise ValueError("Introduce una API key de Google AI Studio para activar el director creativo.")
    topic=str(topic or "").strip()
    if not topic or len(topic)>500:
        raise ValueError("Escribe el tema del video (máximo 500 caracteres).")
    has_audio=bool(str(transcript or "").strip())
    mode_instruction = (
        "El usuario ya tiene una narración grabada. NO la reescribas, NO cambies lo que dice y devuelve script como cadena vacía. "
        "Usa esta transcripción únicamente para diseñar escenas que representen fielmente lo que se está narrando:\n"+str(transcript)[:12000]
        if has_audio else
        f"Escribe un guion original de español latino natural para unos {duration} segundos, con gancho inicial, explicación clara, desarrollo y cierre. No uses encabezados ni acotaciones; solo el texto que se narrará."
    )
    prompt = f"""
Eres director creativo y guionista especializado en motion graphics premium para videos verticales 9:16 hechos con HTML, CSS, SVG y GSAP. No generas video realista ni clips genéricos.
Tema: {topic}
Título sugerido: {desired_title or topic}
Duración objetivo: {duration} segundos.
Identidad: marca cloudservicegm, estética editorial/tecnológica, negro carbón, blanco cálido, rojo coral y verde menta; tipografía cinética grande; transiciones fluidas; objetos y diagramas vectoriales con profundidad, sombras y movimiento.
{mode_instruction}

Devuelve 4 a 7 escenas ordenadas. Cada escena debe tener un concepto visual DIFERENTE y relacionado directamente con lo que se cuenta en ese momento. Selecciona visual de esta biblioteca: {", ".join(VISUALS)}.
No repitas un mismo objeto principal en escenas consecutivas. No uses teléfono, servidores, dashboards o candados por defecto: utilízalos solo cuando el tema y la narración lo justifiquen. Alterna objetos, composiciones, comparaciones, líneas de proceso y tipografía. La última escena debe usar visual "cta" y cerrar con cloudservicegm.
headline muy breve (máximo 7 palabras); detail una línea breve; chips de 2 a 4 etiquetas breves; stat un dato o palabra muy corta, no inventes estadísticas. No incluyas instrucciones HTML, CSS, JavaScript, código, URLs, ni atributos. Devuelve SOLO el JSON solicitado.
No inventes datos numéricos, normativas ni promesas técnicas no indicadas por el usuario. Si falta certeza, usa explicaciones generales.
"""
    url="https://generativelanguage.googleapis.com/v1beta/models/"+MODEL+":generateContent?key="+urllib.parse.quote(key,safe="")
    body={
      "contents":[{"role":"user","parts":[{"text":prompt}]}],
      "generationConfig":{"temperature":0.8,"responseMimeType":"application/json","responseJsonSchema":SCHEMA}
    }
    request=urllib.request.Request(url,data=json.dumps(body,ensure_ascii=False).encode("utf-8"),headers={"Content-Type":"application/json"},method="POST")
    try:
        with urllib.request.urlopen(request,timeout=150) as response:
            payload=json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail=exc.read(1800).decode("utf-8",errors="replace")
        if exc.code in (401,403):
            raise RuntimeError("Google Gemini rechazó la API key. Comprueba que sea una clave de Google AI Studio.")
        if exc.code==429:
            raise RuntimeError("Google Gemini alcanzó el límite de solicitudes de la cuota gratuita. Inténtalo más tarde.")
        raise RuntimeError(f"Gemini devolvió HTTP {exc.code}: {detail[:700]}")
    except (urllib.error.URLError,TimeoutError) as exc:
        raise RuntimeError(f"No se pudo conectar con Google Gemini: {exc}")
    try:
        raw=payload["candidates"][0]["content"]["parts"][0]["text"]
        result=json.loads(raw)
    except Exception as exc:
        raise RuntimeError("Gemini no devolvió un storyboard JSON válido.") from exc
    scenes=result.get("scenes")
    if not isinstance(scenes,list) or len(scenes)<4:
        raise RuntimeError("El director no generó suficientes escenas. Inténtalo de nuevo.")
    cleaned=[]
    for scene in scenes[:7]:
        if not isinstance(scene,dict): continue
        visual=scene.get("visual")
        if visual not in VISUALS: visual="process"
        cleaned.append({
          "visual":visual,
          "label":str(scene.get("label",""))[:48],
          "headline":str(scene.get("headline",""))[:100],
          "detail":str(scene.get("detail",""))[:180],
          "chips":[str(x)[:28] for x in scene.get("chips",[])[:4]],
          "stat":str(scene.get("stat",""))[:24]
        })
    if not cleaned: raise RuntimeError("El storyboard está vacío.")
    if cleaned[-1]["visual"]!="cta":
        cleaned.append({"visual":"cta","label":"CIERRE","headline":"HABLEMOS DE TU PROYECTO","detail":"Cloudservicegm · VPS · Cloud · Web","chips":[],"stat":"C"})
    result["title"]=str(result.get("title") or desired_title or topic)[:180]
    result["script"]=str(result.get("script") or "")[:12000] if not has_audio else ""
    result["scenes"]=cleaned[:8]
    return result
