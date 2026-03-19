"""
DESAFIO 2 - Background Subtraction em Vídeos
=============================================
Aplica subtração de fundo em um arquivo de vídeo usando os algoritmos
BackgroundSubtractorMOG2 e BackgroundSubtractorKNN do OpenCV.

Execute este script diretamente pelo terminal (não via Jupyter Notebook)
para evitar problemas de delay com janelas do OpenCV:

    python desafio2_video_bg_subtraction.py [--video <caminho>] [--metodo <MOG2|KNN>]

Parâmetros exploráveis:
    history          – Nº de frames para construir o modelo estatístico
                       do fundo. Quanto menor, mais rápido mas menos estável.
    dist2Threshold   – Limiar para decidir se um pixel pertence ao fundo.
                       Quanto menor, mais sensível à variação.
    detectShadows    – Se True, sombras aparecem em cinza na máscara.

Tecla ESC → sair
"""

import argparse
import os
import sys

import cv2
import numpy as np


def criar_subtrator(metodo: str = "KNN", history: int = 500,
                    dist2Threshold: float = 400.0,
                    detectShadows: bool = True):
    """
    Cria e retorna um objeto subtrator de fundo.

    Parâmetros
    ----------
    metodo : str
        'MOG2' ou 'KNN'
    history : int
        Número de frames usados para construir o modelo estatístico.
    dist2Threshold : float
        Limiar de distância quadrática para classificar um pixel como primeiro
        plano (KNN) ou desvio padrão acumulado (MOG2).
    detectShadows : bool
        Quando True, sombras são marcadas em cinza (valor 127) na máscara.

    Retorna
    -------
    Subtrator OpenCV configurado.
    """
    metodo = metodo.upper()
    if metodo == "MOG2":
        return cv2.createBackgroundSubtractorMOG2(
            history=history,
            varThreshold=dist2Threshold,
            detectShadows=detectShadows,
        )
    if metodo == "KNN":
        return cv2.createBackgroundSubtractorKNN(
            history=history,
            dist2Threshold=dist2Threshold,
            detectShadows=detectShadows,
        )
    raise ValueError(f"Método desconhecido: {metodo!r}. Use 'MOG2' ou 'KNN'.")


def processar_video(video_path: str, metodo: str = "KNN",
                    history: int = 500, dist2Threshold: float = 400.0,
                    detectShadows: bool = True) -> None:
    """
    Abre o vídeo, aplica o subtrator de fundo frame a frame e exibe o
    resultado em duas janelas lado a lado:
        • 'Frame Original' – vídeo sem processamento
        • 'Máscara FG'     – máscara de primeiro plano gerada pelo subtrator

    Pressione ESC para encerrar.
    """
    if not os.path.isfile(video_path):
        sys.exit(f"[ERRO] Arquivo de vídeo não encontrado: {video_path}")

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        sys.exit(f"[ERRO] Não foi possível abrir o vídeo: {video_path}")

    fgbg = criar_subtrator(metodo, history, dist2Threshold, detectShadows)

    print(f"Processando '{video_path}' com o método {metodo}...")
    print("Pressione ESC para sair.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fim do vídeo.")
            break

        fgmask = fgbg.apply(frame)

        cv2.imshow("Frame Original", frame)
        cv2.imshow("Máscara FG", fgmask)

        # ESC → encerra
        if cv2.waitKey(30) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Subtração de fundo em vídeo (MOG2 ou KNN)"
    )
    parser.add_argument(
        "--video", default=os.path.join("lab_images", "people-walking.mp4"),
        help="Caminho para o arquivo de vídeo (padrão: lab_images/people-walking.mp4)"
    )
    parser.add_argument(
        "--metodo", default="KNN", choices=["MOG2", "KNN"],
        help="Algoritmo de subtração de fundo: MOG2 ou KNN (padrão: KNN)"
    )
    parser.add_argument(
        "--history", type=int, default=500,
        help="Nº de frames para o modelo estatístico do fundo (padrão: 500)"
    )
    parser.add_argument(
        "--dist2threshold", type=float, default=400.0,
        help="Limiar de distância para classificação fundo/frente (padrão: 400)"
    )
    parser.add_argument(
        "--no-shadows", action="store_true",
        help="Desativa a detecção de sombras"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    processar_video(
        video_path=args.video,
        metodo=args.metodo,
        history=args.history,
        dist2Threshold=args.dist2threshold,
        detectShadows=not args.no_shadows,
    )
