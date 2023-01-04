import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
import colorsys
from sklearn.cluster import KMeans
import gc

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
    # Liberar espaço na RAM
    del img, kmeans, cores
    gc.collect()
    return cores_munsell

def main():
    st.title('Classificação da Cor do Solo')
    st.subheader('Carta de cor de solo Munsell')
    menu = st.sidebar.selectbox('Selecione uma opção', ['O que é solo?', 'O que é Carta de classificação de cor de Munsell e porque a cor do solo é importante?', 'Como proceder e analisar cor de solo, segundo a Embrapa', 'Classificação da Cor do Solo'])
    if menu == 'O que é solo?':
        st.markdown('O solo é a camada superficial da Terra que é formada por minerais, matéria orgânica e organismos vivos. Ele é importante para a produção de alimentos, proteção do solo contra erosão, filtragem de água e preservação da biodiversidade.')
    elif menu == 'O que é Carta de classificação de cor de Munsell e porque a cor do solo é importante?':
        st.markdown('A Carta de classificação de cor de Munsell é um sistema de cores utilizado para descrever a cor do solo de maneira precisa e uniforme. A cor do solo é importante porque pode fornecer informações so...')
        elif menu == 'Classificação da Cor do Solo':
        st.markdown('Selecione a imagem do solo seco ou úmido e ajuste a largura e altura desejadas para o processamento da imagem.')
        img_file = st.file_uploader('Fazer upload da imagem do solo seco ou úmido')
        largura = st.slider('Largura', 100, 1000, 400)
        altura = st.slider('Altura', 100, 1000, 400)
        k = st.number_input('Quantidade de cores dominantes', min_value=1, max_value=10, value=3)
        if img_file is not None:
            cores = classificar_cor_solo(img_file, largura, altura, k)
            st.markdown(f'As cores dominantes encontradas foram: {cores}')

if __name__ == '__main__':
    main()


