# cloudservicegm-video-studio

Estudio local para producir videos verticales **HTML/CSS/SVG/GSAP → MP4** con HyperFrames y GitHub Actions. La dirección creativa se adapta al tema: Gemini propone el guion (cuando se solicita) y elige escenas de una biblioteca de motion graphics; no genera clips de video realistas.

## Flujo nuevo

1. **Tema y director creativo:** escribe el tema y usa Google AI Studio para crear un guion y una propuesta visual. También puedes escribir el guion manualmente.
2. **Narración:** genera el audio con ElevenLabs o importa una narración propia.
3. **Transcripción remota:** el workflow `.github/workflows/ai-video.yml` normaliza el audio y ejecuta Whisper large-v3 en GitHub Actions. Devuelve el JSON de transcripción al panel local mediante un Cloudflare Quick Tunnel temporal.
4. **Revisión:** el panel muestra el texto reconocido. Puedes corregirlo directamente antes de continuar. Al editar, el sistema conserva las marcas temporales de las palabras coincidentes e interpola tiempos para las palabras insertadas o sustituidas.
5. **Storyboard:** al confirmar, el director Gemini toma el tema y la transcripción corregida para elegir los componentes visuales y crear el storyboard.
6. **Render:** el panel envía de nuevo el audio, la transcripción revisada y el storyboard al workflow. El constructor crea una composición HTML diferente para ese tema, HyperFrames la valida y renderiza el MP4.
7. **Descarga:** GitHub Actions publica el MP4 como artefacto durante 7 días.

## Director creativo Gemini

- Crear una API key en [Google AI Studio](https://aistudio.google.com/app/apikey).
- Pegarla en el campo correspondiente del panel.
- El modelo configurado actualmente es `gemini-3.6-flash`.
- La API key se envía desde el servidor local a Google mediante HTTPS en la cabecera de autenticación; no se guarda en el repositorio ni se envía a GitHub Actions.
- La cuota gratuita de Gemini tiene límites variables. Consulta [precios y cuotas oficiales](https://ai.google.dev/gemini-api/docs/pricing). En el nivel gratuito, Google indica que el contenido puede utilizarse para mejorar sus productos; no envíes información sensible.

La IA devuelve JSON estructurado, no código ejecutable. El renderer solo admite componentes de una lista controlada en `dynamic_scenes.py`: navegador, certificado, red, escudo, servidores, dashboard, base de datos, terminal, teléfono, comparativa, proceso, gráfico, cronología, tipografía y CTA. El motor decide el HTML y las animaciones GSAP con esos componentes.

## Proveedores de audio

### ElevenLabs
1. Selecciona **Generar voz con ElevenLabs**.
2. Introduce API key y Voice ID.
3. Escribe el guion o créalo previamente con el director Gemini.
4. Genera y escucha la muestra.

### Importar audio
1. Selecciona **Importar audio ya generado**.
2. Elige MP3, WAV, M4A, AAC, OGG, OPUS, FLAC o WEBM (máximo 120 MB).
3. Escucha la vista previa.

Ambos caminos continúan por la misma transcripción remota y revisión antes del render.

## Instalación en Windows

1. Descarga el ZIP del repositorio y extráelo en una carpeta nueva (conserva la carpeta anterior como respaldo).
2. Instala Python 3.10 o posterior.
3. Instala GitHub CLI y Cloudflare Tunnel:

   ```powershell
   winget install --id GitHub.cli -e
   winget install --id Cloudflare.cloudflared -e
   ```

4. Ejecuta `gh auth login` una sola vez y autoriza GitHub Actions.
5. Ejecuta `run_web_studio.bat`.
6. El panel se abrirá en [http://127.0.0.1:8765](http://127.0.0.1:8765).
7. Mantén abierta la consola mientras se transfiere el audio y vuelve la transcripción.

## Recursos y privacidad

- El navegador abre un panel servido solo en `127.0.0.1`; no es un sitio público.
- El PC no ejecuta modelos locales ni renderiza el MP4. Solo sirve la interfaz, recibe los archivos elegidos y crea un túnel temporal.
- Las llamadas a Gemini y ElevenLabs salen del servidor local, pero sus claves no se incluyen en inputs, logs ni archivos del workflow.
- El audio se transfiere con un Quick Tunnel aleatorio. La URL es un token temporal accesible para quien la conozca mientras esté activa.
- Whisper, FFmpeg, HyperFrames, Chromium y el render se ejecutan en GitHub Actions. Hay dos ejecuciones: una para transcribir y otra para renderizar. Se usa `actions/cache` para conservar las cachés habituales de modelos y dependencias entre jobs cuando las rutas coinciden.
- El workflow anterior `.github/workflows/render.yml` se conserva como generador estático de respaldo. El panel nuevo utiliza `.github/workflows/ai-video.yml`.

## Comprobaciones

- `.github/workflows/check-ubuntu-repos.yml`: prueba DNS y HTTPS de los repositorios de Ubuntu sin instalar paquetes.
- `.github/workflows/validate-studio.yml`: comprueba sintaxis Python, la alineación de la transcripción, la generación de escenas y los documentos HTML.
