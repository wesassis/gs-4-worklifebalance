"""
DESAFIO 1 - Background Subtraction em imagens estáticas
========================================================
Detecta movimento comparando duas imagens estáticas: uma imagem de fundo
(referência) e uma imagem de teste. A diferença absoluta realça os objetos
que se moveram ou apareceram entre as duas capturas.

Uso:
    python desafio1_background_subtraction.py

Imagens de entrada sugeridas (pasta lab_images/):
    sala.jpg  →  imagem de fundo (sala vazia)
    sala2.jpg →  imagem de teste  (sala com pessoas/objetos)
    sala3.jpg →  imagem de teste  (sala com pessoas/objetos)
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt


def download_lab_images(laboratorio: str = "lab07", diretorio: str = "lab_images") -> None:
    """Faz o download das imagens do laboratório a partir do repositório remoto."""
    import os
    import requests

    api_url = "https://api.github.com/repos/arnaldojr/cognitivecomputing/contents/material/aulas/PDI/"
    url_completa = api_url + laboratorio
    print(f"Fazendo o download de: {url_completa}")

    response = requests.get(url_completa, timeout=10)
    if response.status_code != 200:
        raise RuntimeError(f"Erro ao acessar o repositório: {response.status_code}")

    os.makedirs(diretorio, exist_ok=True)

    for file in response.json():
        file_name = file["name"]
        if file_name.endswith((".png", ".jpg", ".jpeg", ".mp4")):
            file_url = file["download_url"]
            destination = os.path.join(diretorio, file_name)
            r = requests.get(file_url, stream=True, timeout=30)
            if r.status_code == 200:
                with open(destination, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Baixado: {destination}")
            else:
                print(f"Erro ao baixar {file_url}")

    print(f"Download concluído. Arquivos salvos na pasta {diretorio}.")


def background_subtraction(img_fundo_path: str, img_teste_path: str) -> np.ndarray:
    """
    Subtrai a imagem de teste da imagem de fundo (referência) para detectar
    movimento.

    Parâmetros
    ----------
    img_fundo_path : str
        Caminho para a imagem de fundo (sala vazia).
    img_teste_path : str
        Caminho para a imagem de teste (sala com movimento).

    Retorna
    -------
    np.ndarray
        Máscara binária com as regiões de movimento destacadas.
    """
    img_fundo = cv2.imread(img_fundo_path)
    img_teste = cv2.imread(img_teste_path)

    if img_fundo is None:
        raise FileNotFoundError(f"Imagem de fundo não encontrada: {img_fundo_path}")
    if img_teste is None:
        raise FileNotFoundError(f"Imagem de teste não encontrada: {img_teste_path}")

    # Redimensiona para o mesmo tamanho caso necessário
    if img_fundo.shape != img_teste.shape:
        img_teste = cv2.resize(img_teste, (img_fundo.shape[1], img_fundo.shape[0]))

    # Converte para escala de cinza
    gray_fundo = cv2.cvtColor(img_fundo, cv2.COLOR_BGR2GRAY)
    gray_teste = cv2.cvtColor(img_teste, cv2.COLOR_BGR2GRAY)

    # Diferença absoluta entre os dois frames
    diff = cv2.absdiff(gray_fundo, gray_teste)

    # Limiarização para obter máscara binária
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

    # Operações morfológicas para reduzir ruído
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)   # remove pequenos pontos
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel) # une regiões próximas

    return thresh, diff, img_fundo, img_teste


def exibir_resultados(img_fundo, img_teste, diff, mascara) -> None:
    """Exibe as imagens de entrada, diferença e máscara lado a lado."""
    plt.figure(figsize=(16, 4))

    plt.subplot(1, 4, 1)
    plt.title("Fundo (Referência)")
    plt.imshow(cv2.cvtColor(img_fundo, cv2.COLOR_BGR2RGB))
    plt.axis("off")

    plt.subplot(1, 4, 2)
    plt.title("Imagem de Teste")
    plt.imshow(cv2.cvtColor(img_teste, cv2.COLOR_BGR2RGB))
    plt.axis("off")

    plt.subplot(1, 4, 3)
    plt.title("Diferença Absoluta")
    plt.imshow(diff, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 4, 4)
    plt.title("Máscara (Movimento)")
    plt.imshow(mascara, cmap="gray")
    plt.axis("off")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    import os

    diretorio = "lab_images"

    # Faz o download caso as imagens ainda não existam
    if not os.path.isdir(diretorio):
        download_lab_images(diretorio=diretorio)

    # Caminhos das imagens de entrada
    img_fundo_path = os.path.join(diretorio, "sala2.jpg")
    img_teste_path = os.path.join(diretorio, "sala3.jpg")

    mascara, diff, img_fundo, img_teste = background_subtraction(img_fundo_path, img_teste_path)

    print("Subtração concluída.")
    print(f"Pixels de movimento detectados: {cv2.countNonZero(mascara)}")

    exibir_resultados(img_fundo, img_teste, diff, mascara)

    # Salva o resultado
    cv2.imwrite("sala_res.png", mascara)
    print("Resultado salvo em sala_res.png")
