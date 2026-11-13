#!/usr/bin/env python3
"""Standalone local UI for manually art-directed, topic-specific compositions.

Runs on port 8766 and uses its own process state. It does not import or mutate
the existing classic/Gemini studio state.
"""
from __future__ import annotations
import base64
import json
import mimetypes
import os
import queue
import re
import secrets
import shutil
import subprocess
import threading
import time
import urllib.parse
import urllib.request
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from transcript_utils import flatten_transcript, transcript_text, align_edited_text

ROOT = Path(__file__).resolve().parent
HTML_FILE = ROOT / "web" / "manual.html"
REGISTRY_FILE = ROOT / "manual_compositions" / "registry.json"
REPOSITORY = "Gabomarprog/cloudservicegm-video-studio"
TRANSCRIBE_WORKFLOW = ".github/workflows/ai-video.yml"
RENDER_WORKFLOW = ".github/workflows/manual-render.yml"
HOST = "127.0.0.1"
PORT = 8766
MAX_AUDIO = 120 * 1024 * 1024
MAX_JSON = 250_000


# Remote catalog sync: fetch only the manual renderer and published compositions.
# The existing local studio stays in place; no full-project download is required.
SYNC_INTERVAL = 120
SYNC_LOCK = threading.Lock()
SYNC_LAST_ATTEMPT = 0.0
SYNC_MESSAGE = "Todavía no se ha comprobado el catálogo remoto."

def _fetch_repo_text(path, max_bytes=750_000, optional=False):
    url = f"https://raw.githubusercontent.com/{REPOSITORY}/main/{path}"
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "cloudservicegm-manual-studio/1.0",
            "Cache-Control": "no-cache",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            raw = response.read(max_bytes + 1)
    except urllib.error.HTTPError as exc:
        if optional and exc.code == 404:
            return None
        raise RuntimeError(f"No se pudo descargar {path} (HTTP {exc.code}).") from exc
    if len(raw) > max_bytes:
        raise RuntimeError(f"El archivo remoto {path} supera el tamaño permitido.")
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise RuntimeError(f"El archivo remoto {path} no es UTF-8 válido.") from exc

def _atomic_write(path, content):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".download")
    try:
        temporary.write_text(content, encoding="utf-8", newline="\n")
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink(missing_ok=True)
        except Exception:
            pass

def sync_manual_catalog(force=False):
    """Update manual-only files from the trusted GitHub repository."""
    global SYNC_LAST_ATTEMPT, SYNC_MESSAGE
    now = time.monotonic()
    if not force and now - SYNC_LAST_ATTEMPT < SYNC_INTERVAL:
        return SYNC_MESSAGE
    with SYNC_LOCK:
        now = time.monotonic()
        if not force and now - SYNC_LAST_ATTEMPT < SYNC_INTERVAL:
            return SYNC_MESSAGE
        SYNC_LAST_ATTEMPT = now
        try:
            registry_text = _fetch_repo_text("manual_compositions/registry.json", 100_000)
            registry = json.loads(registry_text)
            if registry.get("schema_version") != 1:
                raise RuntimeError("La versión del catálogo remoto no es compatible.")
            compositions = registry.get("compositions")
            if not isinstance(compositions, list) or len(compositions) > 50:
                raise RuntimeError("El catálogo remoto tiene una estructura no válida.")

            pending = []
            # Keep the local catalogue untouched if any published design cannot
            # be fetched and validated completely.
            builder_text = _fetch_repo_text("build_manual_video.py", 300_000)
            compile(builder_text, "build_manual_video.py", "exec")
            pending.append((ROOT / "build_manual_video.py", builder_text))

            ready_count = 0
            for item in compositions:
                if not isinstance(item, dict) or item.get("status") != "ready":
                    continue
                cid = str(item.get("id", ""))
                if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{1,48}", cid):
                    raise RuntimeError("El catálogo contiene un ID de composición no válido.")
                base = f"manual_compositions/{cid}"
                design_text = _fetch_repo_text(base + "/design.py", 500_000)
                compile(design_text, base + "/design.py", "exec")
                pending.append((ROOT / base / "design.py", design_text))

                narration_text = _fetch_repo_text(base + "/narration_es.txt", 30_000, optional=True)
                if narration_text is not None:
                    pending.append((ROOT / base / "narration_es.txt", narration_text))
                ready_count += 1

            # Write code/package files first and publish the registry last.
            for path, text_content in pending:
                _atomic_write(path, text_content)
            _atomic_write(REGISTRY_FILE, json.dumps(registry, ensure_ascii=False, indent=2) + "\n")
            SYNC_MESSAGE = f"Catálogo actualizado desde GitHub: {ready_count} diseños disponibles."
        except Exception as exc:
            SYNC_MESSAGE = f"No se pudo actualizar desde GitHub; se conserva el catálogo local. {str(exc)[:240]}"
        return SYNC_MESSAGE

