#APP cor de solo
import streamlit as st
import numpy as np
import cv2
from PIL import Image
import colorsys
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from fcmeans import FCM
from skimage.color import rgb2lab, deltaE_ciede2000
import skimage
from skimage.feature import greycomatrix, greycoprops

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
    elif hue < 260:
        munsell_hue = "5BG"
    elif hue < 280:
        munsell_hue = "7.5BG"
    elif hue < 300:
        munsell_hue = "10BG"
    elif hue < 320:
        munsell_hue = "2.5B"
    elif hue < 340:
        munsell_hue = "5B"
    else:
        munsell_hue = "7.5B"  
        
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
    "10YR4/4": {
        "sistema_munsell": "10YR4/4",
        "solo_embrapa": "Latossolo Vermelho-Amarelo",
        "descricao": "Solos bem desenvolvidos, com horizonte B latossólico e alta saturação por bases.",
        "caracteristicas": "Textura predominantemente argilosa, boa capacidade de retenção de água e boa fertilidade natural.",
        "vegetacao_tipica": "Floresta Amazônica, Mata Atlântica, Cerrado e Caatinga.",
        "cultivos_manejo_recomendado": {
            "recomendados": ["Café", "Citros", "Eucalipto", "Banana"],
            "condicionantes": "Adubação e irrigação podem ser necessárias para maximizar a produtividade.",
            "manejo": "Práticas conservacionistas, como plantio direto, rotação de culturas e uso de cobertura vegetal, são recomendadas para preservar a qualidade do solo."
        }
    },

    "2.5YR5/8": {
        "sistema_munsell": "2.5YR5/8",
        "solo_embrapa": "Latossolo Vermelho",
        "descricao": "Solos profundos, com horizonte B latossólico e alta saturação por bases.",
        "caracteristicas": "Textura predominantemente argilosa, boa capacidade de retenção de água e alta fertilidade natural.",
        "vegetacao_tipica": "Floresta Amazônica, Mata Atlântica e Cerrado.",
        "cultivos_manejo_recomendado": {
            "recomendados": ["Soja", "Milho", "Café", "Cana-de-açúcar"],
            "condicionantes": "Adubação e irrigação podem ser necessárias para maximizar a produtividade.",
            "manejo": "Práticas conservacionistas, como plantio direto, rotação de culturas e uso de cobertura vegetal, são recomendadas para preservar a qualidade do solo."
        }
    }
}


def convert_cluster_centers_to_munsell(cluster_centers):
    munsell_colors = []
    for center in cluster_centers:
        r, g, b = center
        munsell_color = rgb_to_embrapa_munsell(r, g, b)
        munsell_colors.append(munsell_color)
    return munsell_colors


def display_munsell_colors(munsell_colors):
    st.subheader("Cores Munsell:")
    for color in munsell_colors:
        st.write(color)


# Função para criar uma imagem segmentada com base na clusterização
def create_segmented_image(image_array, labels, cluster_centers):
    num_clusters = cluster_centers.shape[0]
    segmented_array = np.zeros_like(image_array)
    for i in range(num_clusters):
        segmented_array[labels == i] = cluster_centers[i]
    segmented_image = segmented_array.reshape((50, 50, 3))
    segmented_image = (segmented_image * 255).astype(np.uint8)
    return segmented_image


def plot_munsell_distribution(munsell_colors):
    unique_colors, counts = np.unique(munsell_colors, return_counts=True)
    plt.bar(unique_colors, counts)
    plt.xlabel("Cores Munsell")
    plt.ylabel("Frequência")
    plt.title("Distribuição das cores Munsell")
    plt.xticks(rotation=45)
    st.pyplot(plt.gcf())
    plt.clf()

def plot_error_distribution(image_array, cluster_centers):
    error = np.linalg.norm(image_array - cluster_centers, axis=1)
    plt.hist(error, bins='auto')
    plt.xlabel("Margem de erro")
    plt.ylabel("Frequência")
    plt.title("Distribuição da margem de erro")
    st.pyplot(plt.gcf())
    plt.clf()

def plot_std_deviation_distribution(image_array, cluster_centers):
    error = np.linalg.norm(image_array - cluster_centers, axis=1)
    std_deviation = np.std(error)
    plt.hist(error, bins='auto', density=True)
    plt.axvline(std_deviation, color='r', linestyle='dashed', linewidth=2)
    plt.xlabel("Desvio padrão")
    plt.ylabel("Frequência")
    plt.title("Distribuição do desvio padrão")
    st.pyplot(plt.gcf())
    plt.clf()

def glcm_features(gray_image, distances=[1], angles=[0, np.pi/4, np.pi/2, 3*np.pi/4], levels=256):
    glcm = greycomatrix(gray_image, distances, angles, levels, symmetric=True, normed=True)
    contrast = greycoprops(glcm, 'contrast')
    dissimilarity = greycoprops(glcm, 'dissimilarity')
    homogeneity = greycoprops(glcm, 'homogeneity')
    asm = greycoprops(glcm, 'ASM')
    energy = greycoprops(glcm, 'energy')
    correlation = greycoprops(glcm, 'correlation')
    
    return contrast, dissimilarity, homogeneity, asm, energy, correlation

