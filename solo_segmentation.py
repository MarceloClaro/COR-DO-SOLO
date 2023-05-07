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
    # ...
}

# Streamlit interface
st.title("Classificação de cores de solo com base na notação Munsell")

uploaded_file = st.file_uploader("Selecione uma imagem de solo", type=["jpg", "jpeg", "png"])
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem de solo carregada", use_column_width=True)
    resized_image = image.resize((50, 50), Image.ANTIALIAS)
    image_array = np.array(resized_image)
    image_array = image_array.reshape((image_array.shape[0] * image_array.shape[1], 3))

    cluster_method = st.selectbox("Escolha o método de clusterização:", ("K-Means", "Fuzzy C-Means"))
    n_clusters = st.slider("Selecione o número de clusters:", 1, 10, 5)
    if st.button("Classificar cores"):
if st.button("Classificar cores"):
    if cluster_method == "K-Means":
        kmeans = KMeans(n_clusters=n_clusters)
        kmeans.fit(image_array)
        cluster_centers = kmeans.cluster_centers_
        labels = kmeans.labels_
    elif cluster_method == "Fuzzy C-Means":
        cntr, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
            image_array.T, n_clusters, 2, error=0.005, maxiter=1000, init=None
        )
        labels = np.argmax(u, axis=0)
        cluster_centers = cntr

    munsell_colors = convert_cluster_centers_to_munsell(cluster_centers)

    display_munsell_colors(munsell_colors)

    segmented_image = create_segmented_image(image_array, labels, cluster_centers)
    st.image(segmented_image, caption="Imagem de solo segmentada", use_column_width=True)




