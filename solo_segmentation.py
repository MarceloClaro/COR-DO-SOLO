import streamlit as st
import pandas as pd
import numpy as np
import cv2
import colorsys
from sklearn.cluster import KMeans

def rgb_to_munsell(center):
    r, g, b = center[0][0], center[0][1], center[0][2]
    h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
    h = h*360
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

@st.cache(allow_output_mutation=True)
def classificar_cor_solo(img, largura, altura, k):
    img = cv2.resize(img, (largura, altura))
    kmeans = KMeans(n_clusters=k, random_state=0).fit(img.reshape((largura * altura, 3)))
    labels = kmeans.labels_
    cores = {}
    for i in range(k):
        center = kmeans.cluster_centers_[i]
        munsell = rgb_to_munsell(center)
        cores[munsell] = (labels == i).sum()
    return cores

def main():
    st.title("CLASSIFICADOR DE COR DE SOLO - MUNSEL")
    st.write("Solo é a camada mais superficial da Terra, composta principalmente de rochas e minerais fragmentados, matéria orgânica, água e ar. A cor do solo é um importante indicador de suas características físicas e químicas, e é utilizada como uma ferramenta importante para o estudo geográfico. A cor do solo pode ser influenciada por diversos fatores, como a presença de matéria orgânica, minerais, humidade e tipo de rocha na qual foi formado. O sistema de cores Munsell é um método padronizado de especificação de cor usado em diversas áreas, incluindo o estudo do solo. Ele divide a cor em três componentes: tonalidade, valor e croma.")
st.write("Selecione uma imagem de solo:")
file = st.file_uploader("", type=["jpg", "png"])
if file is not None:
img = cv2.imread(file)
largura = st.sidebar.number_input("Largura da imagem redimensionada:", min_value=1, max_value=1000, value=300, step=1)
altura = st.sidebar.number_input("Altura da imagem redimensionada:", min_value=1, max_value=1000, value=300, step=1)
k = st.sidebar.number_input("Número de clusters a serem gerados pelo algoritmo K-Means:", min_value=1, max_value=10, value=5, step=1)
cores = classificar_cor_solo(img, largura, altura, k)
st.write("Resultado da classificação das cores dominantes na imagem:")
st.write(cores)

if name == 'main':
main()
