import streamlit as st
import pandas as pd
import numpy as np
import cv2
import colorsys
from sklearn.cluster import KMeans

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
    st.write("Solo é a camada mais superficial da Terra, composta principalmente de rochas e minerais fragmentados, matéria orgânica, água e ar. A cor do solo é um importante indicador de suas características físisicas e químicas, pois reflete a presença de diferentes componentes e nutrientes. O estudo da cor do solo é importante em diversas áreas, como agricultura, geologia e meio ambiente.")
    st.write("Para classificar as cores do solo, utilizamos o sistema de cores Munsell. O sistema de cores Munsell é um método padronizado para descrever cores baseado em três fatores: tonalidade (matiz), valor (brilho) e croma (saturação). Esses três fatores são combinados em uma notação que indica a cor específica, por exemplo, '5Y 7/4' significa uma cor de tonalidade amarela, valor 7 e croma 4.")
    st.write("Neste aplicativo, você pode carregar uma imagem de solo e visualizar as cores dominantes na imagem. Escolha o número de clusters para o agrupamento da imagem e clique em 'Classificar cores' para ver os resultados.")
    uploaded_file = st.file_uploader("Escolha a imagem de solo:", type="jpg")
    if uploaded_file is not None:
    if os.path.exists(uploaded_file):
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
        # rest of your code here
    else:
        st.write("Arquivo não encontrado!")

    if uploaded_file is not None:
        # Convert the file to an opencv image.
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

        largura = st.slider("Largura da imagem redimensionada:", min_value=100, max_value=1000, value=300)
        altura = st.slider("Altura da imagem redimensionada:", min_value=100, max_value=1000, value=300)
        k = st.slider("Número de clusters:", min_value=2, max_value=20, value=5)
        st.write("As cores dominantes na imagem são:")
        cores = classificar_cor_solo(image, largura, altura, k)
        df = pd.DataFrame(list(cores.items()), columns=['Cor', 'Porcentagem de pixels'])
        df['Porcentagem de pixels'] = df['Porcentagem de pixels'] / df['Porcentagem de pixels'].sum()
        if uploaded_file is not None:
            image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)
            largura = st.slider("Largura da imagem redimensionada:", min_value=100, max_value=1000, value=300)
            altura = st.slider("Altura da imagem redimensionada:", min_value=100, max_value=1000, value=300)
            k = st.slider("Número de clusters:", min_value=2, max_value=20, value=5)
            margem_erro = st.sidebar.slider("Margem de erro para classificação de cor (em %):", 0, 50, 10)
            st.write("As cores dominantes na imagem são:")
            cores = classificar_cor_solo(image, largura, altura, k)
            df = pd.DataFrame(list(cores.items()), columns=['Cor', 'Porcentagem de pixels'])
            df['Porcentagem de pixels'] = df['Porcentagem de pixels'] / df['Porcentagem de pixels'].sum()
            st.bar_chart(df)
        if st.sidebar.button("Classificar cores"):
            munsell_labels = []
            munsell_values = []
        for munsell, count in cores.items():
            munsell_labels.append(munsell)
            munsell_values.append(count / total_pixels)
            st.bar_chart(munsell_values, munsell_labels)
if __name__ == "__main__":
    main()



