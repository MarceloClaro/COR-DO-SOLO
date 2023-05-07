import streamlit as st
import numpy as np
import cv2
from PIL import Image
import colorsys
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from fcmeans import FCM
from skimage.color import rgb2lab, deltaE_ciede2000

# Função para converter cores RGB em notação Munsell conforme as 160 classificações de cores de solo da Embrapa
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
    "7.5YR5/6": {
        "sistema_munsell": "7.5YR5/6",
        "solo_embrapa": "Argissolo Amarelo",
        "descricao": "Solos jovens, com presença de horizonte B textural e baixa saturação por bases.",
        "caracteristicas": "Textura predominantemente argilosa, elevado teor de alumínio e baixa fertilidade natural.",
        "vegetacao_tipica": "Floresta Amazônica, Cerrado e Caatinga.",
        "cultivos_manejo": "Culturas anuais e perenes, com uso de práticas conservacionistas e correção da acidez e da fertilidade do solo."
    },
    "2.5YR3/6": {
        "sistema_munsell": "2.5YR3/6",
        "solo_embrapa": "Latossolo Vermelho",
        "descricao": "Solos profundos, com presença de horizonte B latossólico e elevada saturação por bases.",
        "caracteristicas": "Textura predominantemente argilosa, alta capacidade de armazenamento de água e nutrientes.",
        "vegetacao_tipica": "Floresta Atlântica, Cerrado e Mata de Araucária.",
        "cultivos_manejo": "Culturas anuais e perenes, com uso de práticas conservacionistas e correção da acidez e da fertilidade do solo."
    },
    "5YR4/4": {
        "sistema_munsell": "5YR4/4",
        "solo_embrapa": "Neossolo Quartzarênico",
        "descricao": "Solos jovens, com presença de horizonte A fraco ou ausente e baixa fertilidade natural.",
        "caracteristicas": "Textura predominantemente arenosa, baixa capacidade de armazenamento de água e nutrientes.",
        "vegetacao_tipica": "Caatinga, Cerrado e Restinga.",
        "cultivos_manejo": "Uso limitado para agricultura. Recomenda-se a adoção de práticas conservacionistas e correção da fertilidade do solo."
    },
    "5YR3/4": {
        "sistema_munsell": "5YR3/4",
        "solo_embrapa": "Cambissolo Háplico",
        "descricao": "Solos jovens, com presença de horizonte B incipiente e elevada saturação por bases.",
        "caracteristicas": "Textura predominantemente argilosa, baixa fertilidade natural e suscetibilidade à erosão.",
        "vegetacao_tipica": "Cerrado, Mata Atlântica e Floresta de Araucária.",
        "cultivos_manejo": "Culturas anuais e perenes, com uso de práticas conservacionistas e correção da acidez e da fertilidade do solo."
    },
    "2.5YR3/6": {
        "sistema_munsell": "2.5YR3/6",
        "solo_embrapa": "Nitossolo Vermelho",
        "descricao": "Solos profundos, com presença de horizonte B textural e elevada saturação por bases.",
        "caracteristicas": "Textura predominantemente argilosa, alta capacidade de armazenamento de água e nutrientes.",
        "vegetacao_tipica": "Mata Atlântica, Cerrado e Floresta de Araucária.",
        "cultivos_manejo": "Culturas anuais e perenes, com uso de práticas conservacionistas e correção da acidez e da fertilidade do solo."
    },
    "10YR3/3": {
        "sistema_munsell": "10YR3/3",
        "solo_embrapa": "Planossolo",
        "descricao": "Solos rasos, com presença de horizonte B incipiente e elevada saturação por bases.",
        "caracteristicas": "Textura variada, com teores elevados de alumínio e baixa fertilidade natural.",
        "vegetacao_tipica": "Cerrado, Caatinga e Mata Atlântica.",
        "cultivos_manejo": "Uso limitado para agricultura. Recomenda-se a adoção de práticas conservacionistas e correção da acidez e da fertilidade do solo."
    },
    "10YR3/3": {
        "sistema_munsell": "10YR3/3",
        "solo_embrapa": "Gleissolo",
        "descricao": "Solos hidromórficos, com presença de horizonte glei e elevada saturação por água.",
        "caracteristicas": "Textura variada, com baixa fertilidade natural e suscetibilidade à compactação.",
        "vegetacao_tipica": "Mata Atlântica, Cerrado e Pantanal.",
        "cultivos_manejo": "Uso limitado para agricultura. Recomenda-se a adoção de práticas conservacionistas e drenagem adequada do solo."
    },
    "7.5YR3/4": {
        "sistema_munsell": "7.5YR3/4",
        "solo_embrapa": "Vertissolo",
        "descricao": "Solos profundos, com presença de horizonte B textural e elevada saturação por bases.",
        "caracteristicas": "Textura argilosa, elevada capacidade de armazenamento de água e nutrientes, e suscetibilidade à fissuração.",
        "vegetacao_tipica": "Cerrado, Caatinga e Mata Atlântica.",
        "cultivos_manejo": "Culturas anuais e perenes, com uso de práticas conservacionistas e correção da acidez e da fertilidade do solo."
    },
    "10YR3/3": {
        "sistema_munsell": "10YR3/3",
        "solo_embrapa": "Luvissolo",
        "descricao": "Solos jovens, com presença de horizonte B textural e baixa saturação por bases.",
        "caracteristicas": "Textura argilosa a média, baixa fertilidade natural e suscetibilidade à compactação.",
        "vegetacao_tipica": "Cerrado, Caatinga e Mata Atlântica.",
        "cultivos_manejo": "Culturas anuais e perenes, com uso de práticas conservacionistas e correção da acidez e da fertilidade do solo."
    },
    "7.5YR4/4": {
        "sistema_munsell": "7.5YR4/4",
        "solo_embrapa": "Espodossolo",
        "descricao": "Solos profundos, com presença de horizonte B espódico e elevada saturação por alumínio.",
        "caracteristicas": "Textura média a arenosa, baixa fertilidade natural e suscetibilidade à erosão.",
        "vegetacao_tipica": "Cerrado, Caatinga e Floresta Amazônica.",
        "cultivos_manejo": "Uso limitado para agricultura. Recomenda-se a adoção de práticas conservacionistas e correção da acidez e da fertilidade do solo."
    },
    "10YR2/1": {
        "sistema_munsell": "10YR2/1",
        "solo_embrapa": "Chernossolo",
        "descricao": "Solos profundos, com presença de horizonte A orgânico e elevada saturação por bases.",
        "caracteristicas": "Textura argilosa, alta fertilidade natural e suscetibilidade à compactação.",
        "vegetacao_tipica": "Pampa e Cerrado.",
        "cultivos_manejo": "Culturas anuais e perenes, com uso de práticas conservacionistas e correção da acidez do solo."
    },
    "10YR7/4": {
        "sistema_munsell": "10YR7/4",
        "solo_embrapa": "Areias Quartzosas",
        "descricao": "Solos jovens, com presença de horizonte A pouco desenvolvido e baixa fertilidade natural.",
        "caracteristicas": "Textura predominantemente arenosa, baixa capacidade de armazenamento de água e nutrientes.",
        "vegetacao_tipica": "Restinga, Caatinga e Cerrado.",
        "cultivos_manejo": "Uso limitado para agricultura. Recomenda-se a adoção de práticas conservacionistas e correção da fertilidade do solo."
    },
    "5YR4/6": {
        "sistema_munsell": "5YR4/6",
        "solo_embrapa": "Podzólico Vermelho-Amarelo",
        "descricao": "Solos profundos, com presença de horizonte B textural e baixa saturação por bases.",
        "caracteristicas": "Textura arenosa a média, baixa fertilidade natural e suscetibilidade à erosão.",
        "vegetacao_tipica": "Cerrado, Caatinga e Mata Atlântica.",
        "cultivos_manejo": "Culturas anuais e perenes, com uso de práticas conservacionistas e correção da acidez e da fertilidade do solo."
    },
    "10YR2/2": {
        "sistema_munsell": "10YR2/2",
        "solo_embrapa": "Organossolo",
        "descricao": "Solos hidromórficos, com presença de horizonte O e elevado teor de matéria orgânica.",
        "caracteristicas": "Textura variada, elevada capacidade de retenção de água e nutrientes, e baixa fertilidade natural.",
        "vegetacao_tipica": "Mata Atlântica, Amazônia e Cerrado.",
        "cultivos_manejo": "Uso limitado para agricultura. Recomenda-se a adoção de práticas conservacionistas e correção da acidez e da fertilidade do solo."
    },
    "7.5YR4/4": {
        "sistema_munsell": "7.5YR4/4",
        "solo_embrapa": "Plintossolo",
        "descricao": "Solos hidromórficos, com presença de horizonte plíntico e elevada saturação por água.",
        "caracteristicas": "Textura variada, baixa fertilidade natural e suscetibilidade à compactação.",
        "vegetacao_tipica": "Mata Atlântica, Cerrado e Pantanal.",
        "cultivos_manejo": "Uso limitado para agricultura. Recomenda-se a adoção de práticas conservacionistas e drenagem adequada do solo."
    },
    "10YR8/2": {
        "sistema_munsell": "10YR8/2",
        "solo_embrapa": "Calcário",
        "descricao": "Sedimentos de rochas calcárias, com elevado teor de cálcio e pH alcalino.",
        "caracteristicas": "Textura variada, elevada capacidade de armazenamento de água e nutrientes, e alta fertilidade natural.",
        "vegetacao_tipica": "Mata Atlântica, Cerrado e Caatinga.",
        "cultivos_manejo": "Culturas anuais e perenes, com uso de práticas conservacionistas e correção da acidez do solo."
    },
}


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
        if cluster_method == "K-Means":
            kmeans = KMeans(n_clusters=n_clusters)
            kmeans.fit(image_array)
            cluster_centers = kmeans.cluster_centers_
            labels = kmeans.labels_
        elif cluster_method == "Fuzzy C-Means":
            fcm = FCM(n_clusters=n_clusters)
            fcm.fit(image_array)
            labels = fcm.predict(image_array)
            cluster_centers = fcm.centers

        munsell_colors = convert_cluster_centers_to_munsell(cluster_centers)

        display_munsell_colors(munsell_colors)

        segmented_image = create_segmented_image(image_array, labels, cluster_centers)
        st.image(segmented_image, caption="Imagem de solo segmentada", use_column_width=True)
if name == 'main':
main()

