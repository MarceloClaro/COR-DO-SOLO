import streamlit as st
import numpy as np
import cv2
from PIL import Image
import colorsys
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from fcmeans import FCM
from skimage.color import rgb2lab, deltaE_ciede2000

# Função para converter cores RGB em notação Munsell conforme a classificação de cores de solo da Embrapa
def rgb_to_embrapa_munsell(r, g, b):
    # Converter de RGB para HLS
    hue, lightness, saturation = colorsys.rgb_to_hls(r/255, g/255, b/255)
    hue = hue * 360
    lightness = lightness * 100
    saturation = saturation * 100

    # Aproximar a notação Munsell com base na tabela da Embrapa
    if lightness < 2:
        munsell_value = "2.5"
    elif lightness < 4:
        munsell_value = "3.5"
    elif lightness < 6:
        munsell_value = "4.5"
    elif lightness < 8:
        munsell_value = "5.5"
    elif lightness < 9.5:
        munsell_value = "6.5"
    else:
        munsell_value = "7.5"
        
    if saturation < 1:
        munsell_chroma = "1"
    elif saturation < 2:
        munsell_chroma = "2"
    elif saturation < 3:
        munsell_chroma = "3"
    else:
        munsell_chroma = "4"
        
    if hue < 2:
        munsell_hue = "10R"
    elif hue < 4:
        munsell_hue = "2.5YR"
    elif hue < 7:
        munsell_hue = "5YR"
    elif hue < 10:
        munsell_hue = "7.5YR"
    elif hue < 15:
        munsell_hue = "10YR"
    elif hue < 22:
        munsell_hue = "2.5Y"
    elif hue < 28:
        munsell_hue = "5Y"
    elif hue < 33:
        munsell_hue = "7.5Y"
    elif hue < 39:
        munsell_hue = "10Y"
    elif hue < 45:
        munsell_hue = "2.5GY"
    elif hue < 60:
        munsell_hue = "5GY"
    elif hue < 80:
        munsell_hue = "7.5GY"
    elif hue < 100:
        munsell_hue = "10GY"
    elif hue < 130:
        munsell_hue = "2.5G"
    elif hue < 170:
        munsell_hue = "5G"
    elif hue < 200:
        munsell_hue = "7.5G"
    elif hue < 220:
        munsell_hue = "10G"
    elif hue < 240:
        munsell_hue = "2.5BG"
    elif hue < 270:
        munsell_hue = "5BG"
    elif hue < 290:
        munsell_hue = "7.5BG"
    elif hue < 310:
                munsell_hue = "10BG"
    elif hue < 330:
        munsell_hue = "2.5B"
    elif hue < 350:
        munsell_hue = "5B"
    elif hue < 370:
        munsell_hue = "7.5B"
    elif hue < 390:
        munsell_hue = "10B"
    elif hue < 410:
        munsell_hue = "2.5PB"
    elif hue < 430:
        munsell_hue = "5PB"
    elif hue < 450:
        munsell_hue = "7.5PB"
    elif hue < 470:
        munsell_hue = "10PB"
    else:
        munsell_hue = "10P"

    return f"{munsell_hue} {munsell_value}/{munsell_chroma}"

# Função para carregar e exibir a imagem
def load_image(image_file):
    img = Image.open(image_file)
    img = np.array(img)
    st.image(img, caption='Imagem carregada', use_column_width=True)
    return img

st.title("Classificador de Cores de Solo Embrapa")
uploaded_file = st.file_uploader("Escolha uma imagem de solo", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    img = load_image(uploaded_file)

    # Pré-processamento da imagem
    img_resized = cv2.resize(img, (100, 100), interpolation=cv2.INTER_AREA)
    img_reshaped = img_resized.reshape(img_resized.shape[0] * img_resized.shape[1], img_resized.shape[2])

    # Agrupamento de cores usando K-means
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(img_reshaped)
    colors = kmeans.cluster_centers_

    # Agrupamento de cores usando FCM
    fcm = FCM(n_clusters=5)
    fcm.fit(img_reshaped)
    fcm_colors = fcm.centers_

    # Conversão das cores para Munsell e exibição
    st.header("Cores Munsell usando K-means")
    for idx, color in enumerate(colors):
        rgb_color = tuple(map(int, color))
        munsell_color = rgb_to_embrapa_munsell(*rgb_color)
        st.write(f"Cor {idx + 1}: {munsell_color}")
        st.write(f"Cor correspondente em RGB: {rgb_color}")

    st.header("Cores Munsell usando FCM")
    for idx, color in enumerate(fcm_colors):
        rgb_color = tuple(map(int, color))
        munsell_color = rgb_to_embrapa_munsell(*rgb_color)
        st.write(f"Cor {idx + 1}: {munsell_color}")
        st.write(f"Cor correspondente em RGB: {rgb_color}")

