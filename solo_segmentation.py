import streamlit as st
import numpy as np
import cv2
from PIL import Image
import colorsys
import matplotlib.pyplot as plt

# Função para converter cores RGB em notação Munsell conforme a classificação de cores de solo da Embrapa
def rgb_to_embrapa_munsell(r, g, b):
    hue, lightness, saturation = colorsys.rgb_to_hls(r/255, g/255, b/255)
    hue = hue * 360
    lightness = lightness * 100
    saturation = saturation * 100

    # Aproximar a notação Munsell com base na tabela da Embrapa
    if lightness < 10:
        munsell_value = "2.5"
    elif lightness < 30:
        munsell_value = "3.5"
    elif lightness < 50:
        munsell_value = "4.5"
    elif lightness < 70:
        munsell_value = "5.5"
    elif lightness < 85:
        munsell_value = "6.5"
    else:
        munsell_value = "7.5"

    if saturation < 5:
        munsell_chroma = "1"
    elif saturation < 15:
        munsell_chroma = "2"
    elif saturation < 30:
        munsell_chroma = "3"
    else:
        munsell_chroma = "4"

    if hue < 20:
        munsell_hue = "10R"
    elif hue < 50:
        munsell_hue = "7.5YR"
    elif hue < 70:
        munsell_hue = "5YR"
    elif hue < 150:
        munsell_hue = "2.5YR"
    elif hue < 250:
        munsell_hue = "10YR"
    else:
        munsell_hue = "10R"

    embrapa_munsell = f"{munsell_hue} {munsell_value}/{munsell_chroma}"
    return embrapa_munsell

# Função para calcular a margem de erro e o desvio padrão da clusterização
def calculate_error_and_std_deviation(Z, center):
    error = np.linalg.norm(Z - center, axis=1)
    mean_error = np.mean(error)
    std_deviation = np.std(error)
    return mean_error, std_deviation

