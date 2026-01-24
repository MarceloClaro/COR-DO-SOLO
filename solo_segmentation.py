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
    # Inputs r, g, b in 0-255
    r_norm, g_norm, b_norm = r/255.0, g/255.0, b/255.0
    h, l, s = colorsys.rgb_to_hls(r_norm, g_norm, b_norm)
    hue_deg = h * 360

    # Mapeamento de Matiz (Hue) aproximado para cartas de solo
    # Centros aproximados: 10R(10), 2.5YR(18), 5YR(27), 7.5YR(36), 10YR(45), 2.5Y(54), 5Y(63)
    if hue_deg < 14: m_hue = "10R"
    elif hue_deg < 23: m_hue = "2.5YR"
    elif hue_deg < 32: m_hue = "5YR"
    elif hue_deg < 41: m_hue = "7.5YR"
    elif hue_deg < 50: m_hue = "10YR"
    elif hue_deg < 59: m_hue = "2.5Y"
    elif hue_deg < 80: m_hue = "5Y"
    elif hue_deg < 120: m_hue = "5Y" # Amarelo esverdeado
    elif hue_deg < 170: m_hue = "5G" # Verde (Glei)
    elif hue_deg < 260: m_hue = "5B" # Azul (Glei)
    else: m_hue = "N" # Neutro/Outros

    # Mapeamento de Valor (Value)
    # Value é aproximadamente L * 10. Valores comuns em cartas de solo: 2.5, 3, 4, 5, 6, 7, 8
    raw_value = l * 10
    valid_values = [2.5, 3, 4, 5, 6, 7, 8]
    m_value = min(valid_values, key=lambda x: abs(x - raw_value))

    # Mapeamento de Croma (Chroma)
    # Chroma está relacionado à saturação. Solos vão até 8 geralmente.
    # Fator de escala empírico: S=1.0 -> C=12 (vívido). S=0.6 -> C=7.2 (arredonda para 6 ou 8).
    raw_chroma = s * 12
    valid_chromas = [1, 2, 3, 4, 6, 8]
    m_chroma = min(valid_chromas, key=lambda x: abs(x - raw_chroma))

    # Formatação Munsell padrão
    embrapa_munsell = f"{m_hue} {m_value}/{m_chroma}"
    return embrapa_munsell

