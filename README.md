# cloudservicegm-video-studio

Generador de videos verticales con HyperFrames, GSAP y dos vías para proporcionar narración: generar con la API de ElevenLabs o importar un archivo de audio creado con cualquier otra herramienta. El render del video se ejecuta en GitHub Actions.

## Elegir cómo proporcionar el audio

Al abrir el panel web local, el primer selector permite elegir:

### Generar con API de ElevenLabs
1. Selecciona **Generar con API de ElevenLabs**.
2. Introduce la API key y el Voice ID.
3. Completa el título y el guion.
4. Pulsa **Generar y escuchar muestra**.
5. Si la voz te convence, pulsa **Renderizar video en GitHub**.

La conexión API incluida actualmente es específica de ElevenLabs. No existe un formato universal para las API de texto a voz: cada proveedor puede requerir una autenticación, endpoint, modelo y estructura de petición diferentes. Para usar otro proveedor sin cambiar el programa, genera y descarga el audio en ese servicio y utiliza el modo de importación. Se pueden añadir adaptadores específicos para otros proveedores en futuras versiones.

### Importar audio ya generado
1. Selecciona **Importar audio ya generado**.
2. Elige un archivo de audio de tu PC.
3. Completa el título. El guion es opcional en este modo porque los subtítulos se transcriben desde el audio.
4. Pulsa **Importar audio y escuchar muestra**.
5. Reproduce la vista previa para comprobar que sea el archivo correcto.
6. Pulsa **Renderizar video en GitHub** cuando estés conforme.

Formatos admitidos: MP3, WAV, M4A, AAC, OGG, OPUS, FLAC y WEBM. Tamaño máximo: 120 MB. El audio se procesa con FFmpeg en GitHub Actions y se convierte a WAV para la transcripción y el render.

## Instalación en Windows

1. Descarga el repositorio desde **Code → Download ZIP** y descomprímelo.
2. Instala Python 3.10 o posterior.
3. Instala GitHub CLI y Cloudflare Tunnel desde PowerShell:

   **GitHub CLI:** winget install --id GitHub.cli -e

   **Cloudflare Tunnel:** winget install --id Cloudflare.cloudflared -e

4. Ejecuta gh auth login y completa el acceso a GitHub una sola vez.
5. Ejecuta run_web_studio.bat en la carpeta del proyecto.
6. Se abrirá el panel en http://127.0.0.1:8765.
7. Mantén abierta la consola del servidor local mientras utilizas el panel y hasta que GitHub confirme que recibió el audio.

## Seguridad y transferencia

- El panel se ejecuta solo en localhost; no es una web pública.
- La API key de ElevenLabs se envía al servicio local y desde allí a ElevenLabs. No se guarda en archivos, repositorio, logs, artefactos, inputs de GitHub Actions ni variables de entorno.
- En modo importar no se solicita API key ni Voice ID.
- El archivo de audio se mantiene temporalmente en memoria del servicio local y se previsualiza desde el propio panel.
- El panel transfiere el archivo a GitHub mediante una URL Quick Tunnel aleatoria de un solo uso. El enlace se cierra después de la descarga confirmada.
- La URL temporal es accesible para quien la conozca mientras está activa. No compartas el enlace de ejecución durante la transferencia.
- Quick Tunnels son una función temporal de desarrollo, no un servicio de alojamiento permanente.

## Requisitos

- Windows 10/11 y Python 3.10 o posterior.
- GitHub CLI (gh), autenticado con permiso para ejecutar Actions en este repositorio.
- Cloudflare Tunnel (cloudflared).
- Internet.
- Para el modo API, una API key ElevenLabs y créditos suficientes.
- Para el modo importar, un archivo de audio compatible.

## Qué hace el render

- Descarga el proyecto en el runner temporal de GitHub.
- Recibe el audio generado por ElevenLabs o el audio importado desde el panel.
- Convierte la pista a WAV mediante FFmpeg, detectando el formato real del archivo.
- Transcribe la narración con HyperFrames para obtener marcas temporales.
- Construye la composición vertical 1080x1920 con HTML/CSS/GSAP.
- Conserva las escenas, las animaciones y los efectos de sonido sincronizados.
- Renderiza el MP4 con HyperFrames.
- Publica el artefacto cloudservicegm-video durante 7 días.

## Opción de respaldo: Qwen3-TTS

Si ejecutas manualmente **Render video** desde GitHub Actions y dejas vacío el campo audio_url, se genera la narración de respaldo con Qwen3-TTS CustomVoice 0.6B (ryan).