# Dicionário e lógica de classificação do solo
soil_dict = {
    "7.5YR4/2": {
        "sistema_munsell": "7.5YR4/2",
        "solo_embrapa": "Solonetz Solodizado",
        "descricao": "Solos com alto teor de sódio, baixa permeabilidade e drenagem restrita.",
        "caracteristicas": "Textura argilosa, baixa fertilidade natural e alta suscetibilidade à compactação.",
        "vegetacao_tipica": "Cerrado",
        "cultivos_manejo": "Uso limitado para agricultura. Recomenda-se a adoção de práticas conservacionistas e correção da salinidade."
    },
    "5YR5/3": {
        "sistema_munsell": "5YR5/3",
        "solo_embrapa": "Plintossolo Háplico",
        "descricao": "Solos com presença de camadas de plintita, que dificultam a infiltração de água.",
        "caracteristicas": "Textura argilosa, baixa fertilidade natural e alta capacidade de retenção de água.",
        "vegetacao_tipica": "Cerrado",
        "cultivos_manejo": "Uso limitado para agricultura. Recomenda-se a adoção de práticas conservacionistas e manejo adequado da camada de plintita."
    },
    "10R 5/3": {
        "sistema_munsell": "10R 5/3",
        "solo_embrapa": "Plintossolo Háplico",
        "descricao": "Solos com presença de camadas de plintita, que dificultam a infiltração de água.",
        "caracteristicas": "Textura argilosa, baixa fertilidade natural e alta capacidade de retenção de água.",
        "vegetacao_tipica": "Cerrado",
        "cultivos_manejo": "Uso limitado para agricultura. Recomenda-se a adoção de práticas conservacionistas e manejo adequado da camada de plintita."
    },
    "7R/0": {
        "sistema_munsell": "7R/0",
        "solo_embrapa": "Solonetz Solodizado",
        "descricao": "Solos de coloração avermelhada a arroxeada, profundos e bem drenados.",
        "caracteristicas": "Textura argilosa, alta fertilidade natural e alta capacidade de retenção de água.",
        "vegetacao_tipica": "Mata Atlântica e Floresta Amazônica",
        "cultivos_manejo": "Adequado para culturas perenes e anuais. Recomenda-se o uso de práticas conservacionistas e adubação equilibrada."
    },
    "10YR8/6": {
        "sistema_munsell": "10YR8/6",
        "solo_embrapa": "Argissolo Amarelo",
        "descricao": "Solos com coloração amarela, profundos e bem drenados.",
        "caracteristicas": "Textura média ou argilosa, boa fertilidade natural e alta capacidade de retenção de água.",
        "vegetacao_tipica": "Cerrado",
        "cultivos_manejo": "Adequado para culturas perenes e anuais. Recomenda-se o uso de práticas conservacionistas e adubação equilibrada."
    },
    "2.5YR 3/3": {
        "sistema_munsell": "2.5YR 3/3",
        "solo_embrapa": "Vertissolo Háplico Eutrófico",
        "descricao": "Solos com presença de argila expansiva, formando fissuras quando secos.",
        "caracteristicas": "Textura argilosa, alta fertilidade natural e alta capacidade de retenção de água.",
        "vegetacao_tipica": "Cerrado e Caatinga",
        "cultivos_manejo": "Pode ser cultivado com culturas anuais e perenes, desde que sejam adotadas práticas conservacionistas e adubação adequada."
    },
    "5YR6/2": {
        "sistema_munsell": "5YR6/2",
        "solo_embrapa": "Argissolo Vermelho-Amarelo Eutrófico",
        "descricao": "Solos com coloração vermelho-amarela, profundos e bem drenados.",
        "caracteristicas": "Textura média ou argilosa, boa fertilidade natural e alta capacidade de retenção de água.",
        "vegetacao_tipica": "Cerrado",
        "cultivos_manejo": "Adequado para culturas perenes e anuais. Recomenda-se o uso de práticas conservacionistas e adubação equilibrada."
    },
    "7.5YR4/3": {
        "sistema_munsell": "7.5YR4/3",
        "solo_embrapa": "Argissolo Vermelho-Amarelo",
        "descricao": "Solos com coloração vermelho-amarela, profundos e bem drenados.",
        "caracteristicas": "Textura média ou argilosa, boa fertilidade natural e alta capacidade de retenção de água.",
        "vegetacao_tipica": "Cerrado",
        "cultivos_manejo": "Adequado para culturas perenes e anuais. Recomenda-se o uso de práticas conservacionistas e adubação equilibrada."
    },
    "10YR6/6": {
        "sistema_munsell": "10YR6/6",
        "solo_embrapa": "Argissolo Amarelo",
        "descricao": "Solos com coloração amarela, profundos e bem drenados.",
        "caracteristicas": "Textura média ou argilosa, boa fertilidade natural e alta capacidade de retenção de água.",
        "vegetacao_tipica": "Cerrado",
        "cultivos_manejo": "Adequado para culturas perenes e anuais. Recomenda-se o uso de práticas conservacionistas e adubação equilibrada."
    }
}

# Carregar e exibir a imagem
st.title("Classificação de Solo")
uploaded_file = st.file_uploader("Escolha a imagem", type="jpg")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagem', use_column_width=True)
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Redimensionar a imagem para uma lista de pixels
    Z = img.reshape((-1,3))
    Z = np.float32(Z)

    # Definir os critérios, número de clusters(K) e aplicar k-means()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 1
    ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)

    # Calcular a margem de erro e o desvio padrão da clusterização
    mean_error, std_deviation = calculate_error_and_std_deviation(Z, center)

    # Converter a imagem para valores de 8 bits
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))

    # Exibir a imagem e a notação Munsell correspondente
    fig, ax = plt.subplots()
    ax.imshow(res2)
    ax.set_title(rgb_to_embrapa_munsell(center[0][0], center[0][1], center[0][2]))
    ax.axis('off')
    st.pyplot(fig)

    embrapa_notation = rgb_to_embrapa_munsell(center[0][0], center[0][1], center[0][2])
    soil_type = soil_dict.get(embrapa_notation, "NÃO CADASTRADO")

    st.write("Tipo de solo correspondente:")
    st.write(soil_type)
    st.write("Margem de erro da clusterização: {:.2f}".format(mean_error))
    st.write("Desvio padrão da clusterização: {:.2f}".format(std_deviation))
