import streamlit as st
import colorsys
from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

HUE_MAP = [
    ('R', (0, 20)),
    ('YR', (20, 40)),
    ('Y', (40, 75)),
    ('GY', (75, 155)),
    ('G', (155, 190)),
    ('GY', (190, 260)),
    ('G', (260, 290)),
    ('BG', (290, 335)),
    ('B', (335, 360)),
]

VALUE_MAP = [
    ('2.5', (0, 0.25)),
    ('3', (0.25, 0.3)),
    ('4', (0.3, 0.4)),
    ('5', (0.4, 0.5)),
    ('6', (0.5, 0.6)),
    ('7', (0.6, 0.7)),
    ('8', (0.7, 0.8)),
    ('10', (0.8, 1)),
]

CHROMA_MAP = [
    ('0.5', (0, 0.2)),
    ('1', (0.2, 0.4)),
    ('2', (0.4, 0.6)),
    ('3', (0.6, 0.8)),
    ('4', (0.8, 1)),
]

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
    
    for hue_name, hue_range in HUE_MAP:
        if hue_range[0] <= h < hue_range[1]:
            hue = hue_name
            break
    
    for value_name, value_range in VALUE_MAP:
        if value_range[0] <= l < value_range[1]:
            value = value_name
            break
    
    for chroma_name, chroma_range in CHROMA_MAP:
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
    cores, contagem = np.unique(kmeans.labels_, return_counts=True)
    cores_dominantes = {}
    for cor, count in zip(cores, contagem):
        r, g, b = kmeans.cluster_centers_[cor]
        munsell = rgb_to_munsell(int(r), int(g), int(b))
        cores_dominantes[munsell] = count / len(kmeans.labels_)
    return cores_dominantes

def calcular_margem_erro(pixels, cores):
    """Calcula a margem de erro entre os pixels da imagem e os pixels de cada cor classificada.
    
    Parâmetros:
    pixels (int): Número total de pixels da imagem.
    cores (dict): Porcentagem de pixels de cada cor classificada.
    
    Retorno:
    dict: Margem de erro de cada cor classificada.
    """
    margem_erro = {}
    for cor, porcentagem in cores.items():
        margem_erro[cor] = abs(pixels - porcentagem) / pixels
    return margem_erro

def imprimir_cor_dominante(cores):
    """Imprime a cor dominante da imagem.
    
    Parâmetros:
    cores (dict): Porcentagem de pixels de cada cor classificada.
    """
    cor_dominante = max(cores, key=cores.get)
    print(f"A cor dominante da imagem é {cor_dominante}")

def imprimir_grafico_margem_erro(margem_erro):
    """Imprime um gráfico de barras com a margem de erro de cada cor classificada.
    
    Parâmetros:
    margem_erro (dict): Margem de erro de cada cor classificada.
    """
    plt.bar(margem_erro.keys(), margem_erro.values())
    plt.xlabel('Cores')
    plt.ylabel('Margem de erro')
    plt.title('Margem de erro por cor')
    plt.show()

def imprimir_grafico_pizza(cores):
    """Imprime um gráfico de pizza com a porcentagem de pixels de cada cor classificada.
    
    Parâmetros:
    cores (dict): Porcentagem de pixels de cada cor classificada.
    """
    labels = cores.keys()
    sizes = cores.values()
    plt.pie(sizes, labels=labels)
    plt.title('Porcentagem de pixels por cor')
    plt.show()

if name == "main":
    main()