LOCK = threading.Lock()
STATE = {
    "preview_id": None,
    "audio": None,
    "audio_mime": "audio/mpeg",
    "title": "",
    "composition_id": "",
    "transcript_data": None,
    "running": False,
    "status": "Selecciona un diseño manual para comenzar.",
    "actions_url": None,
}

def json_bytes(value):
    return json.dumps(value, ensure_ascii=False).encode("utf-8")

def catalog():
    sync_manual_catalog()
    try:
        data = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []
    result = []
    for item in data.get("compositions", []):
        if not isinstance(item, dict) or item.get("status") != "ready":
            continue
        cid = str(item.get("id", ""))
        if not re.fullmatch(r"[a-z0-9][a-z0-9_-]{1,48}", cid):
            continue
        if not (ROOT / "manual_compositions" / cid / "design.py").is_file():
            continue
        result.append({
            "id": cid,
            "title": str(item.get("title") or cid)[:100],
            "topic": str(item.get("topic") or "")[:160],
            "description": str(item.get("description") or "")[:300],
        })
    return result

def set_status(message, running=None, actions_url=None):
    with LOCK:
        STATE["status"] = message
        if running is not None:
            STATE["running"] = running
        if actions_url is not None:
            STATE["actions_url"] = actions_url

class AudioBridgeServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, address, token, audio, audio_mime):
        self.token = token
        self.audio = audio
        self.audio_mime = audio_mime
        self.downloaded = threading.Event()
        self.transcript_received = threading.Event()
        self.transcript_payload = None
        self.lock = threading.Lock()
        self.download_count = 0

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, fmt, *args):
                return

            def do_GET(self):
                if self.path != "/" + self.server.token:
                    self.send_error(404)
                    return
                with self.server.lock:
                    if self.server.downloaded.is_set() or self.server.download_count >= 8:
                        self.send_error(410)
                        return
                    self.server.download_count += 1
                body = self.server.audio
                try:
                    self.send_response(200)
                    self.send_header("Content-Type", self.server.audio_mime)
                    self.send_header("Content-Length", str(len(body)))
                    self.send_header("Cache-Control", "no-store")
                    self.send_header("Content-Disposition", 'attachment; filename="manual-narration"')
                    self.end_headers()
                    self.wfile.write(body)
                    self.wfile.flush()
                except (BrokenPipeError, ConnectionResetError):
                    pass

            def do_POST(self):
                route = urllib.parse.urlsplit(self.path).path
                if route == "/" + self.server.token + "/complete":
                    self.server.downloaded.set()
                    self.send_response(204)
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                if route == "/" + self.server.token + "/transcript":
                    try:
                        size = int(self.headers.get("Content-Length", "0"))
                        if size <= 0 or size > 2_000_000:
                            self.send_error(413)
                            return
                        payload = json.loads(self.rfile.read(size).decode("utf-8"))
                        if not flatten_transcript(payload):
                            self.send_error(422, "No timed words in transcript.")
                            return
                        self.server.transcript_payload = payload
                        self.server.transcript_received.set()
                        self.send_response(204)
                        self.send_header("Content-Length", "0")
                        self.end_headers()
                    except Exception:
                        self.send_error(400, "Invalid transcript.")
                    return
                self.send_error(404)
        super().__init__(address, Handler)

