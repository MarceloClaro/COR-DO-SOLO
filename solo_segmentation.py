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
    "2.5YR 5/8": {
        "sistema_munsell": "2.5YR 5/8",
        "solo_embrapa": "Latossolo Vermelho",
        "descricao": "Solos profundos, com horizonte B latossólico e alta saturação por bases.",
        "caracteristicas": "Textura predominantemente argilosa, boa capacidade de retenção de água e alta fertilidade natural.",
        "vegetacao_tipica": "Floresta Amazônica, Mata Atlântica e Cerrado.",
        "cultivos_manejo_recomendado": {
            "recomendados": ["Soja", "Milho", "Café", "Cana-de-açúcar"],
            "condicionantes": "Adubação e irrigação podem ser necessárias para maximizar a produtividade.",
            "manejo": "Práticas conservacionistas, como plantio direto, rotação de culturas e uso de cobertura vegetal, são recomendadas para preservar a qualidade do solo."
        },
        "ph": "5.5 - 6.0",
        "condutividade_eletrica": "Baixa",
        "teor_nutrientes": "Alto",
        "manejo_inadequado": {
            "consequencias": ["Erosão", "Perda de nutrientes", "Degradação ambiental"]
        }
    },
    "7.5YR 6/6": {
        "sistema_munsell": "7.5YR 6/6",
        "solo_embrapa": "Argissolo Amarelo",
        "descricao": "Solos com horizonte B textural e média a alta saturação por alumínio.",
        "caracteristicas": "Textura média a argilosa, moderada capacidade de retenção de água e média fertilidade natural.",
        "vegetacao_tipica": "Floresta Amazônica, Mata Atlântica e Cerrado.",
        "cultivos_manejo_recomendado": {
            "recomendados": ["Milho", "Feijão", "Mandioca", "Cana-de-açúcar"],
            "condicionantes": "Calagem e adubação podem ser necessárias para melhorar a fertilidade e reduzir a acidez do solo.",
           "manejo": "Práticas conservacionistas, como plantio direto, rotação de culturas e uso de cobertura vegetal, são recomendadas para preservar a qualidade do solo."
        },
        "ph": "5.5 - 6.0",
        "condutividade_eletrica": "Média",
        "teor_nutrientes": "Médio",
        "manejo_inadequado": {
            "consequencias": ["Compactação do solo", "Baixa produtividade", "Perda de nutrientes"]
        }
    },
    "10YR 3/3": {
        "sistema_munsell": "10YR 3/3",
        "solo_embrapa": "Neossolo Quartzarênico",
        "descricao": "Solos arenosos e pouco desenvolvidos, com baixa saturação por bases.",
        "caracteristicas": "Textura arenosa, baixa capacidade de retenção de água e baixa fertilidade natural.",
        "vegetacao_tipica": "Caatinga e Cerrado.",
        "cultivos_manejo_recomendado": {
            "recomendados": ["Mandioca", "Melancia", "Cenoura"],
            "condicionantes": "Uso de técnicas de conservação de solo e irrigação é essencial para garantir a produtividade.",
            "manejo": "Uso de técnicas de conservação de solo, como cultivo mínimo e rotação de culturas, é recomendado para evitar a degradação do solo."
        },
        "ph": "4.5 - 5.5",
        "condutividade_eletrica": "Alta",
        "teor_nutrientes": "Baixo",
        "manejo_inadequado": {
            "consequencias": ["Desertificação", "Erosão", "Perda de água e nutrientes"]
        }
    }
}

# Função para classificar a cor do solo
def classify_soil_color(image):
    # Conversão da imagem para um array numpy
    image_array = np.array(image)
    
    # Redimensionar a imagem para acelerar o processamento
    resized_image = cv2.resize(image_array, (300, 300), interpolation=cv2.INTER_AREA)
    
    # Converter a imagem para o espaço de cor LAB
    lab_image = rgb2lab(resized_image)
    
    # Extrair os canais L, A e B
    l_channel = lab_image[:, :, 0]
    a_channel = lab_image[:, :, 1]
    b_channel = lab_image[:, :, 2]
    
    # Empilhar os canais A e B
    ab_channels = np.stack((a_channel, b_channel), axis=2)
    
    # Redimensionar o array para 2D
    ab_channels_2d = ab_channels.reshape(ab_channels.shape[0] * ab_channels.shape[1], ab_channels.shape[2])
    
    # Realizar a clusterização utilizando o algoritmo Fuzzy C-means
    fcm = FCM(n_clusters=3)
    fcm.fit(ab_channels_2d)
    fcm_centers = fcm.centers
    
    # Calcular a margem de erro e o desvio padrão da clusterização
    mean_error, std_deviation = calculate_error_and_std_deviation(ab_channels_2d, fcm_centers)
    
    # Identificar o centro que representa a cor do solo
    soil_color_center = fcm_centers[np.argmax(std_deviation)]
    
    # Converter a cor do solo para RGB
    soil_color_rgb = lab_image[0, 0, :]
    soil_color_rgb[1:] = soil_color_center
    
    # Converter a cor do solo para notação Munsell
    munsell_color = rgb_to_embrapa_munsell(*soil_color_rgb)
    
    return munsell_color

# Função principal do aplicativo
def main():
    st.title("Classificação de Cores de Solo")
    st.write("Este aplicativo realiza a classificação das cores de solo com base na notação Munsell e na clusterização de cores.")
    
    uploaded_file = st.file_uploader("Carregar Imagem", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagem do Solo", use_column_width=True)
        
        # Processar a imagem e classificar a cor do solo
        munsell_color = classify_soil_color(image)
        
        # Exibir a cor do solo classificada
        st.subheader("Cor do Solo Classificada:")
        st.write(munsell_color)
        
        # Exibir informações adicionais sobre o solo classificado
        if munsell_color in soil_dict:
            soil_info = soil_dict[munsell_color]
            st.subheader("Informações sobre o Solo:")
            st.write("Sistema Munsell:", soil_info["sistema_munsell"])
            st.write("Solo Embrapa:", soil_info["solo_embrapa"])
            st.write("Descrição:", soil_info["descricao"])
            st.write("Características:", soil_info["caracteristicas"])
            st.write("Vegetação Típica:", soil_info["vegetacao_tipica"])
            st.subheader("Cultivos e Manejo Recomendado:")
            st.write("Recomendados:", ", ".join(soil_info["cultivos_manejo_recomendado"]["recomendados"]))
            st.write("Condicionantes:", soil_info["cultivos_manejo_recomendado"]["condicionantes"])
            st.write("Manejo:", soil_info["cultivos_manejo_recomendado"]["manejo"])
            st.subheader("Propriedades do Solo:")
            st.write("pH:", soil_info["ph"])
            st.write("Condutividade Elétrica:", soil_info["condutividade_eletrica"])
            st.write("Teor de Nutrientes:", soil_info["teor_nutrientes"])
            st.subheader("Consequências do Manejo Inadequado:")
            st.write(", ".join(soil_info["manejo_inadequado"]["consequencias"]))
        else:
            st.subheader("Informações sobre o Solo:")
            st.write("Não foram encontradas informações para o solo classificado.")

# Executar o aplicativo
if __name__ == "__main__":
    main()