def classify_soil_embrapa(munsell_str):
    """
    Classifica o solo com base nos critérios da Embrapa/SiBCS usando a cor Munsell.
    Retorna um dicionário com detalhes da classificação.
    """
    try:
        parts = munsell_str.split()
        if len(parts) != 2:
            return None

        hue = parts[0]
        value_chroma = parts[1].split('/')
        if len(value_chroma) != 2:
            return None

        value = float(value_chroma[0])
        chroma = float(value_chroma[1])
    except:
        return None

    # Lógica baseada em princípios do SiBCS (Sistema Brasileiro de Classificação de Solos)

    # 1. Solos Claros/Arenosos (Neossolo Quartzarênico / Espodossolo)
    # Areias brancas ou muito claras, alto valor, baixo croma.
    if hue in ['10YR', '2.5Y', '5Y'] and value >= 6 and chroma <= 4:
         return {
            "solo_embrapa": "Neossolo Quartzarênico / Espodossolo",
            "descricao": "Solos arenosos, pouco desenvolvidos ou podzolizados. Presença de areias quartzosas.",
            "caracteristicas": "Cores claras (brancacentas ou acinzentadas), textura arenosa, baixa retenção de água e nutrientes.",
            "vegetacao_tipica": "Restinga, Campinarana, Cerrado (áreas arenosas).",
            "cultivos_manejo_recomendado": {
                "recomendados": ["Caju", "Coco", "Abacaxi", "Eucalipto", "Melancia"],
                "condicionantes": "Baixa fertilidade natural e baixa retenção de água.",
                "manejo": "Adubação parcelada e frequente, irrigação suplementar."
            },
            "ph": "4.5 - 6.0",
            "condutividade_eletrica": "Baixa",
            "teor_nutrientes": "Muito Baixo",
            "manejo_inadequado": {"consequencias": ["Lixiviação intensa de nutrientes", "Erosão eólica"]}
        }

    # 2. Solos Glei (Gleissolo / Planossolo)
    # Cores neutras, azuladas, esverdeadas ou matizes 2.5Y/5Y com croma baixo associado a encharcamento.
    if hue in ['N', '5B', '5G', '5BG', '5Y', '2.5GY', '5GY', '10G', '10B'] or (chroma <= 2 and value >= 4):
        return {
            "solo_embrapa": "Gleissolo / Planossolo",
            "descricao": "Solos hidromórficos, formados em condições de saturação por água (anaerobiose periódica ou permanente).",
            "caracteristicas": "Coloração cinzenta, azulada ou esverdeada (glei). Planossolos possuem horizonte B plânico impermeável.",
            "vegetacao_tipica": "Várzeas, banhados, matas de galeria, campos úmidos.",
            "cultivos_manejo_recomendado": {
                "recomendados": ["Arroz irrigado", "Pastagens (com drenagem)", "Olericultura (com drenagem)"],
                "condicionantes": "Excesso de água. Necessita de drenagem para a maioria das culturas de sequeiro.",
                "manejo": "Drenagem adequada ou cultivo de espécies adaptadas."
            },
            "ph": "Variável (frequentemente ácido)",
            "condutividade_eletrica": "Variável",
            "teor_nutrientes": "Variável",
            "manejo_inadequado": {"consequencias": ["Encharcamento", "Salinização (em áreas semiáridas)", "Compactação"]}
        }

    # 3. Solos Escuros (Chernossolo / Organossolo / Horizonte A Húmico)
    if value <= 3 and chroma <= 3:
        return {
            "solo_embrapa": "Chernossolo / Organossolo (ou Horizonte A Húmico)",
            "descricao": "Solos com altos teores de matéria orgânica, geralmente férteis e com boa estrutura.",
            "caracteristicas": "Cor escura (preta ou brunada muito escura). Chernossolos têm alta saturação por bases.",
            "vegetacao_tipica": "Campos, matas de araucária, florestas estacionais deciduais.",
            "cultivos_manejo_recomendado": {
                "recomendados": ["Milho", "Trigo", "Soja", "Feijão", "Hortaliças"],
                "condicionantes": "Geralmente férteis. Podem ser rasos ou pedregosos em algumas situações.",
                "manejo": "Evitar revolvimento excessivo para não oxidar a matéria orgânica (Plantio Direto)."
            },
            "ph": "5.5 - 7.0 (Chernossolo)",
            "condutividade_eletrica": "Baixa a Média",
            "teor_nutrientes": "Alto",
            "manejo_inadequado": {"consequencias": ["Perda rápida de matéria orgânica", "Erosão"]}
        }

    # 4. Solos Vermelhos (Latossolo Vermelho / Nitossolo Vermelho / Argissolo Vermelho)
    if hue in ['10R', '2.5YR']:
        return {
            "solo_embrapa": "Latossolo Vermelho / Nitossolo Vermelho / Argissolo Vermelho",
            "descricao": "Solos muito intemperizados, ricos em óxidos de ferro (hematita).",
            "caracteristicas": "Cor vermelha intensa, profundos, bem drenados. Latossolos são muito porosos; Nitossolos têm cerosidade e estrutura em blocos.",
            "vegetacao_tipica": "Cerrado, Mata Atlântica.",
            "cultivos_manejo_recomendado": {
                "recomendados": ["Soja", "Milho", "Café", "Cana-de-açúcar", "Citros", "Algodão"],
                "condicionantes": "Correção de acidez (calagem) e adubação fosfatada são geralmente necessárias.",
                "manejo": "Plantio direto, práticas conservacionistas."
            },
            "ph": "4.0 - 5.5 (Natural)",
            "condutividade_eletrica": "Baixa",
            "teor_nutrientes": "Baixo (Latossolo) a Médio/Alto (Nitossolo Eutrófico)",
            "manejo_inadequado": {"consequencias": ["Erosão laminar", "Compactação"]}
        }

    # 5. Solos Vermelho-Amarelos (Latossolo/Argissolo Vermelho-Amarelo)
    if hue in ['5YR', '7.5YR']:
        return {
            "solo_embrapa": "Latossolo Vermelho-Amarelo / Argissolo Vermelho-Amarelo",
            "descricao": "Solos com mistura de hematita e goethita. Muito comuns no Brasil.",
            "caracteristicas": "Cor bruna a vermelho-amarelada. Argissolos apresentam incremento de argila em profundidade (B textural).",
            "vegetacao_tipica": "Cerrado, Floresta Amazônica, Mata Atlântica.",
            "cultivos_manejo_recomendado": {
                "recomendados": ["Soja", "Pastagens", "Mandioca", "Fruticultura", "Silvicultura"],
                "condicionantes": "Baixa fertilidade natural e acidez elevada na maioria dos casos.",
                "manejo": "Cuidado redobrado com erosão em Argissolos devido à mudança textural."
            },
            "ph": "4.5 - 5.5",
            "condutividade_eletrica": "Baixa",
            "teor_nutrientes": "Baixo a Médio",
            "manejo_inadequado": {"consequencias": ["Erosão laminar acelerada (Argissolos)", "Degradação de pastagens"]}
        }

    # 6. Solos Amarelos (Latossolo Amarelo / Argissolo Amarelo)
    if hue in ['10YR', '2.5Y']:
        return {
            "solo_embrapa": "Latossolo Amarelo / Argissolo Amarelo",
            "descricao": "Solos ricos em goethita, comuns em regiões úmidas e Tabuleiros Costeiros.",
            "caracteristicas": "Cor amarela a brunada. Geralmente ácidos e com baixa fertilidade natural.",
            "vegetacao_tipica": "Floresta Amazônica, Mata Atlântica (Tabuleiros).",
            "cultivos_manejo_recomendado": {
                "recomendados": ["Mandioca", "Fruticultura (Maracujá, Mamão)", "Dendezeiro", "Pimenta-do-reino", "Cana-de-açúcar"],
                "condicionantes": "Correção de acidez e adubação. Alguns Latossolos Amarelos apresentam coesão.",
                "manejo": "Subsolagem em camadas coesas, manutenção da cobertura do solo."
            },
            "ph": "4.0 - 5.0",
            "condutividade_eletrica": "Baixa",
            "teor_nutrientes": "Baixo",
            "manejo_inadequado": {"consequencias": ["Adensamento/Coesão (Hardsetting)", "Erosão"]}
        }

    return {
        "solo_embrapa": "Não Classificado / Outros",
        "descricao": "A cor identificada não se enquadra nos padrões genéricos principais ou requer análise laboratorial complementar (textura, mineralogia).",
        "caracteristicas": f"Matiz: {hue}, Valor: {value}, Croma: {chroma}",
        "vegetacao_tipica": "-",
        "cultivos_manejo_recomendado": {
            "recomendados": [],
            "condicionantes": "",
            "manejo": ""
        },
        "ph": "-",
        "condutividade_eletrica": "-",
        "teor_nutrientes": "-",
        "manejo_inadequado": {"consequencias": []}
    }


