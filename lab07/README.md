# Lab07 – Tracking de Objetos e Movimento

> **Objetivos da aula**
> - Entender o conceito de Background Subtraction
> - Praticar tracking de objetos em movimento com OpenCV
> - Implementar detecção de movimento com bounding boxes
> - (Extra) Construir um sistema de vigilância remoto com Flask

---

## Índice

1. [Instalação e Dependências](#instalação-e-dependências)
2. [Conceito: Background Subtraction](#conceito-background-subtraction)
3. [Desafio 1 – Subtração de Imagens Estáticas](#desafio-1--subtração-de-imagens-estáticas)
4. [Desafio 2 – Background Subtraction em Vídeos](#desafio-2--background-subtraction-em-vídeos)
5. [Desafio 3 – Detecção de Movimento com Bounding Box](#desafio-3--detecção-de-movimento-com-bounding-box)
6. [Desafio 4 (Extra) – Sistema de Segurança com Flask](#desafio-4-extra--sistema-de-segurança-com-flask)
7. [Estrutura de Arquivos](#estrutura-de-arquivos)
8. [Referências](#referências)

---

## Instalação e Dependências

```bash
# Crie e ative um ambiente virtual (recomendado)
python -m venv .venv
source .venv/bin/activate      # Linux / macOS
.venv\Scripts\activate         # Windows

# Instale as dependências
pip install -r requirements.txt
```

**`requirements.txt`** (incluído nesta pasta):

```
opencv-python>=4.8.0
numpy>=1.24.0
matplotlib>=3.7.0
flask>=3.0.0
requests>=2.31.0
```

---

## Conceito: Background Subtraction

### O que é?

**Background Subtraction** (subtração de fundo) é uma técnica de visão computacional que separa os objetos em **primeiro plano** (*foreground*) do **fundo estático** (*background*) de uma imagem ou vídeo.

### Intuição

```
Frame atual  -  Modelo de fundo  =  Máscara de primeiro plano
```

Se um pixel muda significativamente em relação ao modelo de fundo → ele pertence ao primeiro plano (objeto em movimento).

### Caso simples (imagens estáticas)

Quando temos uma imagem de referência do fundo (sala vazia), basta calcular a diferença absoluta:

```python
diff = cv2.absdiff(fundo, frame_atual)
```

### Caso complexo (vídeos sem imagem de referência)

Sem uma imagem de referência, o modelo de fundo precisa ser estimado estatisticamente, quadro a quadro. O OpenCV oferece dois algoritmos:

| Algoritmo | Função OpenCV | Descrição |
|-----------|---------------|-----------|
| **MOG2** | `cv2.createBackgroundSubtractorMOG2()` | Mistura de Gaussianas adaptativa |
| **KNN**  | `cv2.createBackgroundSubtractorKNN()`  | K-Nearest Neighbor no espaço de cor |

### Parâmetros importantes

| Parâmetro | Tipo | Efeito |
|-----------|------|--------|
| `history` | int | Nº de frames usados no modelo. Menor → adapta mais rápido ao fundo |
| `dist2Threshold` | float | Limiar de distância para classificar pixel como frente/fundo. Menor → mais sensível |
| `detectShadows` | bool | `True` → sombras aparecem em cinza (valor 127) na máscara |

---

## Desafio 1 – Subtração de Imagens Estáticas

> Implementar subtração entre duas imagens para detectar movimento.

**Arquivo:** `desafio1_background_subtraction.py`

### Passo a passo

```python
import cv2
import numpy as np

# 1. Carregar imagens
fundo = cv2.imread('lab_images/sala2.jpg')
teste = cv2.imread('lab_images/sala3.jpg')

# 2. Converter para escala de cinza
gray_fundo = cv2.cvtColor(fundo, cv2.COLOR_BGR2GRAY)
gray_teste  = cv2.cvtColor(teste,  cv2.COLOR_BGR2GRAY)

# 3. Diferença absoluta
diff = cv2.absdiff(gray_fundo, gray_teste)

# 4. Limiarização → máscara binária
_, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)

# 5. Operações morfológicas para reduzir ruído
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN,   kernel)  # remove pontos
thresh = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)  # une regiões
```

### Executar

```bash
python desafio1_background_subtraction.py
# Resultado salvo em: sala_res.png
```

### Funções OpenCV utilizadas

| Função | Descrição |
|--------|-----------|
| `cv2.absdiff(a, b)` | Diferença absoluta pixel a pixel |
| `cv2.threshold(src, thresh, maxval, type)` | Limiarização |
| `cv2.morphologyEx(src, op, kernel)` | Operação morfológica |
| `cv2.getStructuringElement(shape, ksize)` | Cria elemento estruturante |

---

## Desafio 2 – Background Subtraction em Vídeos

> Aplicar subtração de fundo em vídeo com os algoritmos MOG2 e KNN.

**Arquivo:** `desafio2_video_bg_subtraction.py`

### Passo a passo

```python
import cv2

cap = cv2.VideoCapture('lab_images/people-walking.mp4')

# Escolha o algoritmo:
fgbg = cv2.createBackgroundSubtractorKNN()   # KNN
# fgbg = cv2.createBackgroundSubtractorMOG2() # MOG2

while True:
    ret, frame = cap.read()
    if not ret:
        break

    fgmask = fgbg.apply(frame)   # aplica o subtrator

    cv2.imshow('Frame Original', frame)
    cv2.imshow('Máscara FG',     fgmask)

    if cv2.waitKey(30) & 0xFF == 27:  # ESC para sair
        break

cap.release()
cv2.destroyAllWindows()
```

> ⚠️ **Execute pelo terminal**, não pelo Jupyter Notebook, para evitar problemas de delay com janelas do OpenCV.

### Executar

```bash
# Com KNN (padrão)
python desafio2_video_bg_subtraction.py

# Com MOG2
python desafio2_video_bg_subtraction.py --metodo MOG2

# Ajustando parâmetros
python desafio2_video_bg_subtraction.py --history 200 --dist2threshold 100 --no-shadows
```

### Comparação MOG2 vs KNN

| Característica | MOG2 | KNN |
|----------------|------|-----|
| Base matemática | Mistura de Gaussianas | K vizinhos mais próximos |
| Velocidade | Rápido | Ligeiramente mais lento |
| Robustez a ruído | Alta | Alta |
| Adaptação a mudanças | Boa | Boa |
| Parâmetro principal | `varThreshold` | `dist2Threshold` |

---

## Desafio 3 – Detecção de Movimento com Bounding Box

> Detectar o movimento de pessoas e marcar cada região com um retângulo.

**Arquivo:** `desafio3_motion_bounding_box.py`

### Passo a passo

```python
import cv2

cap  = cv2.VideoCapture('lab_images/people-walking.mp4')
fgbg = cv2.createBackgroundSubtractorKNN(detectShadows=False)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. Subtração de fundo
    fgmask = fgbg.apply(frame)

    # 2. Binarização (remove valor 127 das sombras)
    _, fgmask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)

    # 3. Remover ruído
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN,   kernel)
    fgmask = cv2.dilate(fgmask, kernel, iterations=3)

    # 4. Encontrar contornos
    contornos, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)

    # 5. Desenhar bounding box em cada contorno válido
    for c in contornos:
        if cv2.contourArea(c) < 500:   # filtra ruído residual
            continue
        x, y, w, h = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('Detecção', frame)
    cv2.imshow('Máscara',  fgmask)

    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
```

### Executar

```bash
python desafio3_motion_bounding_box.py

# Ajustar área mínima (padrão: 500 px²)
python desafio3_motion_bounding_box.py --min-area 1000
```

### Funções OpenCV utilizadas

| Função | Descrição |
|--------|-----------|
| `cv2.findContours(img, mode, method)` | Encontra contornos na máscara binária |
| `cv2.contourArea(contorno)` | Calcula área de um contorno |
| `cv2.boundingRect(contorno)` | Retorna `(x, y, w, h)` do bounding box |
| `cv2.rectangle(img, pt1, pt2, color, thickness)` | Desenha retângulo |

---

## Desafio 4 (Extra) – Sistema de Segurança com Flask

> Transmitir o vídeo processado (com bounding boxes) via HTTP usando Flask.

**Arquivo:** `desafio4_flask_stream/app.py`

### Arquitetura

```
Câmera (local ou IP)
        │
        ▼
  VideoStream (thread)
    ├─ BackgroundSubtractorKNN
    ├─ Operações morfológicas
    └─ Desenho de bounding boxes
        │
        ▼
  Flask Server (porta 5000)
    ├─ GET /           → Interface HTML
    └─ GET /video_feed → Stream MJPEG
        │
        ▼
  Navegador Web (qualquer dispositivo na rede)
```

### Passo a passo

```python
from flask import Flask, Response
import cv2, threading, time

app = Flask(__name__)

def generate():
    """Gerador de frames MJPEG."""
    cap  = cv2.VideoCapture(0)       # 0 = webcam local
    fgbg = cv2.createBackgroundSubtractorKNN(detectShadows=False)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Processamento (igual ao Desafio 3)
        fgmask = fgbg.apply(frame)
        _, fgmask = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        fgmask = cv2.dilate(fgmask, kernel, iterations=3)
        contornos, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        for c in contornos:
            if cv2.contourArea(c) < 500:
                continue
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Codifica como JPEG e envia
        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n'
               + buffer.tobytes() + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Executar

```bash
cd desafio4_flask_stream

# Webcam local
python app.py

# Câmera IP via RTSP
python app.py --source rtsp://usuario:senha@192.168.1.100/stream

# Porta personalizada
python app.py --port 8080
```

Acesse no navegador: **http://localhost:5000/**

---

## Estrutura de Arquivos

```
lab07/
├── requirements.txt                        # Dependências Python
├── README.md                               # Este arquivo
├── desafio1_background_subtraction.py      # Desafio 1 – imagens estáticas
├── desafio2_video_bg_subtraction.py        # Desafio 2 – MOG2 / KNN em vídeo
├── desafio3_motion_bounding_box.py         # Desafio 3 – bounding boxes
└── desafio4_flask_stream/
    └── app.py                              # Desafio 4 – servidor Flask MJPEG
```

> **Pasta `lab_images/`** (criada automaticamente ao rodar o Desafio 1):
> - `sala2.jpg`, `sala3.jpg` – imagens de sala para subtração estática
> - `people-walking.mp4` – vídeo de pessoas andando para os Desafios 2 e 3

---

## Referências

- [OpenCV – Background Subtraction](https://docs.opencv.org/master/de/de1/group__video__motion.html)
- [OpenCV – Contour Features](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_contours/py_contour_features/py_contour_features.html)
- [Flask – Streaming Video](https://flask.palletsprojects.com/en/3.0.x/patterns/streaming/)
- [Repositório de referência – videostream Flask](https://github.com/arnaldojr/videostream)
- [Cognitivecomputing – Material PDI](https://github.com/arnaldojr/cognitivecomputing)
