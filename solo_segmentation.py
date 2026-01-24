#APP cor de solo Streamlit
import streamlit as st
import numpy as np
import cv2
from PIL import Image
import colorsys
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from fcmeans import FCM

# --- Helper Functions ---

def rgb_to_embrapa_munsell(r, g, b):
    # Inputs r, g, b in 0-255
    r_norm, g_norm, b_norm = r/255.0, g/255.0, b/255.0
    h, l, s = colorsys.rgb_to_hls(r_norm, g_norm, b_norm)
    hue_deg = h * 360

    # Mapeamento de Matiz (Hue) aproximado para cartas de solo
    if hue_deg < 14: m_hue = "10R"
    elif hue_deg < 23: m_hue = "2.5YR"
    elif hue_deg < 32: m_hue = "5YR"
    elif hue_deg < 41: m_hue = "7.5YR"
    elif hue_deg < 50: m_hue = "10YR"
    elif hue_deg < 59: m_hue = "2.5Y"
    elif hue_deg < 80: m_hue = "5Y"
    elif hue_deg < 120: m_hue = "5Y"
    elif hue_deg < 170: m_hue = "5G"
    elif hue_deg < 260: m_hue = "5B"
    else: m_hue = "N"

    # Mapeamento de Valor (Value)
    raw_value = l * 10
    valid_values = [2.5, 3, 4, 5, 6, 7, 8]
    m_value = min(valid_values, key=lambda x: abs(x - raw_value))

    # Mapeamento de Croma (Chroma)
    raw_chroma = s * 12
    valid_chromas = [1, 2, 3, 4, 6, 8]
    m_chroma = min(valid_chromas, key=lambda x: abs(x - raw_chroma))

    embrapa_munsell = f"{m_hue} {m_value}/{m_chroma}"
    return embrapa_munsell

def classify_soil_embrapa(munsell_str):
    try:
        parts = munsell_str.split()
        if len(parts) != 2: return None
        hue = parts[0]
        value_chroma = parts[1].split('/')
        if len(value_chroma) != 2: return None
        value = float(value_chroma[0])
        chroma = float(value_chroma[1])
    except:
        return None

    # Logic based on SiBCS
    if hue in ['10YR', '2.5Y', '5Y'] and value >= 6 and chroma <= 4:
         return {
            "solo_embrapa": "Neossolo Quartzarênico / Espodossolo",
            "descricao": "Solos arenosos, pouco desenvolvidos ou podzolizados.",
            "caracteristicas": "Cores claras (brancacentas/acinzentadas), textura arenosa.",
            "riscos": ["Lixiviação", "Erosão eólica"]
        }

    if hue in ['N', '5B', '5G', '5BG', '5Y', '2.5GY', '5GY', '10G', '10B'] or (chroma <= 2 and value >= 4):
        return {
            "solo_embrapa": "Gleissolo / Planossolo",
            "descricao": "Solos hidromórficos, saturação por água.",
            "caracteristicas": "Cores cinzentas/azuladas (glei).",
            "riscos": ["Encharcamento", "Salinização"]
        }

    if value <= 3 and chroma <= 3:
        return {
            "solo_embrapa": "Chernossolo / Organossolo",
            "descricao": "Solos ricos em matéria orgânica.",
            "caracteristicas": "Cor escura (preta/brunada), alta fertilidade potencial.",
            "riscos": ["Perda de MO"]
        }

    if hue in ['10R', '2.5YR']:
        return {
            "solo_embrapa": "Latossolo Vermelho / Nitossolo Vermelho",
            "descricao": "Solos muito intemperizados, ricos em hematita.",
            "caracteristicas": "Cor vermelha intensa, profundos, bem drenados.",
            "riscos": ["Erosão laminar", "Compactação"]
        }

    if hue in ['5YR', '7.5YR']:
        return {
            "solo_embrapa": "Latossolo / Argissolo Vermelho-Amarelo",
            "descricao": "Mistura de hematita e goethita.",
            "caracteristicas": "Cor bruna a vermelho-amarelada.",
            "riscos": ["Erosão laminar (Argissolos)"]
        }

    if hue in ['10YR', '2.5Y']:
        return {
            "solo_embrapa": "Latossolo Amarelo / Argissolo Amarelo",
            "descricao": "Solos ricos em goethita.",
            "caracteristicas": "Cor amarela a brunada. Baixa fertilidade natural.",
            "riscos": ["Coesão (Hardsetting)"]
        }

    return {
        "solo_embrapa": "Não Classificado",
        "descricao": "Cor fora dos padrões principais.",
        "caracteristicas": f"Matiz: {hue}, V: {value}, C: {chroma}",
        "riscos": []
    }

