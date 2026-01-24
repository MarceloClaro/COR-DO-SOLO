#APP cor de solo Streamlit
import streamlit as st
import numpy as np
import cv2
from PIL import Image
import colorsys
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from fcmeans import FCM

# Função para converter cores RGB em notação Munsell conforme a classificação de cores de solo da Embrapa
def rgb_to_embrapa_munsell(r, g, b):
    # Converter de RGB para HLS
    # colorsys.rgb_to_hls expects inputs in range 0-1
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
        "ph": "4.5 - 5.5",
        "condutividade_eletrica": "Baixa",
        "teor_nutrientes": "Médio",
        "manejo_inadequado": {
            "consequencias": ["Erosão", "Perda de nutrientes", "Degradação ambiental"]
        }
    },
    "10YR 7/2": {
        "sistema_munsell": "10YR 7/2",
        "solo_embrapa": "Neossolo Quartzarênico",
        "descricao": "Solos pouco desenvolvidos, com baixa capacidade de retenção de água e baixa fertilidade natural.",
        "caracteristicas": "Textura arenosa, drenagem rápida e susceptível à erosão.",
        "vegetacao_tipica": "Vegetação de restinga, caatinga e cerrado.",
        "cultivos_manejo_recomendado": {
            "recomendados": ["Coco", "Cajueiro", "Pinus", "Eucalipto"],
            "condicionantes": "Irrigação e adubação são necessárias para melhorar a produtividade.",
            "manejo": "Práticas conservacionistas, como plantio direto, rotação de culturas e uso de cobertura vegetal, são recomendadas para preservar a qualidade do solo."
        },
        "ph": "5.0 - 6.0",
        "condutividade_eletrica": "Baixa",
        "teor_nutrientes": "Baixo",
        "manejo_inadequado": {
            "consequencias": ["Erosão", "Perda de nutrientes", "Degradação ambiental"]
        }
    },
    "10YR 5/4": {
        "sistema_munsell": "10YR 5/4",
        "solo_embrapa": "Cambissolo Háplico",
        "descricao": "Solos com horizonte B incipiente e moderada capacidade de retenção de água.",
        "caracteristicas": "Textura média a argilosa, moderada fertilidade natural e susceptível à erosão.",
        "vegetacao_tipica": "Mata Atlântica, cerrado e caatinga.",
        "cultivos_manejo_recomendado": {
            "recomendados": ["Milho", "Feijão", "Mandioca", "Hortaliças"],
            "condicionantes": "Adubação e correção do solo podem ser necessárias para melhorar a fertilidade.",
            "manejo": "Práticas conservacionistas, como plantio direto, rotação de culturas e uso de cobertura vegetal, são recomendadas para preservar a qualidade do solo."
        },
        "ph": "5.5 - 6.5",
        "condutividade_eletrica": "Baixa",
        "teor_nutrientes": "Médio",
        "manejo_inadequado": {
            "consequencias": ["Erosão", "Perda de nutrientes", "Degradação ambiental"]
        }
    },
    "2.5YR 4/6": {
        "sistema_munsell": "2.5YR 4/6",
        "solo_embrapa": "Nitossolo Vermelho",
        "descricao": "Solos bem desenvolvidos, com horizonte B nítico e alta capacidade de retenção de água.",
        "caracteristicas": "Textura argilosa, alta fertilidade natural e boa capacidade de armazenamento de água.",
        "vegetacao_tipica": "Floresta Amazônica, Mata Atlântica e Cerrado.",
        "cultivos_manejo_recomendado": {
            "recomendados": ["Soja", "Milho", "Café", "Cana-de-açúcar"],
            "condicionantes": "Adubação e irrigação podem ser necessárias para maximizar a produtividade.",
            "manejo": "Práticas conservacionistas, como plantio direto, rotação de culturas e uso de cobertura vegetal, são recomendadas para preservar a qualidade do solo."
        },
        "ph": "6.0 - 6.5",
        "condutividade_eletrica": "Baixa",
        "teor_nutrientes": "Alto",
        "manejo_inadequado": {
            "consequencias": ["Erosão", "Perda de nutrientes", "Degradação ambiental"]
        }
    },
    "10YR 6/3": {
        "sistema_munsell": "10YR 6/3",
        "solo_embrapa": "Planossolo",
        "descricao": "Solos com horizonte B textural e baixa a média capacidade de retenção de água.",
        "caracteristicas": "Textura média a argilosa, moderada fertilidade natural e susceptível à encharcamento.",
        "vegetacao_tipica": "Cerrado, campos úmidos e áreas alagáveis.",
        "cultivos_manejo_recomendado": {
            "recomendados": ["Arroz", "Pastagens", "Canola", "Soja"],
            "condicionantes": "Drenagem e adubação podem ser necessárias para melhorar a produtividade.",
            "manejo": "Práticas conservacionistas, como plantio direto, rotação de culturas e uso de cobertura vegetal, são recomendadas para preservar a qualidade do solo."
        },
        "ph": "5.0 - 6.0",
        "condutividade_eletrica": "Baixa",
        "teor_nutrientes": "Médio",
        "manejo_inadequado": {
            "consequencias": ["Erosão", "Perda de nutrientes", "Degradação ambiental"]
        }
    },
    "10YR 4/1": {
        "sistema_munsell": "10YR 4/1",
        "solo_embrapa": "Gleissolo",
        "descricao": "Solos hidromórficos, geralmente encharcados, com horizonte B textural ou hístico.",
        "caracteristicas": "Textura variável, baixa a média fertilidade natural e alta capacidade de retenção de água.",
        "vegetacao_tipica": "Áreas alagáveis, várzeas e banhados.",
        "cultivos_manejo_recomendado": {
            "recomendados": ["Arroz", "Taro", "Açaí", "Pupunha"],
            "condicionantes": "Drenagem e adubação podem ser necessárias para melhorar a produtividade.",
            "manejo": "Práticas conservacionistas, como plantio direto, rotação de culturas e uso de cobertura vegetal, são recomendadas para preservar a qualidade do solo."
        },
        "ph": "4.5 - 6.0",
        "condutividade_eletrica": "Baixa",
        "teor_nutrientes": "Baixo a médio",
        "manejo_inadequado": {
            "consequencias": ["Erosão", "Perda de nutrientes", "Degradação ambiental"]
        }
    },
    "2.5YR 4/4": {
        "sistema_munsell": "2.5YR 4/4",
        "solo_embrapa": "Vertissolo",
        "descricao": "Solos com horizonte B vértico, caracterizados por grande quantidade de argila expansiva.",
        "caracteristicas": "Textura argilosa, alta capacidade de retenção de água e média a alta fertilidade natural.",
        "vegetacao_tipica": "Cerrado, Caatinga e áreas de transição.",
        "cultivos_manejo_recomendado": {
            "recomendados": ["Algodão", "Milho", "Sorgo", "Pastagens"],
            "condicionantes": "Correção do solo e adubação podem ser necessárias para melhorar a produtividade.",
            "manejo": "Práticas conservacionistas, como plantio direto, rotação de culturas e uso de cobertura vegetal, são recomendadas para preservar a qualidade do solo."
        },
        "ph": "5.5 - 6.5",
        "condutividade_eletrica": "Baixa",
        "teor_nutrientes": "Médio a alto",
        "manejo_inadequado": {
            "consequencias": ["Erosão", "Perda de nutrientes", "Degradação ambiental"]
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
def create_segmented_image(image_array, labels, cluster_centers, width, height):
    num_clusters = cluster_centers.shape[0]
    segmented_array = np.zeros_like(image_array)
    for i in range(num_clusters):
        segmented_array[labels == i] = cluster_centers[i]
    segmented_image = segmented_array.reshape((height, width, 3))
    # Removed incorrect * 255 scaling. cluster_centers are already in 0-255 if input was.
    segmented_image = segmented_image.astype(np.uint8)
    return segmented_image


def plot_munsell_distribution(munsell_colors):
    unique_colors, counts = np.unique(munsell_colors, return_counts=True)
    plt.figure(figsize=(10, 5))
    plt.bar(unique_colors, counts)
    plt.xlabel("Cores Munsell")
    plt.ylabel("Frequência")
    plt.title("Distribuição das cores Munsell")
    plt.xticks(rotation=45)
    st.pyplot(plt.gcf())
    plt.clf()

def plot_error_distribution(image_array, labels, cluster_centers):
    # Calculate error for each point relative to its assigned cluster center
    errors = np.linalg.norm(image_array - cluster_centers[labels], axis=1)

    plt.figure(figsize=(10, 5))
    plt.hist(errors, bins='auto')
    plt.xlabel("Margem de erro (Distância Euclidiana)")
    plt.ylabel("Frequência")
    plt.title("Distribuição da margem de erro")
    st.pyplot(plt.gcf())
    plt.clf()

def plot_std_deviation_distribution(image_array, labels, cluster_centers):
    errors = np.linalg.norm(image_array - cluster_centers[labels], axis=1)
    std_deviation = np.std(errors)

    plt.figure(figsize=(10, 5))
    plt.hist(errors, bins='auto', density=True)
    plt.axvline(std_deviation, color='r', linestyle='dashed', linewidth=2, label=f'Desvio Padrão: {std_deviation:.2f}')
    plt.xlabel("Erro")
    plt.ylabel("Densidade")
    plt.title("Distribuição do erro com Desvio Padrão")
    plt.legend()
    st.pyplot(plt.gcf())
    plt.clf()

def plot_comparison_chart(kmeans_error, kmeans_std_deviation, fcm_error, fcm_std_deviation):
    # Definindo os dados para o gráfico
    labels = ['Margem de Erro Média', 'Desvio Padrão']
    kmeans_values = [kmeans_error, kmeans_std_deviation]
    fcm_values = [fcm_error, fcm_std_deviation]

    # Definindo a largura das barras
    bar_width = 0.35

    # Criando as posições das barras
    kmeans_positions = [i - bar_width/2 for i in range(len(labels))]
    fcm_positions = [i + bar_width/2 for i in range(len(labels))]

    # Configurando o gráfico
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(kmeans_positions, kmeans_values, width=bar_width, label='K-Means')
    ax.bar(fcm_positions, fcm_values, width=bar_width, label='Fuzzy C-Means')

    # Adicionando títulos e rótulos aos eixos
    ax.set_ylabel('Valores')
    ax.set_title('Comparação entre K-Means e Fuzzy C-Means')
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.legend()

    return fig

# Helper to calculate stats
def get_stats(image_array, labels, cluster_centers):
    errors = np.linalg.norm(image_array - cluster_centers[labels], axis=1)
    mean_error = np.mean(errors)
    std_deviation = np.std(errors)
    return mean_error, std_deviation

# Streamlit interface
def main():
    st.set_page_config(page_title="Classificação de Solos Munsell", layout="wide")

    st.title("Classificação de cores de solo com base na notação Munsell")

    # Sidebar for controls
    st.sidebar.header("Configurações")

    uploaded_file = st.sidebar.file_uploader("Selecione uma imagem de solo", type=["jpg", "jpeg", "png"])

    cluster_method = st.sidebar.selectbox("Escolha o método de clusterização:", ("K-Means", "Fuzzy C-Means"))
    n_clusters = st.sidebar.slider("Número de clusters (cores dominantes)", min_value=1, max_value=10, value=3)
    resize_dim = st.sidebar.slider("Resolução da análise (px)", min_value=50, max_value=300, value=150, step=50)

    original_rgb = st.sidebar.checkbox("Manter os tons originais da imagem (visualização)", value=False)

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)

        with col1:
            st.image(image, caption="Imagem de solo carregada", use_column_width=True)

        resized_image = image.resize((resize_dim, resize_dim), Image.LANCZOS)
        image_array = np.array(resized_image)
        # Normalize to 0-1 for processing if needed, but RGB usually 0-255 for these libs?
        # Scikit-learn KMeans expects 2D array.
        # Image is (H, W, 3). Flatten to (H*W, 3).
        flat_image_array = image_array.reshape((image_array.shape[0] * image_array.shape[1], 3))
        # Ensure it's float for some operations if needed, but 0-255 int is fine for KMeans usually (it converts internally)
        # But for centroids we want float.
        flat_image_array_float = flat_image_array.astype(np.float64)

        if st.sidebar.button("Classificar cores"):
            with st.spinner('Processando...'):
                if cluster_method == "K-Means":
                    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                    kmeans.fit(flat_image_array_float)
                    cluster_centers = kmeans.cluster_centers_
                    labels = kmeans.labels_
                elif cluster_method == "Fuzzy C-Means":
                    fcm = FCM(n_clusters=n_clusters)
                    fcm.fit(flat_image_array_float)
                    labels = fcm.predict(flat_image_array_float)
                    cluster_centers = fcm.centers

                munsell_colors = convert_cluster_centers_to_munsell(cluster_centers)

                segmented_image = create_segmented_image(flat_image_array, labels, cluster_centers, resize_dim, resize_dim)

                with col2:
                    st.image(segmented_image, caption=f"Imagem segmentada ({cluster_method})", use_column_width=True)

                display_munsell_colors(munsell_colors)

                # Calculate stats
                mean_error, std_deviation = get_stats(flat_image_array_float, labels, cluster_centers)

                st.subheader("Estatísticas:")
                st.write(f"Margem de erro média: {mean_error:.2f}")
                st.write(f"Desvio padrão: {std_deviation:.2f}")

                # Exibir informações de classificação do solo
                st.subheader("Classificação do solo (Embrapa):")
                found_soil = False
                for color in munsell_colors:
                    if color in soil_dict:
                        found_soil = True
                        soil_info = soil_dict[color]
                        with st.expander(f"Detalhes para {color}"):
                            st.write(f"**Solo Embrapa:** {soil_info['solo_embrapa']}")
                            st.write(f"**Descrição:** {soil_info['descricao']}")
                            st.write(f"**Características:** {soil_info['caracteristicas']}")
                            st.write(f"**Vegetação típica:** {soil_info['vegetacao_tipica']}")
                            st.write("**Cultivos e manejo recomendado:**")
                            st.write(f"  - Recomendados: {', '.join(soil_info['cultivos_manejo_recomendado']['recomendados'])}")
                            st.write(f"  - Condicionantes: {soil_info['cultivos_manejo_recomendado']['condicionantes']}")
                            st.write(f"  - Manejo: {soil_info['cultivos_manejo_recomendado']['manejo']}")
                            st.write(f"**pH:** {soil_info['ph']}")
                            st.write(f"**Condutividade elétrica:** {soil_info['condutividade_eletrica']}")
                            st.write(f"**Teor de nutrientes:** {soil_info['teor_nutrientes']}")
                            st.write("**Manejo inadequado:**")
                            st.write(f"  - Consequências: {', '.join(soil_info['manejo_inadequado']['consequencias'])}")

                if not found_soil:
                    st.info("Nenhuma classificação exata encontrada na base de dados para as cores detectadas.")

                # Exibir gráficos
                st.subheader("Gráficos:")
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    plot_munsell_distribution(munsell_colors)
                with col_g2:
                    plot_error_distribution(flat_image_array_float, labels, cluster_centers)

                plot_std_deviation_distribution(flat_image_array_float, labels, cluster_centers)

                # Comparison (Optional)
                if st.button("Comparar K-Means e Fuzzy C-Means"):
                    # We need to run both to compare
                    with st.spinner('Executando comparação...'):
                        # Run K-Means
                        km = KMeans(n_clusters=n_clusters, random_state=42)
                        km.fit(flat_image_array_float)
                        km_centers = km.cluster_centers_
                        km_labels = km.labels_
                        km_error, km_std = get_stats(flat_image_array_float, km_labels, km_centers)

                        # Run FCM
                        fcm_comp = FCM(n_clusters=n_clusters)
                        fcm_comp.fit(flat_image_array_float)
                        fcm_labels_comp = fcm_comp.predict(flat_image_array_float)
                        fcm_centers_comp = fcm_comp.centers
                        fcm_error, fcm_std = get_stats(flat_image_array_float, fcm_labels_comp, fcm_centers_comp)

                        st.subheader("Comparação de Métodos")
                        st.write(f"K-Means - Erro: {km_error:.2f}, Desvio: {km_std:.2f}")
                        st.write(f"Fuzzy C-Means - Erro: {fcm_error:.2f}, Desvio: {fcm_std:.2f}")

                        chart = plot_comparison_chart(km_error, km_std, fcm_error, fcm_std)
                        st.pyplot(chart)

    # Documentation section
    with st.expander("Sobre o aplicativo"):
        st.write("""
        Este aplicativo utiliza a notação Munsell para classificar as cores do solo. Ele utiliza algoritmos de clusterização, como K-Means e Fuzzy C-Means, para identificar e agrupar cores semelhantes presentes na imagem do solo. Em seguida, ele converte as cores médias dos clusters para a notação Munsell e exibe informações relevantes sobre a classificação do solo, como a descrição, características, vegetação típica e cultivos e manejo recomendado, de acordo com os padrões estabelecidos pela Embrapa.
        O código apresentado consiste em um aplicativo para classificação de cores de solo baseado na notação Munsell e na clusterização de cores. O aplicativo tem como funcionalidades principais:
        - Conversão de cores RGB para notação Munsell de acordo com a classificação de cores de solo da Embrapa;
        - Implementação de algoritmos de clusterização, K-Means e Fuzzy C-Means;
        - Cálculo da margem de erro e desvio padrão da clusterização;
        - Exibição de informações sobre a classificação do solo, como descrição, características, vegetação típica e cultivos e manejo recomendado;
        - Exibição de gráficos, como distribuição das cores Munsell, margem de erro e desvio padrão.
        """)

    with st.expander("Como usar"):
        st.write("""
        1. Faça o upload de uma imagem do solo que você deseja analisar na barra lateral.
        2. Selecione o método de clusterização que você deseja usar (K-Means ou Fuzzy C-Means).
        3. Selecione o número de clusters que você deseja usar na análise.
        4. Clique no botão 'Classificar cores' para iniciar a análise.
        5. O aplicativo exibirá a imagem segmentada, a classificação do solo, gráficos e informações adicionais sobre a margem de erro e desvio padrão.
        6. Explore os resultados e ajuste as configurações conforme necessário para obter os melhores resultados.
        """)

    with st.expander("Créditos e Referências"):
        st.write("""
        **Créditos:**
        Este aplicativo foi desenvolvido usando a biblioteca Streamlit para Python. Agradecimentos especiais à Embrapa pelo fornecimento das informações sobre a classificação de solos e notação Munsell.

        Desenvolvedor: [professor Marcelo Claro]
        Contato: [marceloclaro@gmail.com]
        GitHub: [https://github.com/MarceloClaro/COR-DO-SOLO]

        **Referências:**
        1. Munsell Soil Color Charts. [https://www.munsell.com/color-services/color-standards/soil-color-charts/]
        2. Embrapa. Sistema Brasileiro de Classificação de Solos. [https://www.embrapa.br/solos/sistema-brasileiro-de-classificacao-de-solos]
        3. Streamlit. [https://www.streamlit.io/]
        """)

if __name__ == "__main__":
    main()