def open_tunnel(audio, audio_mime):
    token = secrets.token_urlsafe(32)
    bridge = AudioBridgeServer((HOST, 0), token, audio, audio_mime)
    threading.Thread(target=bridge.serve_forever, daemon=True).start()
    tunnel = subprocess.Popen(
        ["cloudflared", "tunnel", "--url", f"http://{HOST}:{bridge.server_address[1]}", "--no-autoupdate"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    found = queue.Queue(maxsize=1)
    def scan():
        try:
            for line in tunnel.stdout:
                match = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", line)
                if match:
                    try:
                        found.put_nowait(match.group(0))
                    except queue.Full:
                        pass
                    return
        except Exception:
            pass
    threading.Thread(target=scan, daemon=True).start()
    try:
        url = found.get(timeout=90)
    except queue.Empty:
        tunnel.terminate()
        bridge.shutdown()
        bridge.server_close()
        raise RuntimeError("Cloudflare no generó el túnel temporal.")
    return bridge, tunnel, url + "/" + token

def dispatch_workflow(workflow, inputs):
    command = [
        "gh", "workflow", "run", workflow, "--repo", REPOSITORY,
        "--ref", "main", "--json"
    ]
    result = subprocess.run(
        command, input=json.dumps(inputs, ensure_ascii=False),
        capture_output=True, text=True, timeout=90
    )
    if result.returncode:
        raise RuntimeError((result.stderr or result.stdout or "GitHub rechazó el workflow.").strip()[:1000])

def worker(stage, title, composition_id, audio, audio_mime, transcript_json=None):
    bridge = tunnel = None
    actions = (
        f"https://github.com/{REPOSITORY}/actions/workflows/"
        + ("ai-video.yml" if stage == "transcribe" else "manual-render.yml")
    )
    try:
        bridge, tunnel, audio_url = open_tunnel(audio, audio_mime)
        if stage == "transcribe":
            inputs = {
                "stage": "transcribe",
                "title": title,
                "audio_url": audio_url,
                "callback_url": audio_url,
            }
            dispatch_workflow(TRANSCRIBE_WORKFLOW, inputs)
            set_status("GitHub está transcribiendo el audio. El render todavía no ha comenzado.", True, actions)
            try:
                webbrowser.open(actions)
            except Exception:
                pass
            deadline = time.monotonic() + 1200
            while time.monotonic() < deadline:
                if bridge.downloaded.is_set() and bridge.transcript_received.is_set():
                    with LOCK:
                        STATE["transcript_data"] = bridge.transcript_payload
                    set_status(
                        "Transcripción recibida. Corrige el texto antes de confirmar el diseño.",
                        False, actions
                    )
                    return
                time.sleep(.35)
            raise RuntimeError("No llegó la transcripción. Revisa la ejecución de GitHub Actions.")
        inputs = {
            "title": title,
            "composition_id": composition_id,
            "audio_url": audio_url,
            "transcript_json_b64": base64.b64encode(transcript_json).decode("ascii"),
        }
        dispatch_workflow(RENDER_WORKFLOW, inputs)
        set_status("GitHub está recibiendo el audio y preparando el diseño manual.", True, actions)
        try:
            webbrowser.open(actions)
        except Exception:
            pass
        deadline = time.monotonic() + 900
        while time.monotonic() < deadline:
            if bridge.downloaded.wait(.4):
                set_status(
                    "GitHub recibió el audio. El ensamblado del MP4 continúa en Actions.",
                    False, actions
                )
                return
        raise RuntimeError("GitHub no descargó el audio en 15 minutos.")
    except Exception as exc:
        set_status("No se completó el proceso: " + str(exc), False, actions)
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
        if bridge is not None:
            try:
                bridge.shutdown()
                bridge.server_close()
            except Exception:
                pass
        if stage == "render":
            with LOCK:
                STATE["audio"] = None
                STATE["preview_id"] = None

class ManualHandler(BaseHTTPRequestHandler):
    server_version = "cloudservicegm-manual/1.0"

    def log_message(self, fmt, *args):
        return

    def send_json(self, status, data):
        body = json_bytes(data)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def read_json(self):
        size = int(self.headers.get("Content-Length", "0"))
        if size <= 0 or size > MAX_JSON:
            raise ValueError("Solicitud vacía o demasiado grande.")
        data = json.loads(self.rfile.read(size).decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("Formato de solicitud no válido.")
        return data

    def local_origin(self):
        origin = self.headers.get("Origin")
        return not origin or origin in (f"http://127.0.0.1:{PORT}", f"http://localhost:{PORT}")

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            body = HTML_FILE.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path == "/api/catalog":
            self.send_json(200, {"compositions": catalog()})
            return
        if self.path == "/api/status":
            with LOCK:
                self.send_json(200, {
                    "running": STATE["running"],
                    "status": STATE["status"],
                    "actions_url": STATE["actions_url"],
                    "transcript_ready": STATE["transcript_data"] is not None,
                })
            return
        if self.path == "/api/transcript":
            with LOCK:
                data = STATE["transcript_data"]
            if data is None:
                self.send_json(404, {"error": "Todavía no hay transcripción."})
            else:
                self.send_json(200, {"text": transcript_text(data)})
            return
        match = re.fullmatch(r"/api/audio/([A-Za-z0-9_-]{16,80})", self.path)
        if match:
            with LOCK:
                audio = STATE["audio"] if match.group(1) == STATE["preview_id"] else None
                mime = STATE["audio_mime"]
            if audio is None:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(audio)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(audio)
            return
        self.send_error(404)

    def do_POST(self):
        if not self.local_origin():
            self.send_json(403, {"error": "Origen no permitido."})
            return
        route = urllib.parse.urlsplit(self.path).path
        try:
            if route == "/api/upload":
                self.upload_audio()
            elif route == "/api/transcribe":
                self.start_transcription()
            elif route == "/api/render":
                self.start_render()
            else:
                self.send_error(404)
        except ValueError as exc:
            self.send_json(400, {"error": str(exc)})
        except Exception as exc:
            self.send_json(500, {"error": str(exc)[:900]})

    def upload_audio(self):
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
        composition_id = str((query.get("composition_id") or [""])[0])
        title = str((query.get("title") or [""])[0]).strip()
        filename = str((query.get("filename") or ["audio"])[0])
        available = {x["id"] for x in catalog()}
        if composition_id not in available:
            raise ValueError("Ese diseño todavía no está publicado. Primero hay que terminar su composición visual.")
        if not title or len(title) > 180:
            raise ValueError("Escribe un título de hasta 180 caracteres.")
        size = int(self.headers.get("Content-Length", "0"))
        if size < 1024 or size > MAX_AUDIO:
            raise ValueError("El audio debe pesar entre 1 KB y 120 MB.")
        mime = self.headers.get("Content-Type", "").split(";", 1)[0].lower()
        if not mime.startswith("audio/"):
            extension = Path(filename).suffix.lower()
            mime = {
                ".mp3":"audio/mpeg",".wav":"audio/wav",".m4a":"audio/mp4",
                ".aac":"audio/aac",".ogg":"audio/ogg",".opus":"audio/opus",
                ".flac":"audio/flac",".webm":"audio/webm",".3gp":"audio/3gpp"
            }.get(extension, mimetypes.guess_type(filename)[0] or "")
        if not mime.startswith("audio/"):
            raise ValueError("Formato no admitido. Usa MP3, WAV, M4A, AAC, OGG, OPUS, FLAC o WEBM.")
        audio = self.rfile.read(size)
        if len(audio) != size:
            raise ValueError("La carga del audio quedó incompleta.")
        sample_id = secrets.token_urlsafe(24)
        with LOCK:
            STATE.update({
                "preview_id": sample_id, "audio": audio, "audio_mime": mime,
                "title": title, "composition_id": composition_id,
                "transcript_data": None, "running": False,
                "status": "Audio importado. Escúchalo antes de transcribir.",
                "actions_url": None,
            })
        self.send_json(200, {"ok": True, "sample_id": sample_id, "audio_bytes": len(audio)})

    def start_transcription(self):
        data = self.read_json()
        sample_id = str(data.get("sample_id", ""))
        with LOCK:
            valid = bool(sample_id and sample_id == STATE["preview_id"] and STATE["audio"])
            running = STATE["running"]
            title, audio, mime, composition_id = STATE["title"], STATE["audio"], STATE["audio_mime"], STATE["composition_id"]
        if not valid:
            raise ValueError("Importa el audio antes de transcribir.")
        if running:
            raise ValueError("Ya hay un proceso activo.")
        missing = [x for x in ("gh", "cloudflared") if not shutil.which(x)]
        if missing:
            raise ValueError("Faltan herramientas: " + ", ".join(missing))
        auth = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, timeout=20)
        if auth.returncode:
            raise ValueError("GitHub CLI no está autenticado. Ejecuta gh auth login.")
        with LOCK:
            STATE["running"] = True
            STATE["transcript_data"] = None
            STATE["status"] = "Preparando transcripción remota. No se ha iniciado el render."
        threading.Thread(
            target=worker, args=("transcribe", title, composition_id, audio, mime),
            daemon=True
        ).start()
        self.send_json(200, {"ok": True})

    def start_render(self):
        data = self.read_json()
        sample_id = str(data.get("sample_id", ""))
        edited = str(data.get("transcript_text", "")).strip()
        with LOCK:
            valid = bool(sample_id and sample_id == STATE["preview_id"] and STATE["audio"])
            running = STATE["running"]
            original = STATE["transcript_data"]
            title, audio, mime, composition_id = STATE["title"], STATE["audio"], STATE["audio_mime"], STATE["composition_id"]
        if not valid:
            raise ValueError("La muestra de audio ya no está disponible.")
        if running:
            raise ValueError("Ya hay un proceso activo.")
        if original is None:
            raise ValueError("Primero debes transcribir y revisar el audio.")
        if not edited or len(edited) > 12000:
            raise ValueError("La transcripción está vacía o supera 12.000 caracteres.")
        duration = max((x["end"] for x in flatten_transcript(original)), default=55.0) + .2
        aligned = align_edited_text(edited, original, duration)
        transcript_json = json_bytes(aligned)
        if len(transcript_json) > 50000:
            raise ValueError("La transcripción corregida es demasiado grande.")
        auth = subprocess.run(["gh", "auth", "status"], capture_output=True, text=True, timeout=20)
        if auth.returncode:
            raise ValueError("GitHub CLI no está autenticado. Ejecuta gh auth login.")
        with LOCK:
            STATE["running"] = True
            STATE["status"] = "Transcripción confirmada. Iniciando el render del diseño manual."
        threading.Thread(
            target=worker,
            args=("render", title, composition_id, audio, mime, transcript_json),
            daemon=True
        ).start()
        self.send_json(200, {"ok": True})

def main():
    if not HTML_FILE.is_file():
        raise SystemExit("No se encontró web/manual.html.")
    sync_result = sync_manual_catalog(force=True)
    print("Sincronización: " + sync_result)
    server = ThreadingHTTPServer((HOST, PORT), ManualHandler)
    url = f"http://{HOST}:{server.server_address[1]}"
    print("cloudservicegm · Diseños manuales en " + url)
    print("Esta modalidad usa un proceso y puerto independientes.")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando Diseños manuales...")
    finally:
        server.shutdown()
        server.server_close()

if __name__ == "__main__":
    main()