def convert_cluster_centers_to_munsell(cluster_centers):
    munsell_colors = []
    for center in cluster_centers:
        r, g, b = center
        munsell_color = rgb_to_embrapa_munsell(r, g, b)
        munsell_colors.append(munsell_color)
    return munsell_colors

def create_segmented_image(image_array, labels, cluster_centers, width, height):
    num_clusters = cluster_centers.shape[0]
    segmented_array = np.zeros_like(image_array)
    for i in range(num_clusters):
        segmented_array[labels == i] = cluster_centers[i]
    segmented_image = segmented_array.reshape((height, width, 3))
    segmented_image = segmented_image.astype(np.uint8)
    return segmented_image

def get_stats(image_array, labels, cluster_centers):
    errors = np.linalg.norm(image_array - cluster_centers[labels], axis=1)
    mean_error = np.mean(errors)
    std_deviation = np.std(errors)
    return mean_error, std_deviation

def analyze_image(image, n_clusters, method, resize_dim):
    # Resize
    resized_image = image.resize((resize_dim, resize_dim), Image.LANCZOS)
    image_array = np.array(resized_image)
    flat_image_array = image_array.reshape((image_array.shape[0] * image_array.shape[1], 3))
    flat_image_array_float = flat_image_array.astype(np.float64)

    # Cluster
    if method == "K-Means":
        model = KMeans(n_clusters=n_clusters, random_state=42)
        model.fit(flat_image_array_float)
        cluster_centers = model.cluster_centers_
        labels = model.labels_
    else: # FCM
        model = FCM(n_clusters=n_clusters)
        model.fit(flat_image_array_float)
        labels = model.predict(flat_image_array_float)
        cluster_centers = model.centers

    # Process results
    munsell_colors = convert_cluster_centers_to_munsell(cluster_centers)
    segmented_img = create_segmented_image(flat_image_array, labels, cluster_centers, resize_dim, resize_dim)
    mean_err, std_dev = get_stats(flat_image_array_float, labels, cluster_centers)

    # Classify main color (simplification: assume most frequent label or just list all)
    # Let's verify classification for the most dominant color
    unique_labels, counts = np.unique(labels, return_counts=True)
    dominant_idx = unique_labels[np.argmax(counts)]
    dominant_munsell = munsell_colors[dominant_idx]
    classification = classify_soil_embrapa(dominant_munsell)

    return {
        "segmented_image": segmented_img,
        "munsell_colors": munsell_colors,
        "dominant_munsell": dominant_munsell,
        "classification": classification,
        "mean_error": mean_err,
        "std_dev": std_dev,
        "flat_array": flat_image_array_float,
        "labels": labels,
        "centers": cluster_centers
    }

# --- Main Dashboard ---

