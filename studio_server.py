#!/usr/bin/env python3
"""Local browser UI for cloudservicegm. ElevenLabs keys stay in this process only."""

import json
import re
import secrets
import shutil
import subprocess
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import queue
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HTML_FILE = ROOT / "web" / "index.html"
REPOSITORY = "Gabomarprog/cloudservicegm-video-studio"
WORKFLOW = ".github/workflows/render.yml"
MODEL_ID = "eleven_multilingual_v2"
HOST = "127.0.0.1"
PORT = 8765
MAX_BODY = 250_000

STATE_LOCK = threading.Lock()
STATE = {
    "preview_id": None, "audio": None, "title": None, "script": None,
    "render_running": False,
    "render_status": "Listo. Introduce los datos para crear tu primera muestra.",
    "actions_url": None,
}


def json_bytes(data):
    return json.dumps(data, ensure_ascii=False).encode("utf-8")


def set_status(message, running=None, actions_url=None):
    with STATE_LOCK:
        STATE["render_status"] = message
        if running is not None:
            STATE["render_running"] = running
        if actions_url is not None:
            STATE["actions_url"] = actions_url


class StudioHandler(BaseHTTPRequestHandler):
    server_version = "cloudservicegm-local/1.0"

    def log_message(self, fmt, *args):
        # Requests may contain narration text and credentials; do not log them.
        return

    def _headers(self, content_type, length=None):
        self.send_header("Content-Type", content_type)
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'self'; img-src 'self' data:; media-src 'self' blob:; "
            "style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'; "
            "connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"
        )
        if length is not None:
            self.send_header("Content-Length", str(length))

    def _send_json(self, status, data):
        body = json_bytes(data)
        self.send_response(status)
        self._headers("application/json; charset=utf-8", len(body))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            raise ValueError("Solicitud no válida.")
        if length <= 0 or length > MAX_BODY:
            raise ValueError("La solicitud está vacía o supera el tamaño permitido.")
        raw = self.rfile.read(length)
        try:
            data = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise ValueError("No se pudo leer el formulario.")
        if not isinstance(data, dict):
            raise ValueError("Formato de solicitud no válido.")
        return data

    def _origin_is_local(self):
        origin = self.headers.get("Origin")
        if not origin:
            return True
        return origin in (
            "http://127.0.0.1:%d" % PORT,
            "http://localhost:%d" % PORT,
        )

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            try:
                body = HTML_FILE.read_bytes()
            except OSError:
                self.send_error(500, "No se encontró web/index.html")
                return
            self.send_response(200)
            self._headers("text/html; charset=utf-8", len(body))
            self.end_headers()
            self.wfile.write(body)
            return

        if self.path == "/api/status":
            with STATE_LOCK:
                data = {
                    "render_running": STATE["render_running"],
                    "render_status": STATE["render_status"],
                    "actions_url": STATE["actions_url"],
                }
            self._send_json(200, data)
            return

        match = re.fullmatch(r"/api/audio/([A-Za-z0-9_-]{16,80})", self.path)
        if match:
            sample_id = match.group(1)
            with STATE_LOCK:
                audio = STATE["audio"] if sample_id == STATE["preview_id"] else None
            if not audio:
                self.send_error(404, "La muestra ya no está disponible.")
                return
            self.send_response(200)
            self._headers("audio/mpeg", len(audio))
            self.end_headers()
            self.wfile.write(audio)
            return

        self.send_error(404)

    def do_POST(self):
        if not self._origin_is_local():
            self._send_json(403, {"error": "Origen no permitido."})
            return
        if self.path == "/api/generate":
            self._generate()
        elif self.path == "/api/render":
            self._render()
        else:
            self.send_error(404)

    def _generate(self):
        try:
            data = self._read_json()
            api_key = str(data.get("api_key", "")).strip()
            voice_id = str(data.get("voice_id", "")).strip()
            title = str(data.get("title", "")).strip()
            script = str(data.get("script", "")).strip()

            if not api_key or len(api_key) > 500:
                raise ValueError("Introduce una API key válida de ElevenLabs.")
            if not re.fullmatch(r"[A-Za-z0-9_-]{6,128}", voice_id):
                raise ValueError("Revisa el Voice ID. Debe contener letras, números, guiones o guiones bajos.")
            if not title or len(title) > 180:
                raise ValueError("El título es obligatorio y debe tener menos de 180 caracteres.")
            if not script or len(script) > 12000:
                raise ValueError("El guion es obligatorio y no puede superar 12.000 caracteres.")

            url = (
                "https://api.elevenlabs.io/v1/text-to-speech/"
                + urllib.parse.quote(voice_id, safe="")
                + "?output_format=mp3_44100_128"
            )
            payload = json_bytes({"text": script, "model_id": MODEL_ID})
            request = urllib.request.Request(
                url, data=payload,
                headers={
                    "xi-api-key": api_key,
                    "Content-Type": "application/json",
                    "Accept": "audio/mpeg",
                },
                method="POST",
            )
            try:
                with urllib.request.urlopen(request, timeout=240) as response:
                    audio = response.read()
            except urllib.error.HTTPError as exc:
                detail = exc.read(1500).decode("utf-8", errors="replace")
                if exc.code in (401, 403):
                    message = "ElevenLabs rechazó la API key o el acceso a esa voz. Comprueba la clave y el Voice ID."
                elif exc.code == 429:
                    message = "ElevenLabs indicó un límite o falta de créditos. Revisa tu plan y cuota."
                else:
                    message = "ElevenLabs devolvió HTTP %d: %s" % (exc.code, detail[:500])
                self._send_json(502, {"error": message})
                return
            except (urllib.error.URLError, TimeoutError) as exc:
                self._send_json(502, {"error": "No se pudo conectar con ElevenLabs: %s" % exc})
                return
            finally:
                # The key is never placed in global state or written to disk.
                api_key = None

            if len(audio) < 1024:
                self._send_json(502, {"error": "ElevenLabs devolvió un audio vacío o incompleto."})
                return

            sample_id = secrets.token_urlsafe(24)
            with STATE_LOCK:
                STATE["preview_id"] = sample_id
                STATE["audio"] = audio
                STATE["title"] = title
                STATE["script"] = script
                STATE["render_status"] = "Muestra lista. Escúchala antes de lanzar el render."
                STATE["actions_url"] = None

            self._send_json(200, {
                "ok": True, "sample_id": sample_id, "model": MODEL_ID,
                "audio_bytes": len(audio),
                "message": "Audio generado. La API key no se guardó y se descartó después de la solicitud.",
            })
        except ValueError as exc:
            self._send_json(400, {"error": str(exc)})
        except Exception as exc:
            self._send_json(500, {"error": "Error interno al generar la voz: %s" % exc})

    def _render(self):
        try:
            data = self._read_json()
            sample_id = str(data.get("sample_id", ""))
            with STATE_LOCK:
                valid = (
                    sample_id and sample_id == STATE["preview_id"]
                    and STATE["audio"] is not None
                )
                already_running = STATE["render_running"]
                title = STATE["title"]
                script = STATE["script"]
                audio = STATE["audio"]

            if not valid:
                raise ValueError("Genera una muestra nueva antes de renderizar.")
            if already_running:
                raise ValueError("Ya hay una transferencia en curso.")
            missing = [name for name in ("gh", "cloudflared") if not shutil.which(name)]
            if missing:
                raise ValueError(
                    "Faltan herramientas: %s. Instálalas según el README del proyecto."
                    % ", ".join(missing)
                )
            auth = subprocess.run(
                ["gh", "auth", "status"],
                capture_output=True, text=True, timeout=20
            )
            if auth.returncode != 0:
                raise ValueError("GitHub CLI no está autenticado. Ejecuta gh auth login en PowerShell.")

            with STATE_LOCK:
                if STATE["render_running"]:
                    raise ValueError("Ya hay una transferencia en curso.")
                STATE["render_running"] = True
                STATE["render_status"] = "Preparando transferencia temporal del audio a GitHub Actions..."
                STATE["actions_url"] = "https://github.com/%s/actions/workflows/render.yml" % REPOSITORY

            worker = threading.Thread(
                target=render_worker, args=(title, script, audio), daemon=True
            )
            worker.start()
            self._send_json(200, {"ok": True, "message": "Preparando el render en la nube."})
        except ValueError as exc:
            self._send_json(400, {"error": str(exc)})
        except subprocess.TimeoutExpired:
            self._send_json(502, {"error": "La comprobación de GitHub tardó demasiado."})
        except Exception as exc:
            self._send_json(500, {"error": "No se pudo preparar el render: %s" % exc})


class OneShotAudioServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, address, token, audio):
        self.token = token
        self.audio = audio
        self.guard = threading.Lock()
        self.downloaded = threading.Event()
        self.claimed = False

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, fmt, *args):
                return

            def do_GET(self):
                if self.path != "/" + self.server.token:
                    self.send_error(404)
                    return
                with self.server.guard:
                    if self.server.claimed:
                        self.send_error(410)
                        return
                    self.server.claimed = True
                succeeded = False
                try:
                    body = self.server.audio
                    self.send_response(200)
                    self.send_header("Content-Type", "audio/mpeg")
                    self.send_header("Content-Length", str(len(body)))
                    self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
                    self.send_header("Content-Disposition", 'attachment; filename="narration.mp3"')
                    self.end_headers()
                    self.wfile.write(body)
                    self.wfile.flush()
                    succeeded = True
                except (BrokenPipeError, ConnectionResetError):
                    succeeded = False
                finally:
                    with self.server.guard:
                        if succeeded:
                            self.server.downloaded.set()
                        else:
                            self.server.claimed = False

        super().__init__(address, Handler)


def render_worker(title, script, audio):
    audio_server = None
    tunnel = None
    try:
        token = secrets.token_urlsafe(32)
        audio_server = OneShotAudioServer((HOST, 0), token, audio)
        port = audio_server.server_address[1]
        threading.Thread(target=audio_server.serve_forever, daemon=True).start()

        tunnel = subprocess.Popen(
            [
                "cloudflared", "tunnel", "--url",
                "http://%s:%d" % (HOST, port),
                "--no-autoupdate",
            ],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        url_queue = queue.Queue(maxsize=1)

        def read_tunnel():
            try:
                for line in tunnel.stdout:
                    match = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", line)
                    if match:
                        try:
                            url_queue.put_nowait(match.group(0))
                        except queue.Full:
                            pass
                        return
            except Exception:
                return

        threading.Thread(target=read_tunnel, daemon=True).start()
        try:
            tunnel_url = url_queue.get(timeout=90)
        except queue.Empty:
            raise RuntimeError("Cloudflare no generó una URL temporal. Comprueba la conexión y cloudflared.")

        action_inputs = {
            "title": title,
            "script": script,
            "audio_url": tunnel_url + "/" + token,
        }
        result = subprocess.run(
            [
                "gh", "workflow", "run", WORKFLOW,
                "--repo", REPOSITORY, "--ref", "main", "--json",
            ],
            input=json.dumps(action_inputs, ensure_ascii=False),
            capture_output=True, text=True, timeout=90,
        )
        if result.returncode != 0:
            raise RuntimeError(
                (result.stderr or result.stdout or "GitHub no aceptó el workflow.").strip()[:900]
            )

        actions_url = "https://github.com/%s/actions/workflows/render.yml" % REPOSITORY
        set_status(
            "GitHub Actions inició el trabajo. Esperando la descarga del audio temporal...",
            running=True, actions_url=actions_url,
        )
        try:
            webbrowser.open(actions_url)
        except Exception:
            pass

        deadline = time.monotonic() + 900
        while time.monotonic() < deadline:
            if audio_server.downloaded.wait(timeout=0.5):
                set_status(
                    "GitHub recibió el audio. La URL temporal se consumió y el túnel se cerrará. "
                    "El render del MP4 continúa en GitHub Actions.",
                    running=False, actions_url=actions_url,
                )
                return

        raise RuntimeError("GitHub no descargó el audio dentro de 15 minutos. Vuelve a iniciar la transferencia.")
    except Exception as exc:
        set_status("No se completó la transferencia: %s" % exc, running=False)
    finally:
        if tunnel is not None:
            try:
                tunnel.terminate()
                tunnel.wait(timeout=5)
            except Exception:
                try:
                    tunnel.kill()
                except Exception:
                    pass
        if audio_server is not None:
            try:
                audio_server.shutdown()
                audio_server.server_close()
            except Exception:
                pass
        with STATE_LOCK:
            STATE["audio"] = None
            STATE["preview_id"] = None


def main():
    if not HTML_FILE.is_file():
        raise SystemExit("No se encontró la interfaz web: %s" % HTML_FILE)
    server = ThreadingHTTPServer((HOST, PORT), StudioHandler)
    address = "http://%s:%d" % (HOST, server.server_address[1])
    print("cloudservicegm Video Studio está listo en %s" % address)
    print("Mantén esta ventana abierta mientras uses el panel web.")
    try:
        webbrowser.open(address)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando el estudio...")
    finally:
        with STATE_LOCK:
            STATE["audio"] = None
            STATE["preview_id"] = None
        server.shutdown()
        server.server_close()


if __name__ == "__main__":
    main()
