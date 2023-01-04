import streamlit as st
import colorsys
from sklearn.cluster import KMeans
import gc
from PIL import Image
import numpy as np

def rgb_to_munsell(center):
    r,g,b = center[0],center[1],center[2]
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
        hue = "GY"
    elif h < 290:
        hue = "G"
    elif h < 335:
        hue = "BG"
    else:
        hue = "B"
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

def classificar_cor_solo(img_path, largura, altura, k):
    # Carregar imagem e redimensioná-la
    img = Image.open(img_path)
    img = img.resize((largura, altura))
    img = np.array(img)
    # Aplicar k-means para segmentação da imagem
    kmeans = KMeans(n_clusters=k, random_state=0).fit(img.reshape(-1,3))
    # Obter as cores dominantes
    cores = kmeans.cluster_centers_.astype(int)
    # Convertê-las para o sistema de cores Munsell
    cores_munsell = [rgb_to_munsell(cor) for cor in cores]
    # Contar a quantidade de pixels de cada cor
    color_counts = {}
    for i in range(k):
        color_counts[cores_munsell[i]] = len(np.where(kmeans.labels_ == i)[0])
    # Calcular as porcentagens de cada cor
total_pixels = sum(color_counts.values())
color_percentages = {color: count / total_pixels * 100 for color, count in color_counts.items()}
# Liberar espaço na RAM
del img, kmeans, cores, color_counts
gc.collect()
return color_percentages

def main():
st.title('Classificação da Cor do Solo')
st.subheader('Carta de cor de solo Munsell')
menu = st.sidebar.selectbox('Selecione uma opção', ['O que é solo?', 'O que é Carta de classificação de cor de Munsell e porque a cor do solo é importante?', 'Como proceder e analisar cor de solo, segundo a Embrapa', 'Classificação da Cor do Solo'])
se menu == 'Classificação da Cor do Solo':
st.markdown('Selecione uma imagem para classificar a cor do solo.')
img_path = st.file_uploader('Imagem', type='jpg')
se img_path não for Nenhum:
largura = st.number_input('Largura', min_value=1, max_value=1000, valor=500)
altura = st.number_input('Altura', min_value=1, max_value=1000, valor=500)
k = st.number_input('Número de clusters', min_value=1, max_value=20, value=5)
color_percentages = classificar_cor_solo(img_path, largura, altura, k)
st.bar_chart(color_percentages

if __name


