# cloudservicegm-video-studio

Generador de videos verticales con HyperFrames, GSAP y la voz Kokoro `em_alex` en español, ejecutado en GitHub Actions.
Tu PC solo necesita un navegador. El render y la síntesis de voz ocurren en el runner de GitHub.

## Primer uso

1. Crea un repositorio público en GitHub llamado `cloudservicegm-video-studio`.
2. Sube todos los archivos de este paquete conservando sus carpetas.
3. Abre la pestaña **Actions** del repositorio y habilita GitHub Actions si GitHub lo solicita.
4. En Actions, selecciona **Render video**.
5. Pulsa **Run workflow**.
6. Escribe el título y pega el guion en español. Pulsa **Run workflow**.
7. Espera a que el trabajo termine en verde.
8. Abre la ejecución y descarga el artefacto `cloudservicegm-video`.

## Qué hace el workflow

- Instala Node, FFmpeg y espeak-ng en el servidor temporal de GitHub.
- Genera la voz con Kokoro ONNX, voz masculina española `em_alex`, velocidad original `1.0`.
- Transcribe la voz con HyperFrames para obtener marcas temporales.
- Construye una composición vertical 1080x1920 con HTML/CSS/GSAP.
- Renderiza el MP4 con HyperFrames.
- Publica el MP4 como artefacto descargable durante 7 días.

## Personalización

- Cambia el estilo visual editando `template/index.template.html`.
- Esta versión recupera la voz inicial `em_alex` con el mismo idioma y velocidad del primer render. No se insertan pausas artificiales.
- Las voces españolas disponibles incluyen `ef_dora`, `em_alex` y `em_santa`. Comprueba las opciones con `npx hyperframes tts --list`.

## Límites y privacidad

- Repositorio público: el código y el guion de ejemplo que se guarde en el repositorio son visibles. Los guiones introducidos en el formulario de ejecución se pasan al job y aparecen en los logs solo si un comando los imprime; evita datos confidenciales.
- GitHub Actions estándar es gratuito para repositorios públicos, sujeto a las condiciones y límites de GitHub.
- Los artefactos expiran; este workflow los conserva 7 días.
- No se instala ni ejecuta nada en tu PC.
- La primera ejecución puede tardar más porque descarga modelos y dependencias.
- Kokoro ONNX se ejecuta en el runner de GitHub. No requiere una API comercial ni clona la voz de una persona.

## Solución de problemas

- Si falla la síntesis, abre el log del paso `Generar narración en español con Kokoro em_alex` y comprueba la instalación de `kokoro-onnx`.
- Si falla la transcripción, revisa el paso `Transcribir narración`. El modelo `large-v3` puede tardar en descargarse y procesarse.
- Si falla el render, revisa `Validar composición` y `Renderizar MP4`.
- Descarga los logs desde la ejecución fallida antes de cambiar versiones o dependencias.
