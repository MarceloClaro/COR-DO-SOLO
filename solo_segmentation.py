import streamlit as st
import numpy as np
from PIL import Image
import colorsys
from sklearn.cluster import KMeans
from fcmeans import FCM
from skimage.color import rgb2lab

# Função para converter cores RGB em notação Munsell conforme a classificação de cores de solo da Embrapa
def rgb_to_embrapa_munsell(r, g, b):
    hue, value, chroma = colorsys.rgb_to_hvc(r / 255, g / 255, b / 255)

    if value < 2:
        munsell_value = "2.5"
    elif value < 4:
        munsell_value = "3.5"
    elif value < 6:
        munsell_value = "4.5"
    elif value < 8:
        munsell_value = "5.5"
    elif value < 9.5:
        munsell_value = "6.5"
    else:
        munsell_value = "7.5"

    if chroma < 1:
        munsell_chroma = "1"
    elif chroma < 2:
        munsell_chroma = "2"
    elif chroma < 3:
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
    elif hue < 340:
        munsell_hue ="2.5B"
    elif hue < 360:
        munsell_hue = "5B"
    embrapa_munsell = f"{munsell_hue} {munsell_value}/{munsell_chroma}"
return embrapa_munsell
def calculate_error_and_std_deviation(Z, center):
    error = np.linalg.norm(Z - center, axis=1)
    return np.mean(error), np.std(error)

def create_segmented_image(image_array, labels, cluster_centers):
    segmented_image_array = cluster_centers[labels]
    return segmented_image_array.reshape(image_array.shape)

def convert_cluster_centers_to_munsell(cluster_centers):
    munsell_colors = [rgb_to_embrapa_munsell(*center) for center in cluster_centers]
    return munsell_colors

def display_munsell_colors(munsell_colors):
    st.subheader("Cores Munsell:")
    st.write('\n'.join(munsell_colors))
def main():
    st.title("Classificação de cores de solo com base na notação Munsell")

    uploaded_file = st.file_uploader("Selecione uma imagem de solo", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagem de solo carregada", use_column_width=True)
        resized_image = image.resize((50, 50), Image.ANTIALIAS)
        image_array = np.array(resized_image).reshape((-1, 3))

        cluster_method = st.selectbox("Escolha o método de clusterização:", ("K-Means", "Fuzzy C-Means"))
        n_clusters = st.slider("Selecione o número de clusters:", 1, 10, 5)

        if st.button("Classificar cores"):
            if cluster_method == "K-Means":
                kmeans = KMeans(n_clusters=n_clusters)
                kmeans.fit(image_array)
                labels = kmeans.labels_
                cluster_centers = kmeans.cluster_centers_
            elif cluster_method == "Fuzzy C-Means":
                fcm = FCM(n_clusters=n_clusters)
                fcm.fit(image_array)
                labels = fcm.predict(image_array)
                cluster_centers = fcm.centers

            munsell_colors = convert_cluster_centers_to_munsell(cluster_centers)
            display_munsell_colors(munsell_colors)

            segmented_image = create_segmented_image(image_array, labels, cluster_centers)
            segmented_image = segmented_image.reshape(resized_image.size + (3,))
            segmented_image = Image.fromarray((segmented_image * 255).astype(np.uint8))
            st.image(segmented_image, caption="Imagem de solo segmentada", use_column_width=True)

if __name__ == "__main__":
    main()
    
