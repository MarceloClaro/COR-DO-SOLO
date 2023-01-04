import streamlit as st
import colorsys
from sklearn.cluster import KMeans
from PIL import Image
import numpy as np

def rgb_to_munsell(r, g, b):
    """Converte uma cor RGB para o sistema de cores Munsell.
    
    Parâmetros:
    r (int): Valor de vermelho (0-255).
    g (int): Valor de verde (0-255).
    b (int): Valor de azul (0-255).
    
    Retorno:
    str: Cor no sistema de cores Munsell.
    """
    h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
    h = h*360
    
    hue_map = {
        (0, 20): 'R',
        (20, 40): 'YR',
        (40, 75): 'Y',
        (75, 155): 'GY',
        (155, 190): 'G',
        (190, 260): 'GY',
        (260, 290): 'G',
        (290, 335): 'BG',
        (335, 360): 'B',
    }
    for hue_range, hue_name in hue_map.items():
        if hue_range[0] <= h < hue_range[1]:
            hue = hue_name
            break
    
    value_map = {
        (0, 0.25): '2.5',
        (0.25, 0.3): '3',
        (0.3, 0.4): '4',
        (0.4, 0.5): '5',
        (0.5, 0.6): '6',
        (0.6, 0.7): '7',
        (0.7, 0.8): '8',
        (0.8, 1): '10',
    }
    for value_range, value_name in value_map.items():
        if value_range[0] <= l < value_range[1]:
            value = value_name
            break
    
    chroma_map = {
        (0, 0.2): '0.5',
        (0.2, 0.4): '1',
        (0.4, 0.6): '2',
        (0.6, 0.8): '3',
        (0.8, 1): '4',
    }
    for chroma_range, chroma_name in chroma_map.items():
        if chroma_range[0] <= s < chroma_range[1]:
            chroma = chroma_name
            break
    
    return f"{hue} {value}/{chroma}"

def classificar_cor_solo(img, largura, altura, k):
    """Classifica as cores dominantes de uma imagem de solo.
    
    Parâmetros:
    img (PIL.Image): Imagem a ser classificada.
    largura (int): Largura da imagem redimensionada.
    altura (int): Altura da imagem redimensionada.
    k (int): Número de clusters a serem gerados pelo algoritmo K-Means.
    
    Retorno:
    dict: Porcentagem de pixels de cada cor classificada.
    """
    # Redimensionar imagem
    img = img.resize((largura, altura))
    img = np.array(img)
    # Aplicar k-means para segmentação da imagem
    kmeans = KMeans(n_clusters=k, random_state=0).fit(img.reshape(-1,3))
    # Obter as cores dominantes
    cores = kmeans.cluster_centers_.astype(int)
    # Convertê-las para o sistema de cores Munsell
    cores_munsell = [rgb_to_munsell(cor[0], cor[1], cor[2]) for cor in cores]
    # Contar a quantidade de pixels de cada cor
    color_counts = {}
    for i in range(k):
        color_counts[cores_munsell[i]] = len(np.where(kmeans.labels_ == i)[0])
    # Calcular as porcentagens de cada cor
    total_pixels = sum(color_counts.values())
    color_percentages = {color: count / total_pixels * 100 for color, count in color_counts.items()}
    return color_percentages

def main():
    st.title('Classificação da Cor do Solo')
    st.subheader('Carta de cor de solo Munsell')
    
    menu = st.sidebar.selectbox('Selecione uma opção', ['O que é solo?', 'O que é Carta de classificação de cor de Munsell e porque a cor do solo é importante?', 'Como proceder e analisar cor de solo, segundo a Embrapa', 'Classificação da Cor do Solo'])
    if menu == 'Classificação da Cor do Solo':
        st.markdown('Selecione uma imagem de solo para classificar as cores dominantes:')
        img_file = st.file_uploader('', type=['jpg', 'jpeg', 'png'])
        if img_file is not None:
            with Image.open(img_file) as img:
                largura = st.sidebar.slider('Largura da imagem redimensionada', 100, 1000, 500, 100)
                altura = st.sidebar.slider('Altura da imagem redimensionada', 100, 1000, 500, 100)
                k = st.sidebar.slider('Número de clusters', 2, 20, 10, 1)
                color_percentages = classificar_cor_solo(img, largura, altura, k)
                st.markdown(f'Cores dominantes na imagem:')
                for color, percentage in color_percentages.items():
                    st.markdown(f'{color}: {percentage:.2f}%')
if __name__ == '__main__':
    main()
