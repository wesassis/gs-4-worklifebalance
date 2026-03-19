"""
DESAFIO 3 - Detecção de Movimento com Bounding Box
===================================================
Detecta o movimento das pessoas andando no vídeo e marca cada região de
movimento com um retângulo (bounding box).

Execute diretamente pelo terminal:

    python desafio3_motion_bounding_box.py [--video <caminho>]

Fluxo do algoritmo:
    1. Subtração de fundo com BackgroundSubtractorKNN
    2. Remoção de ruído (abertura morfológica)
    3. Dilatação para unir regiões próximas
    4. Detecção de contornos
    5. Filtragem pelo área mínima do contorno
    6. Desenho do bounding box ao redor de cada contorno válido

Tecla ESC → sair
"""

import argparse
import os
import sys

import cv2
import numpy as np


# Área mínima (em pixels²) para que um contorno seja considerado movimento real
MIN_CONTOUR_AREA = 500


def criar_subtrator_knn(history: int = 500, dist2Threshold: float = 400.0,
                        detectShadows: bool = False):
    """Cria um BackgroundSubtractorKNN."""
    return cv2.createBackgroundSubtractorKNN(
        history=history,
        dist2Threshold=dist2Threshold,
        detectShadows=detectShadows,
    )


def processar_frame(frame: np.ndarray, fgbg, kernel: np.ndarray) -> tuple:
    """
    Aplica subtração de fundo e operações morfológicas em um único frame.

    Retorna
    -------
    mascara_limpa : np.ndarray
        Máscara binária após denoising.
    contornos : list
        Contornos detectados na máscara.
    """
    # Aplica subtrator de fundo
    fgmask = fgbg.apply(frame)

    # Binarização (remove sombras caso detectShadows=True)
    _, fgmask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)

    # Abertura morfológica: remove pequenos pontos de ruído
    mascara_limpa = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)

    # Dilatação: une regiões próximas para formar um único blob por pessoa
    mascara_limpa = cv2.dilate(mascara_limpa, kernel, iterations=3)

    # Detecção de contornos
    contornos, _ = cv2.findContours(
        mascara_limpa, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    return mascara_limpa, contornos


def desenhar_bounding_boxes(frame: np.ndarray, contornos,
                             min_area: int = MIN_CONTOUR_AREA) -> np.ndarray:
    """
    Filtra contornos pela área mínima e desenha um bounding box verde em cada
    região de movimento válida.

    Parâmetros
    ----------
    frame : np.ndarray
        Frame original (BGR) onde os retângulos serão desenhados.
    contornos : list
        Lista de contornos retornada por cv2.findContours.
    min_area : int
        Área mínima (px²) para considerar um contorno como movimento real.

    Retorna
    -------
    np.ndarray
        Frame com os bounding boxes desenhados.
    """
    resultado = frame.copy()
    for contorno in contornos:
        if cv2.contourArea(contorno) < min_area:
            continue
        x, y, w, h = cv2.boundingRect(contorno)
        cv2.rectangle(resultado, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return resultado


def processar_video(video_path: str, min_area: int = MIN_CONTOUR_AREA) -> None:
    """
    Processa o vídeo frame a frame, detecta movimento e exibe bounding boxes.

    Janelas exibidas:
        • 'Frame com BBox' – frame original com retângulos nos objetos em movimento
        • 'Máscara'        – máscara binária após denoising

    Pressione ESC para encerrar.
    """
    if not os.path.isfile(video_path):
        sys.exit(f"[ERRO] Arquivo de vídeo não encontrado: {video_path}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        sys.exit(f"[ERRO] Não foi possível abrir o vídeo: {video_path}")

    # Subtrator sem detecção de sombras (mais rápido e máscara mais limpa)
    fgbg = criar_subtrator_knn(detectShadows=False)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    print(f"Processando '{video_path}'...")
    print("Pressione ESC para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fim do vídeo.")
            break

        mascara, contornos = processar_frame(frame, fgbg, kernel)
        frame_com_bbox = desenhar_bounding_boxes(frame, contornos, min_area)

        cv2.imshow("Frame com BBox", frame_com_bbox)
        cv2.imshow("Máscara", mascara)

        if cv2.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Detecção de movimento com bounding box"
    )
    parser.add_argument(
        "--video", default=os.path.join("lab_images", "people-walking.mp4"),
        help="Caminho para o arquivo de vídeo (padrão: lab_images/people-walking.mp4)"
    )
    parser.add_argument(
        "--min-area", type=int, default=MIN_CONTOUR_AREA,
        help=f"Área mínima (px²) de contorno para desenhar o bounding box "
             f"(padrão: {MIN_CONTOUR_AREA})"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    processar_video(video_path=args.video, min_area=args.min_area)
