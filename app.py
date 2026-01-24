#APP cor de solo Streamlit
import streamlit as st
import numpy as np
from PIL import Image
import colorsys
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from fcmeans import FCM

# --- CSS Styling (Cyberpunk) ---
def apply_cyberpunk_style():
    st.markdown("""
    <style>
        /* Base Colors */
        :root {
            --neon-cyan: #00f3ff;
            --neon-pink: #ff00ff;
            --neon-purple: #bd00ff;
            --neon-green: #00ff41;
            --dark-bg: #050505;
            --panel-bg: #111111;
            --text-color: #e0e0e0;
        }

        /* Main Background */
        .stApp {
            background-color: var(--dark-bg);
            color: var(--text-color);
            font-family: 'Courier New', Courier, monospace; /* Cyberpunk monospace feel */
        }

        /* Sidebar */
        .stSidebar {
            background-color: var(--panel-bg);
            border-right: 1px solid var(--neon-purple);
        }

        /* Typography - Headers */
        h1, h2, h3 {
            color: var(--neon-cyan) !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
        }

        h1 {
            border-bottom: 2px solid var(--neon-pink);
            padding-bottom: 10px;
        }

        /* Metrics */
        div[data-testid="stMetricValue"] {
            color: var(--neon-green) !important;
            text-shadow: 0 0 5px var(--neon-green);
            font-family: 'Orbitron', sans-serif;
        }

        div[data-testid="stMetricLabel"] {
            color: var(--neon-pink) !important;
        }

        /* Buttons */
        .stButton > button {
            background-color: transparent !important;
            color: var(--neon-cyan) !important;
            border: 1px solid var(--neon-cyan) !important;
            border-radius: 0px !important; /* Sharp edges */
            transition: all 0.3s ease;
            text-transform: uppercase;
            font-weight: bold;
            box-shadow: 0 0 5px var(--neon-cyan);
        }

        .stButton > button:hover {
            background-color: var(--neon-cyan) !important;
            color: black !important;
            box-shadow: 0 0 20px var(--neon-cyan);
        }

        /* Inputs / Selectboxes */
        .stSelectbox > div > div {
            background-color: var(--panel-bg) !important;
            color: var(--neon-green) !important;
            border: 1px solid var(--neon-purple) !important;
        }

        .stSlider > div > div > div > div {
            background-color: var(--neon-pink) !important;
        }

        /* Expanders */
        .streamlit-expanderHeader {
            background-color: #1a1a1a !important;
            color: var(--neon-purple) !important;
            border: 1px solid #333;
        }

        /* Dividers */
        hr {
            border-color: var(--neon-pink);
        }

        /* Warning/Info boxes customization */
        .stAlert {
            background-color: #1a1a1a;
            border: 1px solid var(--neon-cyan);
            color: var(--text-color);
        }

        /* Code blocks */
        code {
            color: var(--neon-green);
            background-color: #000;
            border: 1px solid #333;
        }

        /* Images */
        img {
            border: 1px solid var(--neon-cyan);
            box-shadow: 0 0 10px rgba(0, 243, 255, 0.2);
        }

    </style>
    """, unsafe_allow_html=True)

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
    # Resize and ensure RGB (handles RGBA)
    resized_image = image.resize((resize_dim, resize_dim), Image.LANCZOS).convert('RGB')
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

    # Apply Cyberpunk Style
    apply_cyberpunk_style()

    st.title("📊 CLASSIFICAÇÃO DE SOLOS (CYBER_SOIL)")
    st.markdown("""
    **SISTEMA DE ANÁLISE ESPECTRAL E CLASSIFICAÇÃO PEDOLÓGICA (SiBCS)**
    """)

    # --- Sidebar ---
    st.sidebar.header("📁 UPLOAD")
    file_dry = st.sidebar.file_uploader("AMOSTRA SECA", type=["jpg", "png", "jpeg"], key="dry")
    file_wet = st.sidebar.file_uploader("AMOSTRA ÚMIDA", type=["jpg", "png", "jpeg"], key="wet")

    st.sidebar.markdown("---")
    st.sidebar.header("⚙️ PARÂMETROS")
    cluster_method = st.sidebar.selectbox("ALGORITMO", ("K-Means", "Fuzzy C-Means"))
    n_clusters = st.sidebar.slider("CLUSTER (K)", 1, 5, 3)
    resize_dim = st.sidebar.slider("RESOLUÇÃO (PX)", 50, 300, 150)

    # --- Processing ---

    if not file_dry and not file_wet:
        st.info("👋 INICIE O SISTEMA: FAÇA O UPLOAD DE UMA AMOSTRA.")
        return

    # Container for Analysis
    if st.sidebar.button("INICIAR ANÁLISE"):

        results_dry = None
        results_wet = None

        with st.spinner('PROCESSANDO DADOS...'):
            if file_dry:
                img_dry = Image.open(file_dry)
                results_dry = analyze_image(img_dry, n_clusters, cluster_method, resize_dim)

            if file_wet:
                img_wet = Image.open(file_wet)
                results_wet = analyze_image(img_wet, n_clusters, cluster_method, resize_dim)

        # --- Dashboard Layout ---

        # 1. Visual Comparison
        st.header("1. ANÁLISE VISUAL")
        c1, c2 = st.columns(2)

        with c1:
            if results_dry:
                st.subheader("AMOSTRA SECA")
                st.image(file_dry, caption="ORIGINAL", use_column_width=True)
                st.image(results_dry['segmented_image'], caption=f"SEGMENTADA ({cluster_method})", use_column_width=True)
            else:
                st.warning("Amostra Seca não fornecida")

        with c2:
            if results_wet:
                st.subheader("AMOSTRA ÚMIDA")
                st.image(file_wet, caption="ORIGINAL", use_column_width=True)
                st.image(results_wet['segmented_image'], caption=f"SEGMENTADA ({cluster_method})", use_column_width=True)
            else:
                st.warning("Amostra Úmida não fornecida")

        # 2. Classification Data
        st.markdown("---")
        st.header("2. DADOS DE CLASSIFICAÇÃO")

        c_dry, c_wet = st.columns(2)

        def display_card(title, res):
            if res:
                cls = res['classification']
                st.markdown(f"### {title}")
                st.metric("COR MUNSELL (DOMINANTE)", res['dominant_munsell'])
                st.markdown(f"**CLASSE:** {cls['solo_embrapa']}")
                st.write(f"_{cls['descricao']}_")

                with st.expander("DETALHES TÉCNICOS"):
                    st.write(f"**CARACTERÍSTICAS:** {cls['caracteristicas']}")
                    st.write("**RISCOS:**")
                    for r in cls['riscos']:
                        st.write(f"- {r}")

                st.write("**PALETA DETECTADA:**")
                st.code(", ".join(res['munsell_colors']))
            else:
                st.markdown(f"### {title}")
                st.write("DADOS INDISPONÍVEIS")

        with c_dry:
            display_card("SOLO SECO", results_dry)

        with c_wet:
            display_card("SOLO ÚMIDO", results_wet)

        # 3. Validation Stats
        st.markdown("---")
        st.header("3. ESTATÍSTICAS (DEBUG)")

        m1, m2, m3, m4 = st.columns(4)
        if results_dry:
            m1.metric("ERRO MÉDIO (SECO)", f"{results_dry['mean_error']:.2f}")
            m2.metric("DESVIO PAD. (SECO)", f"{results_dry['std_dev']:.2f}")
        if results_wet:
            m3.metric("ERRO MÉDIO (ÚMIDO)", f"{results_wet['mean_error']:.2f}")
            m4.metric("DESVIO PAD. (ÚMIDO)", f"{results_wet['std_dev']:.2f}")

        # Charts
        st.subheader("DISTRIBUIÇÃO DE ERRO")
        cg1, cg2 = st.columns(2)

        # Helper for plots with dark theme
        def plot_dark_hist(data, color, label):
            fig, ax = plt.subplots()
            # Set plot background to transparent/dark
            fig.patch.set_facecolor('#0e1117')
            ax.set_facecolor('#0e1117')
            ax.hist(data, bins=30, color=color, alpha=0.8, edgecolor=color)

            # Color axis text
            ax.tick_params(colors='#00f3ff')
            ax.xaxis.label.set_color('#00f3ff')
            ax.yaxis.label.set_color('#00f3ff')
            ax.title.set_color('#ff00ff')

            # Color spines
            for spine in ax.spines.values():
                spine.set_edgecolor('#bd00ff')

            return fig

        if results_dry:
            with cg1:
                st.caption("HISTOGRAMA (SECO)")
                err_data = np.linalg.norm(results_dry['flat_array'] - results_dry['centers'][results_dry['labels']], axis=1)
                st.pyplot(plot_dark_hist(err_data, '#ff00ff', 'Erro'))
        if results_wet:
            with cg2:
                st.caption("HISTOGRAMA (ÚMIDO)")
                err_data = np.linalg.norm(results_wet['flat_array'] - results_wet['centers'][results_wet['labels']], axis=1)
                st.pyplot(plot_dark_hist(err_data, '#00f3ff', 'Erro'))

    # 4. Limitations and Methodology (Static)
    st.markdown("---")
    with st.expander("⚠️ PROTOCOLO E LIMITAÇÕES", expanded=False):
        st.markdown("""
        ### LIMITAÇÕES DO SISTEMA
        1.  **ILUMINAÇÃO:** A precisão espectral depende da fonte de luz. Use luz natural difusa.
        2.  **CALIBRAÇÃO:** Sem color checker, os resultados são aproximados devido ao pós-processamento do sensor.

        ### METODOLOGIA
        Classificação baseada em inferência de cor Munsell x SiBCS.
        """)

if __name__ == "__main__":
    main()
