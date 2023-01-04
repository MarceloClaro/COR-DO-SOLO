import streamlit as st
import pandas as pd
import numpy as np
import cv2
import colorsys
from sklearn.cluster import KMeans

def rgb_to_munsell(center):
r, g, b = center[0], center[1], center[2]
h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
h = h * 360
if h < 20:
hue = "R"
elif h < 40:
hue = "YR"
elif h < 75:
hue = "Y"
elif h < 155:
hue = "GY"
elif h < 190:
hue = "G"
elif h < 260:
hue = "BG"
elif h < 290:
hue = "B"
elif h < 335:
hue = "PB"
else:
hue = "P"
if l < 0.25:
value = "2.5"
elif l < 0.3:
value = "3"
elif l < 0.4:
value = "4"
elif l < 0.5:
value = "5"
elif l < 0.6:
value = "6"
elif l < 0.7:
value = "7"
elif l < 0.8:
value = "8"
else:
value = "10"
if s < 0.2:
chroma = "0.5"
elif s < 0.4:
chroma = "1"
elif s < 0.6:
chroma = "2"
elif s < 0.8:
chroma = "3"
else:
chroma = "4"
return f"{hue} {value}/{chroma}"

def classificar_cor_solo(img, largura, altura, k):
img = cv2.resize(img, (largura, altura))
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
kmeans = KMeans(n_clusters=k, random_state=0).fit(img.reshape((largura * altura, 3)))
labels = kmeans.labels_
cores = {}
for i in range(k):
center = kmeans.cluster_centers_[i]
munsell = rgb_to_munsell(center)
cores[munsell] = (labels == i).sum()
return cores

def main():
st.title("Classificador de cor de solo")
# LER IMAGEM
image = cv2.imread("image.jpg")
largura = st.sidebar.number_input("Largura (pixels)", value=500, min_value=100, max_value=1000, step=100)
altura = st.sidebar.number_input("Altura (pixels)", value=500
, min_value=100, max_value=1000, step=100)

MOSTRAR IMAGEM
st.image(image, width=600)

NÚMERO DE CLUSTERS
k = st.sidebar.number_input("Número de clusters", value=2, min_value=2, max_value=10, step=1)

CLASSIFICAR CORES
cores = classificar_cor_solo(image, largura, altura, k)

MOSTRAR CORES
st.header("Cores identificadas:")
for munsell, contagem in cores.items():
st.write(f"{munsell}: {contagem} pixels ({(contagem / (largura * altura)):.2%})")

EXIBIR GRÁFICO DE BARRAS
munsell_labels = []
munsell_values = []
for munsell, contagem in cores.items():
munsell_labels.append(munsell)
munsell_values.append(contagem / (largura * altura))
st.bar_chart(munsell_values, munsell_labels)
