# cloudservicegm-video-studio

Generador de videos verticales con HyperFrames, GSAP y dos opciones de narración: ElevenLabs desde un panel web local, o Qwen3-TTS Ryan 0.6B como alternativa. El render del video se ejecuta en GitHub Actions; tu PC solo maneja el panel y la muestra de voz.

## Panel web de ElevenLabs

1. Descarga el repositorio desde **Code → Download ZIP** y descomprímelo en Windows.
2. Instala Python 3.10 o posterior.
3. Instala GitHub CLI y Cloudflare Tunnel desde PowerShell:

   **GitHub CLI:** winget install --id GitHub.cli -e

   **Cloudflare Tunnel:** winget install --id Cloudflare.cloudflared -e

4. En PowerShell ejecuta **gh auth login** y completa el acceso a GitHub. Esto se hace una sola vez.
5. En la carpeta del proyecto, ejecuta **run_web_studio.bat**.
6. Se abrirá el panel web local en http://127.0.0.1:8765.
7. Introduce tu API key, el Voice ID, el título y el guion.
8. Pulsa **Generar y escuchar muestra**. Cuando estés satisfecho con la voz, pulsa **Renderizar video en GitHub**.
9. Mantén abierta la consola y la pestaña del navegador hasta que el panel confirme que GitHub recibió el audio.
10. Abre GitHub Actions y descarga el artefacto **cloudservicegm-video** cuando el render termine.

## Seguridad de la API key

- La interfaz web se sirve únicamente en localhost; no es una página pública ni un sitio de GitHub Pages.
- La API key se envía por la red local al servicio Python y desde ahí a ElevenLabs usando el encabezado xi-api-key.
- La clave no se escribe en archivos, repositorio, logs, artefactos, inputs de GitHub Actions ni variables de entorno.
- La clave permanece en memoria durante la solicitud de generación, se elimina del formulario y no se conserva en el estado de la aplicación.
- El panel usa el endpoint oficial POST /v1/text-to-speech/{voice_id} con el modelo eleven_multilingual_v2.
- GitHub recibe únicamente el título, el guion y una URL temporal para descargar el MP3. Esa URL es de un solo uso, usa un token aleatorio y el túnel se cierra después de la descarga.
- La URL temporal es accesible para quien la conozca mientras está activa. No compartas el enlace de ejecución durante la transferencia.
- Quick Tunnels son una función temporal de desarrollo, no una solución de alojamiento permanente.

## Requisitos

- Windows 10/11.
- Python 3.10 o posterior.
- GitHub CLI (gh), autenticado con permiso para ejecutar GitHub Actions en este repositorio.
- Cloudflare Tunnel (cloudflared).
- Acceso a Internet.
- Una API key ElevenLabs válida, el Voice ID y créditos de generación suficientes.

## Opción de respaldo: Qwen3-TTS

También puedes ejecutar manualmente **Render video** desde GitHub Actions y dejar vacío el campo de audio temporal. En ese caso se genera la narración de respaldo con Qwen3-TTS CustomVoice 0.6B (ryan).

## Qué hace el render

- Instala Node, Python y FFmpeg en el runner temporal de GitHub.
- Si recibe audio MP3 de ElevenLabs, lo descarga y convierte a WAV. Si no, genera voz con Qwen3-TTS.
- Transcribe el audio con HyperFrames para obtener marcas temporales.
- Construye una composición vertical 1080x1920 con HTML/CSS/GSAP.
- Conserva las escenas, las animaciones y los efectos de sonido sincronizados.
- Renderiza el MP4 con HyperFrames.
- Publica cloudservicegm-video como artefacto descargable durante 7 días.

## Personalización

- Cambia el estilo visual editando template/index.template.html.
- Edita el título y el guion desde el panel web.
- Usa el Voice ID de la voz que quieras probar.
- El audio se genera en MP3 44.1 kHz / 128 kbps.

## Solución de problemas

- Si la API key es rechazada, revisa la clave, la voz y los créditos de ElevenLabs.
- Si gh auth status falla, ejecuta gh auth login.
- Si falta cloudflared, instala Cloudflare Tunnel desde PowerShell.
- Si no se genera la URL temporal, comprueba tu conexión y actualiza cloudflared.
- Si GitHub no descarga el audio dentro de 15 minutos, genera otra muestra y vuelve a iniciar la transferencia.
- Si el render falla, revisa el paso rojo en GitHub Actions.
- Los artefactos de video expiran después de 7 días.
