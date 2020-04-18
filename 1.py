9# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 15:56:20 2020

@author: Marcelo Claro

Criar dois subplots no matplotlib, uma é a webcam a outra um retângulo com a cor dominante
Utilizar o FuncAnimation para animar o gráfico no matplot, atualizando o mesmo a cada 200 ms
Utilizar o K-means Clustering do OpenCV para obter os parâmetros RGB da cor dominante ou utilizar o unique_count_app()
Criar um retângulo com as cores RGB da cor dominante.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


# https://stackoverflow.com/a/44604435/7690982
def grab_frame(cap):
    ret, frame = cap.read()
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def atualizar(i):
    img = grab_frame(captura)
    im1.set_data(img)
    im2.set_data(retangulo(img))


def close(event):
    if event.key == 'q':
        plt.close(event.canvas.figure)


# https://stackoverflow.com/q/50899692/7690982
def unique_count_app(a):
    colors, count = np.unique(a.reshape(-1, a.shape[-1]), axis=0, return_counts=True)
    return colors[count.argmax()]


def retangulo(img):
    r, g, b = contar_kmeans(img)
    h, w, c = img.shape
    rect = np.zeros((h, w, 3), np.uint8)
    rect[0:h, 0:w] = (r, g, b)
    return rect


# https://stackoverflow.com/a/50900494/7690982
def contar_kmeans(img):
    data = np.reshape(img, (-1, 3))
    data = np.float32(data)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    compactness, labels, centers = cv2.kmeans(data, 1, None, criteria, 10, flags)
    return centers[0]


# Inicialização
captura = cv2.VideoCapture(1)
imagem = grab_frame(captura)

# Cria os dois subplots
ax1 = plt.subplot(1, 2, 1)
ax2 = plt.subplot(1, 2, 2)
plt.subplot(222)

# Cria duas imagens nos subplots
im1 = ax1.imshow(imagem)
im2 = ax2.imshow(retangulo(imagem))

# Animação e atualização
ani = FuncAnimation(plt.gcf(), atualizar, interval=200)

# Fechar
cid = plt.gcf().canvas.mpl_connect("key_press_event", close)
plt.title('CORES DO SOLO')
plt.show()
