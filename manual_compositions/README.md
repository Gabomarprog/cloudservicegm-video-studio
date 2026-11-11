# Diseños manuales por tema

Tercera modalidad del estudio: composiciones programadas manualmente por ChatGPT, independientes de la plantilla clásica y del director Gemini.

Cada diseño vive en manual_compositions/<id>/design.py y debe implementar build_design(duration, words, groups, title). Devuelve:
- css: estilos específicos del tema.
- scenes: 3–10 escenas con start/end en segundos, label, headline, detail, markup HTML/SVG y animation GSAP.
- sfx_events: efectos sincronizados usando IDs CC0 existentes en build_video.py.

Reglas:
- Cada escena necesita un objeto visual protagonista, con animación GSAP propia.
- Las escenas deben cubrir el audio sin huecos importantes.
- Cada escena debe tener al menos un efecto sonoro sincronizado.
- No se llama a Gemini ni se generan guiones automáticamente.
- No se modifican los workflows ni plantillas de las otras dos modalidades.

El catálogo visible vive en manual_compositions/registry.json. Solo se publican paquetes completos con status ready.
