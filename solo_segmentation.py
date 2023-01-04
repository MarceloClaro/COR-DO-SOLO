import streamlit as st
import colorsys
from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
# Mapa de tonalidades do sistema de cores Munsell
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
# Mapa de valores do sistema de cores Munsell
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
#Mapa de cromas do sistema de cores Munsell
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
    kmeans = KMeans(n_clusters=k, random_state=0).fit(img.reshape((largura * altura, 3)))
    labels = kmeans.labels_
    # Contar número de pixels de cada cor
    cores = {}
    for i in range(k):
        # Converter os valores RGB dos centroides para o sistema de cores Munsell
        r, g, b = kmeans.cluster_centers_[i]
        cor = rgb_to_munsell(int(r*255), int(g*255), int(b*255))
        # Contar número de pixels de cada cor
        cores[cor] = sum(labels == i)
    # Calcular porcentagem de pixels de cada cor
    pixels = largura * altura
    for cor, quantidade in cores.items():
        cores[cor] = quantidade / pixels * 100
    return cores

def plotar_cores(cores):
    """Plota um gráfico de barras com a porcentagem de pixels de cada cor classificada.
    
    Parâmetros:
    cores (dict): Porcentagem de pixels de cada cor classificada.
    """
    plt.bar(cores.keys(), cores.values())
    plt.xlabel('Cores')
    plt.ylabel('Porcentagem de pixels')
    plt.title('Porcentagem de pixels por cor')
    plt.show()

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
        margem     erro[cor] = abs(pixels - porcentagem) / pixels
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

st.title("Classificação de Cor do Solo")
st.subheader("Sistema de Munsell")

st.markdown("""
O que é Solo?

O solo é uma camada fina da crosta terrestre composta por minerais, matéria orgânica decomposta, água e ar. Ele é importante para a produção de alimentos, manutenção da biodiversidade e como um importante reservatório de nutrientes.

Qual a importância da cor do solo?

A cor do solo pode fornecer informações importantes sobre suas características físicas, químicas e biológicas. Por exemplo, a cor pode indicar o teor de matéria orgânica, pH, fertilidade e capacidade de retenção de água. Além disso, a cor do solo pode ser utilizada como um indicador da qualidade do solo em áreas agrícolas e florestais.
""")

# Lê imagem
img = Image.open('solo.jpg')
st.image(img, width=300)

# Classifica as cores dominantes da imagem
# Obtém os parâmetros de classificação da imagem
largura = st.sidebar.slider("Largura da imagem redimensionada", 100, 1000, 500)
altura = st.sidebar.slider("Altura da imagem redimensionada", 100, 1000, 500)
k = st.sidebar.slider("Número de clusters (cores) a serem gerados pelo algoritmo K-Means", 2, 20, 5)

cores = classificar_cor_solo(img, largura, altura, k)

# Plota o gráfico de barras com a porcentagem de pixels de cada cor classificada
plotar_cores(cores)

# Calcula a margem de erro entre os pixels da imagem e os pixels de cada cor classificada
margem_erro = calcular_margem_erro(largura * altura, cores)

# Imprime a cor dominante da imagem
imprimir_cor_dominante(cores)

# Imprime o gráfico de barras com a margem de erro de cada cor classificada
imprimir_grafico_margem_erro(margem_erro)

# Imprime o gráfico de pizza com a porcentagem de pixels de cada cor classificada
imprimir_grafico_pizza(cores)

