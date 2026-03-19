"""
DESAFIO 4 (Extra) - Sistema de Segurança Remoto com Flask
==========================================================
Aplicação web em Flask que captura frames de uma câmera (local ou IP),
realiza detecção de movimento com bounding box e transmite o resultado
via HTTP como um stream MJPEG.

Uso:
    python app.py [--source <0|rtsp://...|http://...>] [--port <porta>]

Acesse no navegador:
    http://localhost:5000/           → Interface web
    http://localhost:5000/video_feed → Stream MJPEG direto

Exemplos de fonte de vídeo:
    0                            – webcam local padrão
    1                            – segunda webcam
    rtsp://usuario:senha@ip/cam  – câmera IP via RTSP
    http://ip:porta/video        – câmera IP via HTTP
"""

import argparse
import os
import threading
import time

import cv2
import numpy as np
from flask import Flask, Response, render_template_string

# ---------------------------------------------------------------------------
# Configurações padrão
# ---------------------------------------------------------------------------
DEFAULT_SOURCE = 0          # 0 = webcam local
DEFAULT_PORT = 5000
MIN_CONTOUR_AREA = 500      # px² mínimos para considerar como movimento real

# ---------------------------------------------------------------------------
# Template HTML embutido (sem dependência de arquivos externos)
# ---------------------------------------------------------------------------
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Segurança – Detecção de Movimento</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #1a1a2e;
            color: #eee;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        h1 { color: #00d4ff; }
        img {
            border: 3px solid #00d4ff;
            border-radius: 8px;
            max-width: 90vw;
        }
        .info {
            margin-top: 12px;
            font-size: 0.9em;
            color: #aaa;
        }
    </style>
</head>
<body>
    <h1>🎥 Detecção de Movimento em Tempo Real</h1>
    <img src="/video_feed" alt="Stream de vídeo">
    <p class="info">
        Pressione <kbd>Ctrl+C</kbd> no terminal para encerrar o servidor.
    </p>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# Captura e processamento de vídeo
# ---------------------------------------------------------------------------

class VideoStream:
    """
    Captura frames de uma câmera em thread separada, aplica subtração de
    fundo e retorna os frames com bounding boxes desenhados.
    """

    def __init__(self, source=DEFAULT_SOURCE):
        self.source = source
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise RuntimeError(f"Não foi possível abrir a fonte de vídeo: {source!r}")

        self.fgbg = cv2.createBackgroundSubtractorKNN(
            history=500, dist2Threshold=400.0, detectShadows=False
        )
        self.kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

        self._frame = None
        self._lock = threading.Lock()
        self._stop_event = threading.Event()

        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()

    # ------------------------------------------------------------------
    def _capture_loop(self):
        while not self._stop_event.is_set():
            ret, frame = self.cap.read()
            if not ret:
                # Câmera desconectada ou fim do arquivo – tenta reconectar
                time.sleep(0.5)
                self.cap.release()
                self.cap = cv2.VideoCapture(self.source)
                continue

            processed = self._process(frame)
            with self._lock:
                self._frame = processed

    # ------------------------------------------------------------------
    def _process(self, frame: np.ndarray) -> np.ndarray:
        """Aplica subtração de fundo e desenha bounding boxes."""
        fgmask = self.fgbg.apply(frame)

        _, fgmask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, self.kernel)
        fgmask = cv2.dilate(fgmask, self.kernel, iterations=3)

        contornos, _ = cv2.findContours(
            fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        resultado = frame.copy()
        for c in contornos:
            if cv2.contourArea(c) < MIN_CONTOUR_AREA:
                continue
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(resultado, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return resultado

    # ------------------------------------------------------------------
    def get_frame(self):
        """Retorna o frame mais recente como bytes JPEG."""
        with self._lock:
            if self._frame is None:
                return None
            _, buffer = cv2.imencode(".jpg", self._frame)
            return buffer.tobytes()

    # ------------------------------------------------------------------
    def stop(self):
        self._stop_event.set()
        self.cap.release()


# ---------------------------------------------------------------------------
# Aplicação Flask
# ---------------------------------------------------------------------------
app = Flask(__name__)
video_stream: VideoStream = None  # inicializado em main()


@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route("/video_feed")
def video_feed():
    """Endpoint MJPEG – transmite frames processados continuamente."""
    def generate():
        while True:
            frame_bytes = video_stream.get_frame()
            if frame_bytes is None:
                time.sleep(0.05)
                continue
            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n"
                + frame_bytes
                + b"\r\n"
            )
            time.sleep(0.033)  # ~30 fps

    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


# ---------------------------------------------------------------------------
# Ponto de entrada
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sistema de segurança remoto com Flask e detecção de movimento"
    )
    parser.add_argument(
        "--source", default=str(DEFAULT_SOURCE),
        help=(
            "Fonte de vídeo: 0 (webcam local), índice de câmera, "
            "URL RTSP ou HTTP de câmera IP (padrão: 0)"
        ),
    )
    parser.add_argument(
        "--port", type=int, default=DEFAULT_PORT,
        help=f"Porta do servidor Flask (padrão: {DEFAULT_PORT})"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Converte source para inteiro se for um dígito (índice de câmera)
    source = int(args.source) if args.source.isdigit() else args.source

    print(f"Iniciando stream da fonte: {source!r}")
    print(f"Acesse: http://localhost:{args.port}/")

    video_stream = VideoStream(source=source)

    try:
        app.run(host="0.0.0.0", port=args.port, debug=False, threaded=True)
    finally:
        video_stream.stop()
