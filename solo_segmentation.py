import streamlit as st
import numpy as np
import cv2
from PIL import Image
import colorsys
import matplotlib.pyplot as plt

# Função para converter RGB em notação Munsell
def rgb_to_munsell(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
    h = h*360
    hue = ""
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
    value = ""
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
    chroma = ""
    if s < 0.1:
        chroma = "0"
    elif s < 0.2:
        chroma = "1"
    elif s < 0.3:
        chroma = "2"
    elif s < 0.4:
        chroma = "3"
    elif s < 0.5:
        chroma = "4"
    elif s < 0.6:
        chroma = "5"
    elif s < 0.7:
        chroma = "6"
    elif s < 0.8:
        chroma = "7"
    elif s < 0.9:
        chroma = "8"
    elif s < 1.0:
        chroma = "9"
    else:
        chroma = "0"

    return value + hue + "/" + chroma

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

        # Converter a imagem para valores de 8 bits
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))

    # Exibir a imagem e a notação Munsell correspondente
    fig, ax = plt.subplots()
    ax.imshow(res2)
    ax.set_title(rgb_to_munsell(center[0][0], center[0][1], center[0][2]))
    ax.axis('off')
    st.pyplot(fig)

    soil_dict = {
    "7.5YR5/4": {
        "sistema_munsell": "7.5YR5/4",
        "solo_embrapa": "Argissolo Vermelho-Amarelo",
        "descricao": "Solos com coloração vermelho-amarela, profundos e bem drenados.",
        "caracteristicas": "Textura média ou argilosa, boa fertilidade natural e alta capacidade de retenção de água.",
        "vegetacao_tipica": "Cerrado, Caatinga e Mata Atlântica",
        "cultivos_manejo": "Adequado para culturas perenes e anuais. Recomenda-se o uso de práticas conservacionistas e adubação equilibrada."
    },
    "10YR3/3": {
        "sistema_munsell": "10YR3/3",
        "solo_embrapa": "Neossolo Regolítico",
        "descricao": "Solos pouco desenvolvidos, geralmente rasos e localizados em áreas com relevo acentuado.",
        "caracteristicas": "Baixa fertilidade natural, baixa capacidade de retenção de água e alta susceptibilidade à erosão.",
        "vegetacao_tipica": "Caatinga e Cerrado",
        "cultivos_manejo": "Uso limitado para agricultura. Preferencialmente, deve ser preservado para conservação ambiental e recarga de aquíferos."
    },
    "2.5YR5/4": {
        "sistema_munsell": "2.5YR5/4",
        "solo_embrapa": "Cambissolo Háplico",
        "descricao": "Solos de coloração avermelhada, geralmente pouco profundos e com horizonte B incipiente.",
        "caracteristicas": "Textura média, fertilidade natural moderada e moderada capacidade de retenção de água.",
        "vegetacao_tipica": "Cerrado, Mata Atlântica e Floresta Amazônica",
        "cultivos_manejo": "Pode ser cultivado com culturas anuais e perenes, desde que sejam adotadas práticas conservacionistas e adubação adequada."
    },
    "7R/0": {
        "sistema_munsell": "7R/0",
        "solo_embrapa": "Luvissolo Crômico",
        "descricao": "Solos de coloração avermelhada a arroxeada, profundos e bem drenados.",
        "caracteristicas": "Textura argilosa, alta fertilidade natural e alta capacidade de retenção de água.",
        "vegetacao_tipica": "Mata Atlântica e Floresta Amazônica",
        "cultivos_manejo": "Adequado para culturas perenes e anuais. Recomenda-se o uso de práticas conservacionistas e adubação equilibrada."
    }
}


    munsell_notation = rgb_to_munsell(center[0][0], center[0][1], center[0][2])
    soil_type = soil_dict.get(munsell_notation, "NÃO CADASTRADO")

    st.write("Tipo de solo correspondente:")
    st.write(soil_type)
