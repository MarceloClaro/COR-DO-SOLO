import streamlit as st
import pandas as pd
import numpy as np
import cv2
import colorsys
from sklearn.cluster import KMeans

# Função para converter uma cor RGB para a notação de cor Munsell
def rgb_to_munsell(center):
    r, g, b = center[0], center[1], center[2]
    
    # Converter cor RGB para espaço de cor HLS
    h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
    
    # Multiplicar h por 360 para obter o ângulo na escala HSL
    h = h * 360
    
    # Verificar em qual faixa de ângulo o h se encontra e atribuir a tonalidade correspondente
    if h < 20:
        hue = "vermelho R"
    elif h < 40:
        hue = "amarelo vermelho YR"
    elif h < 75:
        hue = "amarelo Y"
    elif h < 155:
        hue = "amarelo verde GY"
    elif h < 190:
        hue = "verde G"
    elif h < 260:
        hue = "verde azul BG" 
    elif h < 290:
        hue = "azul B"
    elif h < 335:
        hue = "azul roxo PB"
    else:
        hue = "roxo P"
    
    # Verificar em qual faixa o l se encontra e atribuir o valor correspondente
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
    
    # Verificar em qual faixa o s se encontra e atribuir o croma correspondente
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
    
    # Retornar a notação de cor Munsell
    return f"{hue} {value}/{chroma}"

# Função para classificar as cores de uma imagem de solo
def classificar_cor_solo(img, largura, altura, k):
    # Redimensionar imagem
    img = cv2.resize(img, (largura, altura))
    
    # Converter imagem para o espaço de cor HSV
   

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Aplicar agrupamento K-Means à imagem
    kmeans = KMeans(n_clusters=k, random_state=0).fit(img.reshape((largura * altura, 3)))

    labels = kmeans.labels_
    
    # Criar dicionário para armazenar as cores e a quantidade de pixels de cada cor
    cores = {}
    
    # Loop pelos clusters
    for i in range(k):
        # Obter o centro do cluster
        center = kmeans.cluster_centers_[i]
        
        # Converter o centro do cluster para a notação de cor Munsell
        munsell = rgb_to_munsell(center)
        
        # Adicionar cor e quantidade de pixels ao dicionário
        cores[munsell] = (labels == i).sum()
    
    # Retornar dicionário de cores e quantidades de pixels
    return cores

st.title("CLASSIFICADOR DE COR DE SOLO - MUNSELL")
st.write("Prof. Marcelo Claro. - (88)981587145 / marceloclaro@geomaker.org")

st.write("Solo é a camada mais superficial da Terra, composta principalmente de rochas e minerais fragmentados, matéria orgânica, água e ar. A cor do solo é um importante indicador de suas características físisicas e químicas, pois reflete a presença de diferentes componentes e nutrientes. O estudo da cor do solo é importante em diversas áreas, como agricultura, geologia e meio ambiente.")
st.write("Para classificar as cores do solo, utilizamos o sistema de cores Munsell. O sistema de cores Munsell é um método padronizado para descrever cores baseado em três fatores: tonalidade (matiz), valor (brilho) e croma (saturação). Esses três fatores são combinados em uma notação que indica a cor específica, por exemplo, '5Y 7/4' significa uma cor de tonalidade amarela, valor 7 e croma 4.")
st.write("Neste aplicativo, você pode carregar uma imagem de solo e visualizar as cores dominantes na imagem. Escolha o número de cores dominantes (clusters) para o agrupamento da imagem .")
    
def main():
    uploaded_file = st.file_uploader("Escolha a imagem de solo:", type="jpg")

    # Se o usuário tiver carregado uma imagem
    if image is not None:
        st.image(image, width=600)
    else:
        st.write("No image available.")

    if uploaded_file is not None:
        # Converta o arquivo em uma imagem opencv.
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), cv2.IMREAD_COLOR)

        # Obter largura e altura da imagem redimensionada pelo usuário
        largura = st.sidebar.slider("Largura da imagem (em pixels):", min_value=1, max_value=5000, value=1000)
        altura = st.sidebar.slider("Altura da imagem (em pixels):", min_value=1, max_value=5000, value=1000)
        k = st.slider("Número de clusters (cores dominantes):", min_value=1, max_value=20, value=5)

        
        margem_erro = st.sidebar.number_input("Margem de erro para classificação da cor de Munsell (em %):", 0, 50, 10)
        
        
        

           # Mostrar a imagem na tela
    st.image(image, width=600)

    # Chamada da função para classificar as cores da imagem
    cores = classificar_cor_solo(image, largura, altura, k)

    # Exibir gráfico de barras com as cores dominantes na imagem
    st.write("As cores de Munsell dominantes na imagem são:")
    df = pd.DataFrame(list(cores.items()), columns=['Cor de Munsell', 'Porcentagem de pixels'])
    df['Porcentagem de pixels'] = df['Porcentagem de pixels'] / df['Porcentagem de pixels'].sum()
    st.bar_chart(df)

    # Exibir gráfico de barras com as cores classificadas pelo sistema Munsell
    munsell_labels = []
    munsell_values = []
    for munsell, contagem in cores.items():
        munsell_labels.append(munsell)
        contagem = 0
        munsell_values.append(contagem / total_pixels)
    st.bar_chart(munsell_values, munsell_labels)



if __name__ == "__main__":
    main()