# Dicionário de solos específicos (Amostras conhecidas para referência exata)
# Mantido para compatibilidade, mas o sistema agora usa a classificação genérica como fallback
soil_dict = {
    "2.5YR 5/8": {
        "sistema_munsell": "2.5YR 5/8",
        "solo_embrapa": "Latossolo Vermelho (Amostra Típica)",
        "descricao": "Solos profundos, com horizonte B latossólico.",
        "caracteristicas": "Textura argilosa, alta permeabilidade.",
        "vegetacao_tipica": "Cerrado.",
        "cultivos_manejo_recomendado": {"recomendados": ["Soja", "Milho"], "condicionantes": "Correção de solo.", "manejo": "Plantio Direto."},
        "ph": "5.0",
        "condutividade_eletrica": "Baixa",
        "teor_nutrientes": "Baixo",
        "manejo_inadequado": {"consequencias": ["Erosão"]}
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
    st.subheader("Cores Munsell Identificadas:")
    for color in munsell_colors:
        st.write(f"- {color}")


# Função para criar uma imagem segmentada com base na clusterização
def create_segmented_image(image_array, labels, cluster_centers, width, height):
    num_clusters = cluster_centers.shape[0]
    segmented_array = np.zeros_like(image_array)
    for i in range(num_clusters):
        segmented_array[labels == i] = cluster_centers[i]
    segmented_image = segmented_array.reshape((height, width, 3))
    segmented_image = segmented_image.astype(np.uint8)
    return segmented_image


def plot_munsell_distribution(munsell_colors):
    unique_colors, counts = np.unique(munsell_colors, return_counts=True)
    plt.figure(figsize=(10, 5))
    plt.bar(unique_colors, counts, color='skyblue')
    plt.xlabel("Cores Munsell")
    plt.ylabel("Contagem de Pixels (Aprox.)")
    plt.title("Distribuição das Cores Munsell Dominantes")
    plt.xticks(rotation=45)
    st.pyplot(plt.gcf())
    plt.clf()

def plot_error_distribution(image_array, labels, cluster_centers):
    errors = np.linalg.norm(image_array - cluster_centers[labels], axis=1)
    plt.figure(figsize=(10, 5))
    plt.hist(errors, bins=30, color='gray', alpha=0.7)
    plt.xlabel("Erro de Quantização (Distância Euclidiana RGB)")
    plt.ylabel("Frequência")
    plt.title("Histograma de Erro da Clusterização")
    st.pyplot(plt.gcf())
    plt.clf()

def plot_std_deviation_distribution(image_array, labels, cluster_centers):
    errors = np.linalg.norm(image_array - cluster_centers[labels], axis=1)
    std_deviation = np.std(errors)
    mean_error = np.mean(errors)

    plt.figure(figsize=(10, 5))
    plt.hist(errors, bins=30, density=True, color='lightgreen', alpha=0.6)
    plt.axvline(mean_error, color='b', linestyle='-', linewidth=2, label=f'Média: {mean_error:.2f}')
    plt.axvline(mean_error + std_deviation, color='r', linestyle='--', linewidth=2, label=f'+1 DP: {(mean_error+std_deviation):.2f}')
    plt.xlabel("Erro")
    plt.ylabel("Densidade")
    plt.title("Distribuição do Erro")
    plt.legend()
    st.pyplot(plt.gcf())
    plt.clf()

def plot_comparison_chart(kmeans_error, kmeans_std_deviation, fcm_error, fcm_std_deviation):
    labels = ['Erro Médio', 'Desvio Padrão']
    kmeans_values = [kmeans_error, kmeans_std_deviation]
    fcm_values = [fcm_error, fcm_std_deviation]

    bar_width = 0.35
    kmeans_positions = [i - bar_width/2 for i in range(len(labels))]
    fcm_positions = [i + bar_width/2 for i in range(len(labels))]

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(kmeans_positions, kmeans_values, width=bar_width, label='K-Means', color='blue', alpha=0.7)
    ax.bar(fcm_positions, fcm_values, width=bar_width, label='Fuzzy C-Means', color='orange', alpha=0.7)

    ax.set_ylabel('Valor')
    ax.set_title('Comparação de Desempenho: K-Means vs Fuzzy C-Means')
    ax.set_xticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.legend()

    return fig

def get_stats(image_array, labels, cluster_centers):
    errors = np.linalg.norm(image_array - cluster_centers[labels], axis=1)
    mean_error = np.mean(errors)
    std_deviation = np.std(errors)
    return mean_error, std_deviation

# Streamlit interface
def main():
    st.set_page_config(page_title="Classificação de Solos Munsell (Embrapa)", layout="wide")

    st.title("Classificação de Cores de Solo e Tipos (Embrapa/SiBCS)")
    st.markdown("Identificação automática de cores Munsell e classificação de tipos de solo baseada no Sistema Brasileiro de Classificação de Solos (SiBCS).")

    # Sidebar
    st.sidebar.header("Configurações da Análise")
    uploaded_file = st.sidebar.file_uploader("Carregar imagem do solo (JPG, PNG)", type=["jpg", "jpeg", "png"])
    cluster_method = st.sidebar.selectbox("Método de Clusterização", ("K-Means", "Fuzzy C-Means"))
    n_clusters = st.sidebar.slider("Número de Cores Dominantes (Clusters)", 1, 10, 3)
    resize_dim = st.sidebar.slider("Resolução de Processamento (px)", 50, 500, 150)

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Imagem Original", use_column_width=True)

        # Resize for processing
        resized_image = image.resize((resize_dim, resize_dim), Image.LANCZOS)
        image_array = np.array(resized_image)

        # Flatten
        flat_image_array = image_array.reshape((image_array.shape[0] * image_array.shape[1], 3))
        flat_image_array_float = flat_image_array.astype(np.float64)

        if st.sidebar.button("Executar Classificação"):
            with st.spinner('Processando imagem e classificando...'):

                # Clustering
                if cluster_method == "K-Means":
                    model = KMeans(n_clusters=n_clusters, random_state=42)
                    model.fit(flat_image_array_float)
                    cluster_centers = model.cluster_centers_
                    labels = model.labels_
                elif cluster_method == "Fuzzy C-Means":
                    model = FCM(n_clusters=n_clusters)
                    model.fit(flat_image_array_float)
                    labels = model.predict(flat_image_array_float)
                    cluster_centers = model.centers

                # Munsell Conversion
                munsell_colors = convert_cluster_centers_to_munsell(cluster_centers)

                # Create Segmented Image
                segmented_image = create_segmented_image(flat_image_array, labels, cluster_centers, resize_dim, resize_dim)

                with col2:
                    st.image(segmented_image, caption=f"Imagem Segmentada ({cluster_method})", use_column_width=True)

                # Results
                st.divider()
                display_munsell_colors(munsell_colors)

                mean_error, std_deviation = get_stats(flat_image_array_float, labels, cluster_centers)
                st.info(f"Qualidade da segmentação: Erro Médio = {mean_error:.2f} | Desvio Padrão = {std_deviation:.2f}")

                # Classification Logic
                st.subheader("Interpretação Pedológica (Embrapa/SiBCS)")

                for i, color in enumerate(munsell_colors):
                    soil_info = None
                    source = ""

                    # 1. Try exact match
                    if color in soil_dict:
                        soil_info = soil_dict[color]
                        source = "Base de Dados (Exata)"
                    # 2. Try general rules
                    else:
                        soil_info = classify_soil_embrapa(color)
                        if soil_info:
                            source = "Classificação Geral (Regras SiBCS)"

                    with st.expander(f"Cor #{i+1}: {color} - {source}", expanded=True):
                        if soil_info:
                            st.markdown(f"**Classe de Solo Provável:** {soil_info['solo_embrapa']}")
                            st.write(f"**Descrição:** {soil_info['descricao']}")
                            st.write(f"**Características:** {soil_info['caracteristicas']}")
                            st.write(f"**Vegetação:** {soil_info['vegetacao_tipica']}")

                            col_m1, col_m2 = st.columns(2)
                            with col_m1:
                                st.write("**Cultivos Recomendados:**")
                                for crop in soil_info['cultivos_manejo_recomendado']['recomendados']:
                                    st.write(f"- {crop}")
                            with col_m2:
                                st.write("**Manejo:**")
                                st.write(soil_info['cultivos_manejo_recomendado']['manejo'])
                                if soil_info['cultivos_manejo_recomendado']['condicionantes']:
                                    st.write(f"*Obs: {soil_info['cultivos_manejo_recomendado']['condicionantes']}*")
                        else:
                            st.warning("Não foi possível classificar automaticamente esta cor com as regras atuais.")

                st.divider()
                st.subheader("Análise Estatística da Imagem")
                col_g1, col_g2 = st.columns(2)
                with col_g1:
                    plot_munsell_distribution(munsell_colors)
                with col_g2:
                    plot_std_deviation_distribution(flat_image_array_float, labels, cluster_centers)

                if st.button("Comparar Algoritmos (K-Means vs FCM)"):
                     with st.spinner('Comparando...'):
                        km = KMeans(n_clusters=n_clusters, random_state=42).fit(flat_image_array_float)
                        km_stats = get_stats(flat_image_array_float, km.labels_, km.cluster_centers_)

                        fcm = FCM(n_clusters=n_clusters)
                        fcm.fit(flat_image_array_float)
                        fcm_stats = get_stats(flat_image_array_float, fcm.predict(flat_image_array_float), fcm.centers)

                        st.pyplot(plot_comparison_chart(km_stats[0], km_stats[1], fcm_stats[0], fcm_stats[1]))

    # Footer/Docs
    st.divider()
    with st.expander("Metodologia e Referências"):
        st.write("""
        **Metodologia:**
        O sistema converte os pixels da imagem para o espaço de cor RGB e utiliza algoritmos de agrupamento (K-Means ou Fuzzy C-Means) para identificar as cores dominantes.
        Estas cores são convertidas para o sistema Munsell (Matiz, Valor, Croma) utilizando uma aproximação matemática.
        A classificação do solo segue as regras gerais do Sistema Brasileiro de Classificação de Solos (SiBCS - Embrapa), associando cores a classes de solos (ex: Latossolos Vermelhos, Gleissolos, etc.).

        **Referências:**
        1. Santos, H. G. et al. (2018). Sistema Brasileiro de Classificação de Solos. 5. ed. Brasília, DF: Embrapa.
        2. Munsell Soil Color Charts.
        """)

if __name__ == "__main__":
    main()