def main():
    st.set_page_config(page_title="Dashboard Análise de Solo", layout="wide")

    st.title("📊 Dashboard de Classificação de Solos (Embrapa/SiBCS)")
    st.markdown("""
    Este dashboard permite a análise da cor do solo em amostras **secas** e **úmidas**,
    gerando a classificação provável segundo o Sistema Brasileiro de Classificação de Solos.
    """)

    # --- Sidebar ---
    st.sidebar.header("📁 Upload de Amostras")
    file_dry = st.sidebar.file_uploader("Foto Solo Seco", type=["jpg", "png", "jpeg"], key="dry")
    file_wet = st.sidebar.file_uploader("Foto Solo Úmido", type=["jpg", "png", "jpeg"], key="wet")

    st.sidebar.header("⚙️ Parâmetros")
    cluster_method = st.sidebar.selectbox("Algoritmo", ("K-Means", "Fuzzy C-Means"))
    n_clusters = st.sidebar.slider("Cores Dominantes (K)", 1, 5, 3)
    resize_dim = st.sidebar.slider("Resolução (px)", 50, 300, 150)

    # --- Processing ---

    if not file_dry and not file_wet:
        st.info("👋 Por favor, faça o upload de pelo menos uma imagem (Seco ou Úmido) para iniciar o Dashboard.")
        return

    # Container for Analysis
    if st.sidebar.button("Gerar Dashboard de Análise"):

        results_dry = None
        results_wet = None

        with st.spinner('Processando imagens...'):
            if file_dry:
                img_dry = Image.open(file_dry)
                results_dry = analyze_image(img_dry, n_clusters, cluster_method, resize_dim)

            if file_wet:
                img_wet = Image.open(file_wet)
                results_wet = analyze_image(img_wet, n_clusters, cluster_method, resize_dim)

        # --- Dashboard Layout ---

        # 1. Visual Comparison
        st.header("1. Análise Visual")
        c1, c2 = st.columns(2)

        with c1:
            if results_dry:
                st.subheader("Amostra Seca")
                st.image(file_dry, caption="Original", use_column_width=True)
                st.image(results_dry['segmented_image'], caption=f"Segmentada ({cluster_method})", use_column_width=True)
            else:
                st.warning("Amostra Seca não fornecida")

        with c2:
            if results_wet:
                st.subheader("Amostra Úmida")
                st.image(file_wet, caption="Original", use_column_width=True)
                st.image(results_wet['segmented_image'], caption=f"Segmentada ({cluster_method})", use_column_width=True)
            else:
                st.warning("Amostra Úmida não fornecida")

        # 2. Classification Data
        st.divider()
        st.header("2. Dados de Classificação (Cor Dominante)")

        c_dry, c_wet = st.columns(2)

        def display_card(title, res):
            if res:
                cls = res['classification']
                st.markdown(f"### {title}")
                st.metric("Cor Munsell (Dominante)", res['dominant_munsell'])
                st.markdown(f"**Classe:** {cls['solo_embrapa']}")
                st.write(f"_{cls['descricao']}_")

                with st.expander("Características e Riscos"):
                    st.write(f"**Características:** {cls['caracteristicas']}")
                    st.write("**Riscos/Limitações:**")
                    for r in cls['riscos']:
                        st.write(f"- {r}")

                st.write("**Todas as cores detectadas:**")
                st.code(", ".join(res['munsell_colors']))
            else:
                st.markdown(f"### {title}")
                st.write("Dados indisponíveis")

        with c_dry:
            display_card("Solo Seco", results_dry)

        with c_wet:
            display_card("Solo Úmido", results_wet)

        # 3. Validation Stats
        st.divider()
        st.header("3. Estatísticas de Validação")
        st.markdown("Métricas internas de qualidade do agrupamento de cores (menor erro = cores mais fiéis).")

        m1, m2, m3, m4 = st.columns(4)
        if results_dry:
            m1.metric("Erro Médio (Seco)", f"{results_dry['mean_error']:.2f}")
            m2.metric("Desvio Padrão (Seco)", f"{results_dry['std_dev']:.2f}")
        if results_wet:
            m3.metric("Erro Médio (Úmido)", f"{results_wet['mean_error']:.2f}")
            m4.metric("Desvio Padrão (Úmido)", f"{results_wet['std_dev']:.2f}")

        # Charts
        st.subheader("Distribuição de Erro")
        cg1, cg2 = st.columns(2)
        if results_dry:
            with cg1:
                st.caption("Histograma de Erro (Seco)")
                fig, ax = plt.subplots()
                ax.hist(np.linalg.norm(results_dry['flat_array'] - results_dry['centers'][results_dry['labels']], axis=1), bins=30, color='brown', alpha=0.7)
                st.pyplot(fig)
        if results_wet:
            with cg2:
                st.caption("Histograma de Erro (Úmido)")
                fig, ax = plt.subplots()
                ax.hist(np.linalg.norm(results_wet['flat_array'] - results_wet['centers'][results_wet['labels']], axis=1), bins=30, color='darkblue', alpha=0.7)
                st.pyplot(fig)

    # 4. Limitations and Methodology (Static)
    st.divider()
    with st.expander("⚠️ Limitações, Validação e Metodologia", expanded=False):
        st.markdown("""
        ### Limitações Técnicas
        1.  **Iluminação:** A precisão da cor depende drasticamente da iluminação da foto. Fotos tiradas sob luz solar direta vs sombra vs luz artificial produzirão resultados Munsell diferentes. Recomenda-se luz natural difusa.
        2.  **Calibração da Câmera:** Sensores de celular aplicam pós-processamento que altera as cores reais. Sem um cartão de referência de cor na imagem para calibração, os resultados são aproximados.
        3.  **Umidade:** A umidade escurece o solo (diminui o Valor). A classificação completa do SiBCS geralmente requer a cor do solo úmido e seco para determinações precisas (ex: variação de cor).
        4.  **Representatividade:** A análise é feita sobre a imagem carregada. Se a imagem contiver raízes, pedras ou sombras, isso afetará os clusters de cor.

        ### Validação do Algoritmo
        *   **Margem de Erro:** Calculada como a distância Euclidiana média entre a cor original do pixel e a cor do cluster atribuído (centroide).
        *   **Desvio Padrão:** Indica a dispersão das cores dentro de um mesmo grupo. Desvios altos indicam que o solo é muito heterogêneo ou o número de clusters (K) é insuficiente.

        ### Metodologia Embrapa
        A classificação apresentada é uma **inferência** baseada nas cores Munsell identificadas e nas regras gerais do Sistema Brasileiro de Classificação de Solos (SiBCS). A determinação definitiva de um tipo de solo requer análise granulométrica, química e morfológica em perfil de solo.
        """)

if __name__ == "__main__":
    main()