# Streamlit interface
def main():
    st.title("Classificação de cores de solo com base na notação Munsell")

    uploaded_file = st.file_uploader("Selecione uma imagem de solo", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagem de solo carregada", use_column_width=True)
        resized_image = image.resize((50, 50), Image.LANCZOS)
        image_array = np.array(resized_image)
        image_array = image_array.reshape((image_array.shape[0] * image_array.shape[1], 3))
        cluster_method = st.selectbox("Escolha o método de clusterização:", ("K-Means", "Fuzzy C-Means"))
        n_clusters = st.slider("Selecione o número de clusters:", 1, 10, 5)

        if st.button("Classificar cores"):
            if cluster_method == "K-Means":
                kmeans = KMeans(n_clusters=num_clusters, n_init=10)
                kmeans.fit(image_array)
                cluster_centers = kmeans.cluster_centers_
                labels = kmeans.labels_
            elif cluster_method == "Fuzzy C-Means":
                fcm = FCM(n_clusters=num_clusters, n_init=10)
                fcm.fit(image_array)
                labels = fcm.predict(image_array)
                cluster_centers = fcm.centers

            munsell_colors = convert_cluster_centers_to_munsell(cluster_centers)
            display_munsell_colors(munsell_colors)

            segmented_image = create_segmented_image(image_array, labels, cluster_centers)
            st.image(segmented_image, caption="Imagem de solo segmentada", use_column_width=True)

            # Exibir margem de erro e desvio padrão
            mean_error, std_deviation = calculate_error_and_std_deviation(image_array, cluster_centers)
            st.subheader("Margem de erro e desvio padrão:")
            st.write(f"Margem de erro: {mean_error}")
            st.write(f"Desvio padrão: {std_deviation}")

            # Exibir informações de classificação do solo
            st.subheader("Classificação do solo:")
            for color in munsell_colors:
                if color in soil_dict:
                    soil_info = soil_dict[color]
                    st.write(f"Cor Munsell: {soil_info['sistema_munsell']}")
                    st.write(f"Solo Embrapa: {soil_info['solo_embrapa']}")
                    st.write(f"Descrição: {soil_info['descricao']}")
                    st.write(f"Características: {soil_info['caracteristicas']}")
                    st.write(f"Vegetação típica: {soil_info['vegetacao_tipica']}")
                    st.write("Cultivos e manejo recomendado:")
                    st.write(f"  - Recomendados: {', '.join(soil_info['cultivos_manejo_recomendado']['recomendados'])}")
                    st.write(f"  - Condicionantes: {soil_info['cultivos_manejo_recomendado']['condicionantes']}")
                    st.write(f"  - Manejo: {soil_info['cultivos_manejo_recomendado']['manejo']}")
                    st.write("\n")
        # Exibir gráficos
        st.subheader("Gráficos:")
        plot_munsell_distribution(munsell_colors)
        plot_error_distribution(image_array, cluster_centers)
        plot_std_deviation_distribution(image_array, cluster_centers)


if __name__ == '__main__':
    main()

# Exibir informações do App
st.subheader("Sobre o aplicativo:")
st.write("""
Este aplicativo utiliza a notação Munsell para classificar as cores do solo. Ele utiliza algoritmos de clusterização, como K-Means e Fuzzy C-Means, para identificar e agrupar cores semelhantes presentes na imagem do solo. Em seguida, ele converte as cores médias dos clusters para a notação Munsell e exibe informações relevantes sobre a classificação do solo, como a descrição, características, vegetação típica e cultivos e manejo recomendado, de acordo com os padrões estabelecidos pela Embrapa.
""")

st.subheader("Como usar:")
st.write("""
1. Faça o upload de uma imagem do solo que você deseja analisar.
2. Selecione o método de clusterização que você deseja usar (K-Means ou Fuzzy C-Means).
3. Selecione o número de clusters que você deseja usar na análise.
4. Clique no botão 'Classificar cores' para iniciar a análise.
5. O aplicativo exibirá a imagem segmentada, a classificação do solo, gráficos e informações adicionais sobre a margem de erro e desvio padrão.
6. Explore os resultados e ajuste as configurações conforme necessário para obter os melhores resultados.
""")

st.subheader("Créditos:")
st.write("""
Este aplicativo foi desenvolvido usando a biblioteca Streamlit para Python e a arquitetura GPT-4 da OpenAI. Agradecimentos especiais à Embrapa pelo fornecimento das informações sobre a classificação de solos e notação Munsell.
""")
st.write("Desenvolvedor: [professor Marcelo Claro]")
st.write("Contato: [marceloclaro@gmail.com]")
st.write("GitHub: [https://github.com/MarceloClaro/COR-DO-SOLO/edit/master/solo_segmentation.py]")

st.subheader("Referências:")
st.write("""
1. Munsell Soil Color Charts. [https://www.munsell.com/color-services/color-standards/soil-color-charts/]
2. Embrapa. Sistema Brasileiro de Classificação de Solos. [https://www.embrapa.br/solos/sistema-brasileiro-de-classificacao-de-solos]
3. Streamlit. [https://www.streamlit.io/]
4. OpenAI. GPT-4. [https://www.openai.com/]
""")
