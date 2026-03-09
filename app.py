#!/usr/bin/env python3
"""
Sistema EMBRAPA de Classificação de Solos
Framework Streamlit + TensorFlow para análise de imagens de solo
Classificação segundo critérios EMBRAPA - SiBCS (Sistema Brasileiro de Classificação de Solos)
Desenvolvido por: Professor Marcelo Claro
"""

import streamlit as st
import numpy as np
import cv2
from PIL import Image
import colorsys
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sklearn.cluster import KMeans
import warnings
import io
import json

warnings.filterwarnings("ignore")

# ─── Optional imports ───────────────────────────────────────────────────────
TF_AVAILABLE = False
try:
    import tensorflow as tf
    from tensorflow.keras.applications import MobileNetV2
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    TF_AVAILABLE = True
except ImportError:
    pass

FCM_AVAILABLE = False
try:
    from fcmeans import FCM
    FCM_AVAILABLE = True
except ImportError:
    pass

# ═══════════════════════════════════════════════════════════════════════════
# SEÇÃO 1 – BASE DE DADOS EMBRAPA (SiBCS)
# ═══════════════════════════════════════════════════════════════════════════

# Parâmetros HSV típicos por tipo de solo (hue 0-360, sat 0-100, val 0-100)
# Usados para cálculo de similaridade de cor
SOIL_HSV = {
    "Latossolo Vermelho": {
        "h_mean": 8, "h_std": 8, "s_mean": 65, "s_std": 15, "v_mean": 35, "v_std": 10,
    },
    "Latossolo Vermelho-Amarelo": {
        "h_mean": 20, "h_std": 10, "s_mean": 55, "s_std": 15, "v_mean": 50, "v_std": 12,
    },
    "Latossolo Amarelo": {
        "h_mean": 35, "h_std": 10, "s_mean": 45, "s_std": 15, "v_mean": 65, "v_std": 10,
    },
    "Argissolo Vermelho-Amarelo": {
        "h_mean": 22, "h_std": 12, "s_mean": 50, "s_std": 15, "v_mean": 55, "v_std": 12,
    },
    "Nitossolo Vermelho": {
        "h_mean": 6, "h_std": 6, "s_mean": 70, "s_std": 12, "v_mean": 28, "v_std": 8,
    },
    "Neossolo Quartzarênico": {
        "h_mean": 38, "h_std": 14, "s_mean": 18, "s_std": 10, "v_mean": 82, "v_std": 10,
    },
    "Cambissolo Háplico": {
        "h_mean": 30, "h_std": 12, "s_mean": 38, "s_std": 15, "v_mean": 55, "v_std": 12,
    },
    "Gleissolo Háplico": {
        "h_mean": 45, "h_std": 15, "s_mean": 12, "s_std": 8, "v_mean": 45, "v_std": 12,
    },
    "Planossolo Háplico": {
        "h_mean": 38, "h_std": 14, "s_mean": 16, "s_std": 8, "v_mean": 70, "v_std": 10,
    },
    "Vertissolo": {
        "h_mean": 25, "h_std": 12, "s_mean": 30, "s_std": 12, "v_mean": 28, "v_std": 8,
    },
    "Chernossolo": {
        "h_mean": 30, "h_std": 12, "s_mean": 22, "s_std": 10, "v_mean": 22, "v_std": 8,
    },
    "Espodossolo": {
        "h_mean": 20, "h_std": 12, "s_mean": 10, "s_std": 8, "v_mean": 75, "v_std": 12,
    },
}

EMBRAPA_SOLOS = {
    "Latossolo Vermelho": {
        "codigo": "LV",
        "descricao": "Solos profundos (>2m) com horizonte B latossólico. Coloração vermelha intensa por altos teores de óxidos de ferro (hematita). Textura muito argilosa.",
        "area_brasil": "~18% do território",
        "biomas": ["Cerrado", "Mata Atlântica", "Amazônia"],
        "composicao": {"argila": (60, 80), "silte": (5, 15), "areia": (10, 30), "materia_organica": (2, 5), "Fe2O3": (15, 25), "Al2O3": (20, 35)},
        "quimica": {"ph": (4.5, 5.5), "ctc": "Baixa-média (5-10 cmolc/dm³)", "sat_bases": "<50% (distrófico)", "sat_aluminio": "Variável (0-40%)"},
        "drenagem": "Acentuada a bem drenado",
        "erodibilidade": "Baixa a moderada",
        "cultivos": {
            "Soja": "Alta", "Milho": "Alta", "Café": "Alta", "Cana-de-açúcar": "Alta",
            "Algodão": "Média", "Eucalipto": "Alta", "Pastagens": "Alta", "Citros": "Média"
        },
        "correcao": {
            "calagem": "Necessária. pH típico 4,5-5,5. Aplicar 2-4 t/ha de calcário dolomítico (PRNT 100%).",
            "fosfatagem": "Alta necessidade (solos fixam muito P). 100-200 kg P₂O₅/ha no plantio.",
            "adubacao_npk": "N: 60-120 kg/ha | P₂O₅: 80-160 kg/ha | K₂O: 60-120 kg/ha",
            "micronutrientes": "Zinco (2-5 kg ZnSO₄/ha) e Boro (0,5-1 kg B/ha) frequentemente deficientes.",
            "materia_organica": "Plantio direto. Rotação de culturas. Incorporar resíduos culturais.",
            "gessagem": "Recomendada para subsolos com alta saturação de Al. 1-3 t/ha."
        }
    },
    "Latossolo Vermelho-Amarelo": {
        "codigo": "LVA",
        "descricao": "Latossolo com matiz entre 2,5YR e 5YR. Transição entre vermelho e amarelo. Muito comum no Brasil Central e Sudeste.",
        "area_brasil": "~22% do território",
        "biomas": ["Cerrado", "Mata Atlântica", "Caatinga"],
        "composicao": {"argila": (35, 60), "silte": (10, 20), "areia": (20, 50), "materia_organica": (1.5, 4), "Fe2O3": (7, 15), "Al2O3": (15, 25)},
        "quimica": {"ph": (4.5, 5.5), "ctc": "Baixa (4-8 cmolc/dm³)", "sat_bases": "<50%", "sat_aluminio": "Variável"},
        "drenagem": "Bem a acentuadamente drenado",
        "erodibilidade": "Baixa a moderada",
        "cultivos": {
            "Soja": "Alta", "Milho": "Alta", "Eucalipto": "Alta", "Pastagens": "Alta",
            "Mandioca": "Alta", "Feijão": "Média", "Café": "Média", "Cana-de-açúcar": "Alta"
        },
        "correcao": {
            "calagem": "Necessária. Aplicar 2-3 t/ha de calcário dolomítico.",
            "fosfatagem": "Alta necessidade. 80-150 kg P₂O₅/ha.",
            "adubacao_npk": "N: 60-100 kg/ha | P₂O₅: 60-120 kg/ha | K₂O: 60-100 kg/ha",
            "micronutrientes": "Zinco, Boro e Manganês.",
            "materia_organica": "Plantio direto e rotação de culturas.",
            "gessagem": "Recomendada quando há Al tóxico no subsolo."
        }
    },
    "Latossolo Amarelo": {
        "codigo": "LA",
        "descricao": "Latossolo com matiz 7,5YR a 10YR, coloração amarelada por predomínio de caulinita e gibbsita. Muito comum na Amazônia.",
        "area_brasil": "~15% do território",
        "biomas": ["Amazônia"],
        "composicao": {"argila": (40, 70), "silte": (5, 15), "areia": (15, 40), "materia_organica": (1, 3), "Fe2O3": (2, 7), "Al2O3": (20, 40)},
        "quimica": {"ph": (4.0, 5.0), "ctc": "Muito baixa (3-6 cmolc/dm³)", "sat_bases": "<30%", "sat_aluminio": "Alta (>50%)"},
        "drenagem": "Bem a excessivamente drenado",
        "erodibilidade": "Baixa",
        "cultivos": {
            "Dendê (Palma)": "Alta", "Cupuaçu": "Alta", "Castanha": "Alta",
            "Seringueira": "Alta", "Soja": "Média", "Pastagens": "Média"
        },
        "correcao": {
            "calagem": "URGENTE. pH muito baixo (4,0-5,0) com alta toxidez de Al. Aplicar 3-5 t/ha.",
            "fosfatagem": "Muito alta necessidade. 120-200 kg P₂O₅/ha.",
            "adubacao_npk": "N: 80-120 kg/ha | P₂O₅: 100-180 kg/ha | K₂O: 80-120 kg/ha",
            "micronutrientes": "Zinco, Cobre, Boro e Molibdênio.",
            "materia_organica": "Adicionar 10-20 t/ha de composto orgânico. Solo muito pobre.",
            "gessagem": "Recomendada para todo o perfil."
        }
    },
    "Argissolo Vermelho-Amarelo": {
        "codigo": "PVA",
        "descricao": "Solos com gradiente textural abrupto (horizonte B textural). Susceptíveis à erosão. Muito ampla distribuição geográfica no Brasil.",
        "area_brasil": "~15% do território",
        "biomas": ["Mata Atlântica", "Cerrado", "Caatinga", "Pampa"],
        "composicao": {"argila": (20, 50), "silte": (10, 25), "areia": (30, 65), "materia_organica": (1, 3), "Fe2O3": (5, 12), "Al2O3": (10, 20)},
        "quimica": {"ph": (4.5, 5.5), "ctc": "Baixa-média (5-10 cmolc/dm³)", "sat_bases": "<50%", "sat_aluminio": "Variável"},
        "drenagem": "Moderada a bem drenado",
        "erodibilidade": "Moderada a alta",
        "cultivos": {
            "Milho": "Alta", "Feijão": "Alta", "Mandioca": "Alta",
            "Cana-de-açúcar": "Média", "Citros": "Média", "Pastagens": "Alta", "Soja": "Média"
        },
        "correcao": {
            "calagem": "Necessária. Aplicar 1,5-3 t/ha de calcário.",
            "fosfatagem": "Média a alta necessidade. 60-120 kg P₂O₅/ha.",
            "adubacao_npk": "N: 60-100 kg/ha | P₂O₅: 60-100 kg/ha | K₂O: 60-100 kg/ha",
            "micronutrientes": "Zinco e Boro.",
            "materia_organica": "Plantio direto fundamental para evitar erosão.",
            "manejo_erosao": "CRÍTICO: terraços, curvas de nível, cobertura permanente do solo."
        }
    },
    "Nitossolo Vermelho": {
        "codigo": "NV",
        "descricao": "Solos bem desenvolvidos com horizonte B nítico (faces lustrosas). Estrutura em blocos bem desenvolvida. Geralmente de alta fertilidade natural.",
        "area_brasil": "~3% do território",
        "biomas": ["Mata Atlântica", "Sul do Brasil"],
        "composicao": {"argila": (55, 80), "silte": (5, 15), "areia": (10, 30), "materia_organica": (2, 5), "Fe2O3": (15, 30), "Al2O3": (15, 25)},
        "quimica": {"ph": (5.0, 6.5), "ctc": "Média-alta (8-15 cmolc/dm³)", "sat_bases": "Variável (eutrófico ou distrófico)", "sat_aluminio": "Baixa"},
        "drenagem": "Bem a acentuadamente drenado",
        "erodibilidade": "Baixa a moderada",
        "cultivos": {
            "Café": "Muito Alta", "Soja": "Alta", "Milho": "Alta", "Trigo": "Alta",
            "Cana-de-açúcar": "Alta", "Citros": "Alta", "Feijão": "Alta"
        },
        "correcao": {
            "calagem": "Moderada (solos mais férteis). 1-2 t/ha quando necessário.",
            "fosfatagem": "Média necessidade. 60-100 kg P₂O₅/ha.",
            "adubacao_npk": "N: 80-150 kg/ha | P₂O₅: 60-100 kg/ha | K₂O: 80-120 kg/ha",
            "micronutrientes": "Zinco e Boro ocasionalmente.",
            "materia_organica": "Manutenção com rotação de culturas e resíduos."
        }
    },
    "Neossolo Quartzarênico": {
        "codigo": "RQ",
        "descricao": "Solos arenosos (>85% areia) com mínima diferenciação de horizontes. Muito permeáveis, grande susceptibilidade à lixiviação e erosão eólica.",
        "area_brasil": "~11% do território",
        "biomas": ["Cerrado", "Caatinga", "Amazônia"],
        "composicao": {"argila": (0, 10), "silte": (0, 10), "areia": (85, 100), "materia_organica": (0.5, 1.5), "Fe2O3": (0.1, 1), "Al2O3": (0.5, 3)},
        "quimica": {"ph": (4.5, 6.0), "ctc": "Muito baixa (1-3 cmolc/dm³)", "sat_bases": "Variável", "sat_aluminio": "Pode ser alta"},
        "drenagem": "Excessivamente drenado",
        "erodibilidade": "Alta a muito alta (eólica e hídrica)",
        "cultivos": {
            "Caju": "Alta", "Coco": "Alta", "Melancia": "Alta",
            "Eucalipto": "Alta", "Pinus": "Alta", "Pastagens": "Média"
        },
        "correcao": {
            "calagem": "Aplicar conforme análise. 1-2 t/ha parcelado.",
            "fosfatagem": "PARCELADO para evitar lixiviação. 40-80 kg P₂O₅/ha.",
            "adubacao_npk": "PARCELADO: N: 40-80 | P₂O₅: 40-80 | K₂O: 40-80 kg/ha",
            "micronutrientes": "Zinco, Cobre e Manganês.",
            "materia_organica": "ESSENCIAL: 15-20 t/ha de composto. Cobertura vegetal permanente.",
            "irrigacao": "Necessária para a maioria das culturas. Solo retém pouca água."
        }
    },
    "Cambissolo Háplico": {
        "codigo": "CX",
        "descricao": "Solos em processo de desenvolvimento com horizonte B incipiente. Textura e fertilidade variáveis. Muito comuns em áreas de relevo ondulado.",
        "area_brasil": "~7% do território",
        "biomas": ["Mata Atlântica", "Cerrado", "Caatinga", "Pampa", "Amazônia"],
        "composicao": {"argila": (15, 55), "silte": (15, 40), "areia": (20, 60), "materia_organica": (2, 6), "Fe2O3": (3, 10), "Al2O3": (8, 20)},
        "quimica": {"ph": (5.0, 6.5), "ctc": "Média (6-12 cmolc/dm³)", "sat_bases": "Variável", "sat_aluminio": "Variável"},
        "drenagem": "Variável",
        "erodibilidade": "Moderada a alta",
        "cultivos": {
            "Milho": "Alta", "Feijão": "Alta", "Hortaliças": "Alta",
            "Mandioca": "Alta", "Fruticultura": "Média", "Pastagens": "Alta"
        },
        "correcao": {
            "calagem": "Geralmente necessária. 1-3 t/ha.",
            "fosfatagem": "Moderada. 60-100 kg P₂O₅/ha.",
            "adubacao_npk": "N: 60-120 kg/ha | P₂O₅: 60-100 kg/ha | K₂O: 60-100 kg/ha",
            "micronutrientes": "Zinco, Boro e Manganês.",
            "materia_organica": "Rotação de culturas e cobertura vegetal."
        }
    },
    "Gleissolo Háplico": {
        "codigo": "GX",
        "descricao": "Solos hidromórficos com gleização (redução de Fe e Mn). Ocorrem em áreas alagadas ou com lençol freático alto. Horizonte glei cinzento/azulado.",
        "area_brasil": "~4% do território",
        "biomas": ["Amazônia", "Pantanal", "Mata Atlântica (várzeas)"],
        "composicao": {"argila": (30, 70), "silte": (20, 45), "areia": (5, 35), "materia_organica": (3, 8), "Fe2O3": (1, 5), "Al2O3": (10, 25)},
        "quimica": {"ph": (4.5, 6.5), "ctc": "Média-alta (8-20 cmolc/dm³)", "sat_bases": "Variável", "sat_aluminio": "Variável"},
        "drenagem": "Mal a muito mal drenado",
        "erodibilidade": "Baixa (planícies)",
        "cultivos": {
            "Arroz Irrigado": "Alta", "Açaí": "Alta", "Banana": "Alta",
            "Taro": "Alta", "Pastagens (drenado)": "Média"
        },
        "correcao": {
            "calagem": "Após drenagem. 2-4 t/ha.",
            "fosfatagem": "Moderada. 60-100 kg P₂O₅/ha.",
            "adubacao_npk": "N: 60-100 | P₂O₅: 60-100 | K₂O: 60-100 kg/ha",
            "micronutrientes": "Zinco e Manganês (cuidado com toxidez de Mn).",
            "materia_organica": "Rico em MO naturalmente.",
            "drenagem": "ESSENCIAL: implementar sistema de drenagem antes do cultivo."
        }
    },
    "Planossolo Háplico": {
        "codigo": "SX",
        "descricao": "Solos com mudança textural abrupta e drenagem impedida. Caracterizados pela alternância de molhamento e secagem. Comuns no Pampa gaúcho.",
        "area_brasil": "~5% do território",
        "biomas": ["Pampa", "Cerrado", "Nordeste"],
        "composicao": {"argila": (15, 45), "silte": (20, 40), "areia": (25, 60), "materia_organica": (1, 3), "Fe2O3": (1, 5), "Al2O3": (8, 18)},
        "quimica": {"ph": (5.0, 6.5), "ctc": "Baixa-média (5-12 cmolc/dm³)", "sat_bases": "Variável", "sat_aluminio": "Moderada"},
        "drenagem": "Imperfeitamente a mal drenado",
        "erodibilidade": "Moderada",
        "cultivos": {
            "Arroz": "Alta", "Pastagens": "Alta", "Soja (com drenagem)": "Média",
            "Sorgo": "Média", "Canola": "Média", "Girassol": "Média"
        },
        "correcao": {
            "calagem": "Necessária. 1-3 t/ha.",
            "fosfatagem": "Moderada. 60-100 kg P₂O₅/ha.",
            "adubacao_npk": "N: 60-100 | P₂O₅: 60-100 | K₂O: 60-100 kg/ha",
            "micronutrientes": "Zinco e Manganês.",
            "materia_organica": "Adição de MO para melhorar estrutura.",
            "drenagem": "Drenagem superficial e subsuperficial recomendada."
        }
    },
    "Vertissolo": {
        "codigo": "V",
        "descricao": "Solos com alta proporção de argila expansiva (esmectita/montmorilonita). Apresentam fendas quando secos e são muito pegajosos quando úmidos.",
        "area_brasil": "<2% do território",
        "biomas": ["Caatinga", "Cerrado", "Pantanal"],
        "composicao": {"argila": (55, 80), "silte": (10, 30), "areia": (5, 25), "materia_organica": (1, 3), "Fe2O3": (2, 8), "Al2O3": (10, 20)},
        "quimica": {"ph": (5.5, 7.5), "ctc": "Alta (20-50 cmolc/dm³)", "sat_bases": ">50% (eutrófico)", "sat_aluminio": "Baixa"},
        "drenagem": "Imperfeitamente drenado",
        "erodibilidade": "Moderada",
        "cultivos": {
            "Algodão": "Alta", "Milho": "Alta", "Sorgo": "Alta",
            "Pastagens": "Alta", "Girassol": "Média", "Feijão": "Média"
        },
        "correcao": {
            "calagem": "Geralmente não necessária (pH já adequado). Verificar análise.",
            "fosfatagem": "Moderada. 60-100 kg P₂O₅/ha.",
            "adubacao_npk": "N: 60-100 | P₂O₅: 60-100 | K₂O: 40-80 kg/ha",
            "micronutrientes": "Boro, Zinco e Molibdênio.",
            "materia_organica": "Adicionar para melhorar estrutura e manejo.",
            "manejo_fisico": "Evitar tráfego pesado quando úmido. Manejo cuidadoso da umidade."
        }
    },
    "Chernossolo": {
        "codigo": "M",
        "descricao": "Solos com horizonte A chernozêmico escuro e rico em matéria orgânica. Alta fertilidade natural. Ocorrem principalmente no Sul do Brasil.",
        "area_brasil": "<1% do território",
        "biomas": ["Pampa", "Cerrado"],
        "composicao": {"argila": (30, 70), "silte": (15, 40), "areia": (10, 45), "materia_organica": (4, 10), "Fe2O3": (3, 8), "Al2O3": (10, 20)},
        "quimica": {"ph": (6.0, 7.5), "ctc": "Alta (15-30 cmolc/dm³)", "sat_bases": ">65% (eutrófico)", "sat_aluminio": "Muito baixa"},
        "drenagem": "Bem drenado",
        "erodibilidade": "Baixa",
        "cultivos": {
            "Soja": "Muito Alta", "Trigo": "Muito Alta", "Milho": "Muito Alta",
            "Cevada": "Alta", "Canola": "Alta", "Pastagens": "Alta"
        },
        "correcao": {
            "calagem": "Geralmente não necessária. Monitorar pH.",
            "fosfatagem": "Baixa a moderada. 40-80 kg P₂O₅/ha.",
            "adubacao_npk": "N: 80-150 | P₂O₅: 40-80 | K₂O: 60-100 kg/ha",
            "micronutrientes": "Zinco e Manganês eventualmente.",
            "materia_organica": "Manutenção com plantio direto e rotação."
        }
    },
    "Espodossolo": {
        "codigo": "E",
        "descricao": "Solos com horizonte espódico (acúmulo iluvial de matéria orgânica e/ou Al e Fe). Comum em restingas e áreas de baixada com vegetação de cerrado/campos.",
        "area_brasil": "~3% do território",
        "biomas": ["Amazônia", "Mata Atlântica (restingas)"],
        "composicao": {"argila": (2, 15), "silte": (2, 10), "areia": (80, 95), "materia_organica": (1, 4), "Fe2O3": (0.5, 3), "Al2O3": (1, 5)},
        "quimica": {"ph": (3.5, 5.5), "ctc": "Muito baixa (1-5 cmolc/dm³)", "sat_bases": "Muito baixa", "sat_aluminio": "Alta"},
        "drenagem": "Excessivo a impedido",
        "erodibilidade": "Alta",
        "cultivos": {
            "Pinus": "Alta", "Eucalipto": "Média", "Caju": "Média",
            "Coco": "Baixa", "Pastagens": "Baixa"
        },
        "correcao": {
            "calagem": "Urgente. pH muito baixo. 2-4 t/ha.",
            "fosfatagem": "Alta. Parcelado para evitar lixiviação. 80-120 kg P₂O₅/ha.",
            "adubacao_npk": "Parcelado: N: 40-80 | P₂O₅: 60-100 | K₂O: 40-80 kg/ha",
            "micronutrientes": "Zinco, Cobre e Boro.",
            "materia_organica": "ESSENCIAL. 20+ t/ha de composto.",
            "observacoes": "Solo de baixíssima aptidão agrícola. Prefira reflorestamento."
        }
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# SEÇÃO 2 – BANCO DE DADOS DE CULTURAS
# ═══════════════════════════════════════════════════════════════════════════

CULTURAS_DB = {
    "Soja": {"ph_ideal": (6.0, 6.5), "ph_critico": 5.8, "v_ideal": 60,
             "npk": {"N": "20-30 (fixação BNF)", "P2O5": "60-120", "K2O": "80-120"},
             "micro": ["Molibdênio (0,02 kg/ha)", "Cobalto (0,003 kg/ha)", "Zinco (2 kg/ha)", "Boro (0,5 kg/ha)"],
             "producao": "3-5 t/ha", "obs": "Inoculação com Bradyrhizobium japonicum ESSENCIAL."},
    "Milho": {"ph_ideal": (5.8, 7.0), "ph_critico": 5.5, "v_ideal": 60,
              "npk": {"N": "80-180", "P2O5": "60-120", "K2O": "60-120"},
              "micro": ["Zinco (2-4 kg ZnSO₄/ha)", "Boro (0,5 kg/ha)"],
              "producao": "6-14 t/ha", "obs": "Parcelar N: 1/3 plantio + 2/3 cobertura (V4-V6)."},
    "Café": {"ph_ideal": (5.5, 6.5), "ph_critico": 5.3, "v_ideal": 60,
             "npk": {"N": "120-300", "P2O5": "40-80", "K2O": "120-200"},
             "micro": ["Zinco", "Boro (0,5-1 kg/ha)", "Ferro", "Manganês"],
             "producao": "25-50 sacas/ha", "obs": "Cultura perene; adubação parcelada (4-6x/ano)."},
    "Cana-de-açúcar": {"ph_ideal": (6.0, 6.5), "ph_critico": 5.5, "v_ideal": 65,
                        "npk": {"N": "60-120", "P2O5": "60-100", "K2O": "100-180"},
                        "micro": ["Zinco", "Boro", "Cobre"],
                        "producao": "70-130 t/ha", "obs": "Grande exportação de K. Vinhaça (30-150 m³/ha) substitui K na soqueira."},
    "Arroz": {"ph_ideal": (5.5, 6.5), "ph_critico": 5.0, "v_ideal": 50,
              "npk": {"N": "60-120", "P2O5": "40-80", "K2O": "40-80"},
              "micro": ["Zinco (2-3 kg ZnSO₄/ha)"],
              "producao": "5-10 t/ha", "obs": "Arroz irrigado tolera solos ácidos. Parcelar N (plantio + perfilhamento + primórdio)."},
    "Feijão": {"ph_ideal": (6.0, 7.0), "ph_critico": 5.8, "v_ideal": 60,
               "npk": {"N": "20-40 + inoculação", "P2O5": "60-100", "K2O": "60-100"},
               "micro": ["Molibdênio", "Zinco"],
               "producao": "1.5-3.5 t/ha", "obs": "Sensível ao Al³⁺. Inoculação com Rhizobium recomendada."},
    "Mandioca": {"ph_ideal": (5.5, 7.0), "ph_critico": 5.0, "v_ideal": 50,
                  "npk": {"N": "40-80", "P2O5": "40-80", "K2O": "60-120"},
                  "micro": ["Zinco", "Boro"],
                  "producao": "18-35 t/ha", "obs": "Cultura tolerante a solos ácidos e pobres. Boa opção para solos marginais."},
    "Eucalipto": {"ph_ideal": (5.0, 6.5), "ph_critico": 4.5, "v_ideal": 40,
                   "npk": {"N": "20-60", "P2O5": "40-80", "K2O": "40-80"},
                   "micro": ["Boro (1-2 kg/ha)", "Zinco"],
                   "producao": "30-50 m³/ha/ano", "obs": "Tolerante à acidez. Rotação de 6-7 anos."},
    "Pastagens": {"ph_ideal": (5.5, 6.5), "ph_critico": 5.0, "v_ideal": 50,
                   "npk": {"N": "40-120", "P2O5": "40-80", "K2O": "40-80"},
                   "micro": ["Zinco", "Enxofre (20-30 kg S/ha)"],
                   "producao": "8-20 t MS/ha/ano", "obs": "Braquiária (Urochloa) tolera solos ácidos e de baixa fertilidade."},
    "Citros": {"ph_ideal": (5.5, 7.0), "ph_critico": 5.3, "v_ideal": 60,
               "npk": {"N": "100-200", "P2O5": "40-80", "K2O": "100-180"},
               "micro": ["Zinco", "Boro", "Manganês", "Ferro"],
               "producao": "30-60 t/ha", "obs": "Cultura perene, sensível ao clorose de ferro em pH alto."},
    "Algodão": {"ph_ideal": (6.0, 6.8), "ph_critico": 5.8, "v_ideal": 60,
                "npk": {"N": "80-150", "P2O5": "60-120", "K2O": "80-120"},
                "micro": ["Boro (1,5-2 kg/ha)", "Zinco", "Molibdênio"],
                "producao": "3-5 t/ha algodão em caroço", "obs": "Muito exigente em Boro. Sensível ao déficit hídrico no florescimento."},
    "Trigo": {"ph_ideal": (5.5, 7.0), "ph_critico": 5.5, "v_ideal": 60,
              "npk": {"N": "60-120", "P2O5": "60-100", "K2O": "60-80"},
              "micro": ["Zinco", "Manganês", "Boro"],
              "producao": "3-6 t/ha", "obs": "Cultura de inverno. Sensível ao Al³⁺ e Mn²⁺ tóxico."}
}

# ═══════════════════════════════════════════════════════════════════════════
# SEÇÃO 3 – MAPEAMENTO DE BIOMAS BRASILEIROS POR COORDENADAS
# ═══════════════════════════════════════════════════════════════════════════

def detectar_bioma(lat, lon):
    """Detecta o bioma brasileiro mais provável com base nas coordenadas."""
    bioma = "Desconhecido"
    score = {}

    # Pantanal – bacia do Alto Paraguai
    if -22 <= lat <= -15 and -61 <= lon <= -55:
        score["Pantanal"] = 1.0
    # Amazônia
    if -12 <= lat <= 5 and -73 <= lon <= -47:
        score["Amazônia"] = 0.9
    # Caatinga – semiárido nordestino
    if -15 <= lat <= -3 and -45 <= lon <= -35:
        score["Caatinga"] = 0.9
    # Pampa – sul do Brasil
    if -34 <= lat <= -28 and -57 <= lon <= -49:
        score["Pampa"] = 1.0
    # Cerrado – Brasil Central
    if -24 <= lat <= -5 and -60 <= lon <= -43:
        if "Pantanal" not in score and "Amazônia" not in score:
            score["Cerrado"] = 0.85
        else:
            score["Cerrado"] = 0.5
    # Mata Atlântica – faixa costeira
    if -30 <= lat <= -5 and -50 <= lon <= -34:
        score["Mata Atlântica"] = 0.7

    if not score:
        if -35 <= lat <= 5 and -75 <= lon <= -28:
            bioma = "Brasil – bioma não determinado"
        else:
            bioma = "Fora do território brasileiro"
        return bioma, {}

    bioma = max(score, key=score.get)
    return bioma, score


# ═══════════════════════════════════════════════════════════════════════════
# SEÇÃO 4 – MODELO TENSORFLOW (MobileNetV2 Feature Extractor)
# ═══════════════════════════════════════════════════════════════════════════

@st.cache_resource(show_spinner=False)
def carregar_modelo_tf():
    """Carrega MobileNetV2 pré-treinado no ImageNet para extração de features."""
    if not TF_AVAILABLE:
        return None
    try:
        modelo = MobileNetV2(weights="imagenet", include_top=False, pooling="avg", input_shape=(224, 224, 3))
        return modelo
    except Exception:
        return None


def extrair_features_tf(imagem_pil, modelo):
    """Extrai vetor de features 1280-dim usando MobileNetV2."""
    if modelo is None:
        return None
    try:
        img = imagem_pil.resize((224, 224)).convert("RGB")
        arr = np.array(img, dtype=np.float32)[np.newaxis]
        arr = preprocess_input(arr)
        feats = modelo.predict(arr, verbose=0)[0]  # (1280,)
        return feats
    except Exception:
        return None


def score_textura_tf(features, tipo_solo):
    """
    Gera um score de textura [0-1] baseado nas features do TF.
    Usa projeções simples das features para estimar grossura de textura.
    """
    if features is None:
        return 0.5  # neutro quando TF não disponível
    # Proxy para textura: desvio padrão do vetor de features
    std = float(np.std(features))
    mean = float(np.mean(features))
    # Solos arenosos: features mais uniformes (baixo std)
    # Solos argilosos: features mais variadas (alto std)
    TEXTURA_SCORES = {
        "Latossolo Vermelho":         (0.6, 0.9),   # alta variância textural
        "Latossolo Vermelho-Amarelo":  (0.5, 0.8),
        "Latossolo Amarelo":           (0.5, 0.8),
        "Argissolo Vermelho-Amarelo":  (0.4, 0.7),
        "Nitossolo Vermelho":          (0.6, 0.9),
        "Neossolo Quartzarênico":      (0.1, 0.4),  # baixa variância
        "Cambissolo Háplico":          (0.3, 0.6),
        "Gleissolo Háplico":           (0.4, 0.7),
        "Planossolo Háplico":          (0.3, 0.6),
        "Vertissolo":                  (0.5, 0.8),
        "Chernossolo":                 (0.5, 0.8),
        "Espodossolo":                 (0.1, 0.4),
    }
    # Normalizar std para [0,1] usando valores típicos de MobileNetV2
    std_norm = min(1.0, std / 0.8)
    low, high = TEXTURA_SCORES.get(tipo_solo, (0.3, 0.7))
    mid = (low + high) / 2
    # Similaridade gaussiana entre std_norm e mid esperado
    score = float(np.exp(-0.5 * ((std_norm - mid) / 0.3) ** 2))
    return score


# ═══════════════════════════════════════════════════════════════════════════
# SEÇÃO 5 – ANÁLISE DE CORES E CLASSIFICAÇÃO MUNSELL
# ═══════════════════════════════════════════════════════════════════════════

def rgb_para_hsv(r, g, b):
    """Converte RGB (0-255) para HSV (H:0-360, S:0-100, V:0-100)."""
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return h * 360, s * 100, v * 100


def rgb_para_munsell(r, g, b):
    """Converte RGB para notação Munsell aproximada (critério Embrapa)."""
    h, lightness, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    hue_deg = h * 360
    lightness = lightness * 100
    s = s * 100

    # Munsell Value (V)
    if lightness < 10:
        val = "2.5"
    elif lightness < 25:
        val = "3.5"
    elif lightness < 40:
        val = "4.5"
    elif lightness < 55:
        val = "5.5"
    elif lightness < 70:
        val = "6.5"
    else:
        val = "7.5"

    # Munsell Chroma (C)
    if s < 10:
        chroma = "1"
    elif s < 20:
        chroma = "2"
    elif s < 30:
        chroma = "3"
    else:
        chroma = "4"

    # Munsell Hue
    if hue_deg < 8:
        munsell_hue = "10R"
    elif hue_deg < 18:
        munsell_hue = "2.5YR"
    elif hue_deg < 30:
        munsell_hue = "5YR"
    elif hue_deg < 42:
        munsell_hue = "7.5YR"
    elif hue_deg < 58:
        munsell_hue = "10YR"
    elif hue_deg < 75:
        munsell_hue = "2.5Y"
    elif hue_deg < 95:
        munsell_hue = "5Y"
    elif hue_deg < 135:
        munsell_hue = "5GY"
    elif hue_deg < 180:
        munsell_hue = "5G"
    elif hue_deg < 225:
        munsell_hue = "5BG"
    elif hue_deg < 270:
        munsell_hue = "5B"
    elif hue_deg < 315:
        munsell_hue = "5PB"
    else:
        munsell_hue = "10R"

    return f"{munsell_hue} {val}/{chroma}"


def corrigir_umidade(h, s, v, estado_umidade):
    """
    Ajusta HSV conforme estado de umidade.
    Solo úmido → cores mais escuras. Correção para equivalente ar-seco.
    """
    if estado_umidade == "Úmido":
        # Adicionar ~15% de valor (clarear) para estimar cor seca
        v_corr = min(100.0, v + 15.0)
        s_corr = max(0.0, s - 5.0)  # ligeiro dessaturado quando seco
        return h, s_corr, v_corr
    return h, s, v


def gauss_sim(x, mean, std):
    """Similaridade Gaussiana normalizada."""
    return float(np.exp(-0.5 * ((x - mean) / max(std, 1e-6)) ** 2))


def gauss_sim_circular(h, mean_h, std_h):
    """Similaridade Gaussiana para ângulo (circular), escala 0-360."""
    diff = abs(h - mean_h)
    diff = min(diff, 360 - diff)  # menor distância circular
    return float(np.exp(-0.5 * (diff / max(std_h, 1e-6)) ** 2))


def analisar_imagem(imagem_pil, n_clusters, metodo, estado_umidade):
    """
    Segmenta a imagem em clusters de cor dominantes.
    Retorna: cluster_centers (RGB), labels, proporções, HSV corrigido.
    """
    img = imagem_pil.convert("RGB").resize((200, 200), Image.LANCZOS)
    arr = np.array(img).reshape(-1, 3).astype(np.float64)

    if metodo == "Fuzzy C-Means" and FCM_AVAILABLE:
        modelo = FCM(n_clusters=n_clusters)
        modelo.fit(arr)
        labels = modelo.predict(arr)
        centers = modelo.centers
    else:
        modelo = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        modelo.fit(arr)
        labels = modelo.labels_
        centers = modelo.cluster_centers_

    # Proporção de pixels por cluster
    contagens = np.bincount(labels, minlength=n_clusters)
    proporcoes = contagens / contagens.sum()

    # HSV corrigido por umidade
    hsv_corrigido = []
    for c in centers:
        h, s, v = rgb_para_hsv(*c)
        h, s, v = corrigir_umidade(h, s, v, estado_umidade)
        hsv_corrigido.append((h, s, v))

    return centers, labels, proporcoes, hsv_corrigido


def classificar_solo(centers_rgb, proporcoes, hsv_corrigido, bioma, features_tf=None):
    """
    Classifica o tipo de solo com base em:
    - Similaridade de cor HSV (60% peso)
    - Features de textura TensorFlow (20% peso)
    - Contexto geográfico/bioma (20% peso)
    Retorna lista ordenada de (tipo_solo, score_percentual)
    """
    scores = {}

    for tipo, params in SOIL_HSV.items():
        score_cor = 0.0
        for (h, s, v), prop in zip(hsv_corrigido, proporcoes):
            sim_h = gauss_sim_circular(h, params["h_mean"], params["h_std"])
            sim_s = gauss_sim(s, params["s_mean"], params["s_std"])
            sim_v = gauss_sim(v, params["v_mean"], params["v_std"])
            score_cluster = (sim_h * 0.5 + sim_s * 0.3 + sim_v * 0.2)
            score_cor += score_cluster * prop

        # Score de textura TF
        score_tf = score_textura_tf(features_tf, tipo) if features_tf is not None else 0.5

        # Score geográfico/bioma
        biomas_solo = EMBRAPA_SOLOS.get(tipo, {}).get("biomas", [])
        score_geo = 1.2 if any(bioma in b or b in bioma for b in biomas_solo) else 0.8

        # Score final ponderado
        score_final = score_cor * 0.60 + score_tf * 0.20 + (score_geo - 1.0) * 0.20 + 0.5 * 0.20
        scores[tipo] = score_final

    # Normalizar para percentuais
    total = sum(scores.values())
    if total > 0:
        scores = {k: (v / total) * 100 for k, v in scores.items()}

    classificacao = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return classificacao


def criar_imagem_segmentada(imagem_pil, labels, centers, tamanho=(200, 200)):
    """Cria imagem segmentada com cores dos centroids."""
    arr = np.array(imagem_pil.convert("RGB").resize(tamanho, Image.LANCZOS))
    flat = arr.reshape(-1, 3)
    segmentada = centers[labels].reshape(tamanho[1], tamanho[0], 3).astype(np.uint8)
    return Image.fromarray(segmentada)


# ═══════════════════════════════════════════════════════════════════════════
# SEÇÃO 6 – MOTOR DE RECOMENDAÇÕES AGRÍCOLAS
# ═══════════════════════════════════════════════════════════════════════════

def calcular_correcoes_cultura(solo_tipo, cultura, estado_umidade):
    """Calcula correções específicas por cultura para o tipo de solo detectado."""
    if solo_tipo not in EMBRAPA_SOLOS:
        return {}
    if cultura not in CULTURAS_DB:
        return {}

    solo = EMBRAPA_SOLOS[solo_tipo]
    cult = CULTURAS_DB[cultura]

    ph_solo_min, ph_solo_max = solo["quimica"]["ph"]
    ph_solo_med = (ph_solo_min + ph_solo_max) / 2

    ph_ideal_min, ph_ideal_max = cult["ph_ideal"]
    ph_ideal_med = (ph_ideal_min + ph_ideal_max) / 2

    # Calagem estimada (t/ha de calcário PRNT 100%)
    if ph_solo_med < ph_ideal_min:
        deficit_ph = ph_ideal_min - ph_solo_med
        calagem = round(deficit_ph * 2.5, 1)  # regra empírica simplificada
        calagem_status = f"⚠️ Necessária: {calagem} t/ha de calcário dolomítico (PRNT 100%)"
    elif ph_solo_med > ph_ideal_max + 0.5:
        calagem_status = "⚠️ pH muito alto – evitar calagem; monitorar micronutrientes (Fe, Mn, Zn)"
    else:
        calagem_status = "✅ pH adequado para a cultura"

    # NPK
    npk = cult["npk"]

    # Micronutrientes
    micro = cult["micro"]

    # Observações extras por umidade
    obs_umidade = ""
    if estado_umidade == "Úmido":
        obs_umidade = " Solo úmido: adiar aplicação de calcário até solo secar. Risco de compactação – evitar tráfego pesado."

    return {
        "cultura": cultura,
        "ph_solo": f"{ph_solo_min:.1f} – {ph_solo_max:.1f}",
        "ph_ideal": f"{ph_ideal_min:.1f} – {ph_ideal_max:.1f}",
        "calagem": calagem_status,
        "npk": npk,
        "micronutrientes": micro,
        "producao_esperada": cult["producao"],
        "observacoes": cult["obs"] + obs_umidade,
    }


def obter_cultivos_recomendados(solo_tipo):
    """Retorna cultivos ordenados por viabilidade para o tipo de solo."""
    if solo_tipo not in EMBRAPA_SOLOS:
        return {}
    ordem = {"Muito Alta": 5, "Alta": 4, "Média": 3, "Baixa": 2, "Muito Baixa": 1}
    cultivos = EMBRAPA_SOLOS[solo_tipo]["cultivos"]
    return dict(sorted(cultivos.items(), key=lambda x: ordem.get(x[1], 0), reverse=True))


# ═══════════════════════════════════════════════════════════════════════════
# SEÇÃO 7 – VISUALIZAÇÕES
# ═══════════════════════════════════════════════════════════════════════════

def plotar_distribuicao_cores(centers_rgb, proporcoes, munsell_labels):
    """Gráfico de barras das cores dominantes."""
    cores_hex = [f"rgb({int(c[0])},{int(c[1])},{int(c[2])})" for c in centers_rgb]
    labels = [f"{m}<br>{p*100:.1f}%" for m, p in zip(munsell_labels, proporcoes)]
    fig = go.Figure(go.Bar(
        x=labels,
        y=proporcoes * 100,
        marker_color=cores_hex,
        marker_line_color="rgba(0,0,0,0.3)",
        marker_line_width=1.5,
        text=[f"{p*100:.1f}%" for p in proporcoes],
        textposition="outside"
    ))
    fig.update_layout(
        title="Distribuição das Cores Dominantes (Munsell)",
        xaxis_title="Cor Munsell",
        yaxis_title="Proporção (%)",
        yaxis_range=[0, max(proporcoes) * 120],
        plot_bgcolor="#f8f9fa",
        height=380
    )
    return fig


def plotar_composicao(comp_dict, solo_nome):
    """Gráfico de pizza da composição granulométrica estimada."""
    nomes = ["Argila", "Silte", "Areia", "Matéria Orgânica"]
    chaves = ["argila", "silte", "areia", "materia_organica"]
    cores = ["#c0392b", "#e67e22", "#f1c40f", "#27ae60"]
    valores = []
    for k in chaves:
        rng = comp_dict.get(k, (0, 0))
        valores.append((rng[0] + rng[1]) / 2)

    fig = go.Figure(go.Pie(
        labels=nomes,
        values=valores,
        marker_colors=cores,
        hole=0.4,
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>%{percent}<extra></extra>"
    ))
    fig.update_layout(
        title=f"Composição Estimada – {solo_nome}",
        annotations=[dict(text="Solo", x=0.5, y=0.5, font_size=16, showarrow=False)],
        height=380
    )
    return fig


def plotar_classificacao_barras(classificacao_top3):
    """Barras horizontais das probabilidades de classificação."""
    nomes = [c[0] for c in classificacao_top3]
    scores = [c[1] for c in classificacao_top3]
    cores_barras = ["#e74c3c", "#e67e22", "#3498db"]
    fig = go.Figure(go.Bar(
        y=nomes,
        x=scores,
        orientation="h",
        marker_color=cores_barras[:len(nomes)],
        text=[f"{s:.1f}%" for s in scores],
        textposition="outside"
    ))
    fig.update_layout(
        title="Probabilidade de Classificação (Top 3)",
        xaxis_title="Probabilidade (%)",
        xaxis_range=[0, max(scores) * 1.25],
        plot_bgcolor="#f8f9fa",
        height=280
    )
    return fig


def plotar_mapa(lat, lon, bioma):
    """Mapa interativo com OpenStreetMap mostrando o ponto de coleta."""
    fig = go.Figure(go.Scattermapbox(
        lat=[lat],
        lon=[lon],
        mode="markers+text",
        marker=go.scattermapbox.Marker(size=18, color="#e74c3c"),
        text=["Ponto de Coleta"],
        textposition="top right",
        hovertemplate=f"<b>Ponto de Coleta</b><br>Lat: {lat:.4f}<br>Lon: {lon:.4f}<br>Bioma: {bioma}<extra></extra>"
    ))
    fig.update_layout(
        mapbox_style="open-street-map",
        mapbox=dict(center=dict(lat=lat, lon=lon), zoom=7),
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        height=420,
        title=f"Localização da Coleta – Bioma: {bioma}"
    )
    return fig


# ═══════════════════════════════════════════════════════════════════════════
# SEÇÃO 8 – INTERFACE STREAMLIT
# ═══════════════════════════════════════════════════════════════════════════

def main():
    st.set_page_config(
        page_title="Classificador de Solos EMBRAPA",
        page_icon="🌱",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # ── CSS customizado ──────────────────────────────────────────────────
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1a5c2a 0%, #2d8a45 50%, #8B4513 100%);
        color: white; padding: 1.5rem 2rem; border-radius: 12px; margin-bottom: 1.5rem;
    }
    .main-header h1 { color: white !important; margin: 0; font-size: 1.8rem; }
    .main-header p { color: #c8e6c9; margin: 0.3rem 0 0 0; font-size: 0.95rem; }
    .soil-card {
        background: #fff; border-left: 5px solid #e74c3c; border-radius: 8px;
        padding: 1rem 1.2rem; margin: 0.5rem 0; box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    .soil-card.rank2 { border-left-color: #e67e22; }
    .soil-card.rank3 { border-left-color: #3498db; }
    .metric-box {
        background: #f8f9fa; border-radius: 8px; padding: 0.8rem;
        text-align: center; border: 1px solid #dee2e6;
    }
    .badge-alta { background: #27ae60; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; }
    .badge-media { background: #f39c12; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; }
    .badge-baixa { background: #e74c3c; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; }
    .badge-muito-alta { background: #1a5c2a; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8rem; }
    </style>
    """, unsafe_allow_html=True)

    # ── Cabeçalho ────────────────────────────────────────────────────────
    st.markdown("""
    <div class="main-header">
        <h1>🌱 Sistema EMBRAPA de Classificação de Solos</h1>
        <p>Análise por imagem com TensorFlow · Critérios SiBCS · Recomendações Agrícolas</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar ───────────────────────────────────────────────────────────
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/EMBRAPA_logo.svg/200px-EMBRAPA_logo.svg.png",
                 width=140)
        st.markdown("---")
        st.header("⚙️ Parâmetros de Análise")

        uploaded = st.file_uploader(
            "📤 Imagem do Solo",
            type=["jpg", "jpeg", "png", "webp"],
            help="Foto da amostra de solo (câmera, laboratório, campo)"
        )

        st.markdown("### 📍 Coordenadas da Coleta")
        col_lat, col_lon = st.columns(2)
        with col_lat:
            lat = st.number_input("Latitude", min_value=-35.0, max_value=5.0,
                                  value=-15.8, step=0.001, format="%.4f",
                                  help="Latitude em graus decimais (Brasil: -35 a +5)")
        with col_lon:
            lon = st.number_input("Longitude", min_value=-75.0, max_value=-28.0,
                                  value=-47.9, step=0.001, format="%.4f",
                                  help="Longitude em graus decimais (Brasil: -75 a -28)")

        st.markdown("### 💧 Estado de Umidade")
        estado_umidade = st.radio(
            "O solo está:",
            ["Seco (ar-seco)", "Úmido"],
            help="Solo úmido apresenta cores mais escuras. O sistema aplica correção automática."
        )

        st.markdown("### 🔬 Configurações do Algoritmo")
        n_clusters = st.slider("Número de clusters (cores)", 2, 8, 4,
                               help="Quantidade de cores dominantes a detectar")
        metodo = st.selectbox(
            "Método de clusterização",
            ["K-Means"] + (["Fuzzy C-Means"] if FCM_AVAILABLE else []),
            help="Fuzzy C-Means disponível apenas se a biblioteca fcmeans estiver instalada"
        )

        st.markdown("---")
        analisar = st.button("🔬 Analisar Solo", type="primary", use_container_width=True)

        # Status das dependências
        st.markdown("---")
        st.caption("**Status das dependências:**")
        st.caption(f"{'✅' if TF_AVAILABLE else '⚠️'} TensorFlow: {'Ativo' if TF_AVAILABLE else 'Não instalado (modo cor)'}")
        st.caption(f"{'✅' if FCM_AVAILABLE else '⚠️'} Fuzzy C-Means: {'Ativo' if FCM_AVAILABLE else 'Não instalado'}")

    # ── Área principal ────────────────────────────────────────────────────
    if uploaded is None:
        # Tela de boas-vindas
        c1, c2, c3 = st.columns(3)
        with c1:
            st.info("**1. Faça upload** da imagem do solo na barra lateral.")
        with c2:
            st.info("**2. Informe** as coordenadas e estado de umidade.")
        with c3:
            st.info("**3. Clique em Analisar** para obter o laudo completo.")

        st.markdown("---")
        st.subheader("📋 Tipos de Solo Classificados (EMBRAPA SiBCS)")
        df_solos = pd.DataFrame([
            {"Tipo de Solo": k, "Código": v["codigo"], "Biomas": ", ".join(v["biomas"]),
             "Área no Brasil": v["area_brasil"],
             "pH Típico": f"{v['quimica']['ph'][0]}-{v['quimica']['ph'][1]}"}
            for k, v in EMBRAPA_SOLOS.items()
        ])
        st.dataframe(df_solos, use_container_width=True, hide_index=True)
        return

    # ── Carregar imagem e modelo ──────────────────────────────────────────
    imagem = Image.open(uploaded).convert("RGB")

    if analisar:
        bioma, score_biomas = detectar_bioma(lat, lon)

        with st.spinner("🔄 Carregando modelo TensorFlow..."):
            modelo_tf = carregar_modelo_tf()

        with st.spinner("🎨 Analisando cores e texturas..."):
            centers, labels, proporcoes, hsv_corrigido = analisar_imagem(
                imagem, n_clusters, metodo, estado_umidade
            )
            munsell_labels = [rgb_para_munsell(*c) for c in centers]

        with st.spinner("🧠 Extraindo features com TensorFlow..."):
            features_tf = extrair_features_tf(imagem, modelo_tf)

        with st.spinner("📊 Classificando tipo de solo..."):
            classificacao = classificar_solo(centers, proporcoes, hsv_corrigido, bioma, features_tf)
            top3 = classificacao[:3]

        solo_principal = top3[0][0]
        img_seg = criar_imagem_segmentada(imagem, labels, centers.astype(np.uint8))

        # ── Resumo rápido no topo ─────────────────────────────────────────
        st.success(f"✅ Análise concluída! Solo mais provável: **{solo_principal}** "
                   f"({EMBRAPA_SOLOS[solo_principal]['codigo']}) — "
                   f"Confiança: **{top3[0][1]:.1f}%**")

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Solo Identificado", f"{EMBRAPA_SOLOS[solo_principal]['codigo']}", solo_principal)
        col_m2.metric("Bioma Detectado", bioma)
        ph_min, ph_max = EMBRAPA_SOLOS[solo_principal]["quimica"]["ph"]
        col_m3.metric("pH Estimado", f"{ph_min:.1f} – {ph_max:.1f}")
        col_m4.metric("Umidade da Amostra", estado_umidade.split(" ")[0])

        st.markdown("---")

        # ── Tabs de resultados ────────────────────────────────────────────
        tabs = st.tabs([
            "🔬 Análise Visual",
            "🏔️ Classificação EMBRAPA",
            "⚗️ Composição do Solo",
            "🌱 Recomendações Agrícolas",
            "📍 Localização & Bioma"
        ])

        # ─── Tab 1: Análise Visual ─────────────────────────────────────
        with tabs[0]:
            st.subheader("Análise Visual da Imagem de Solo")
            col_img1, col_img2 = st.columns(2)
            with col_img1:
                st.image(imagem, caption="📷 Imagem Original", use_container_width=True)
            with col_img2:
                st.image(img_seg, caption=f"🎨 Segmentada ({metodo}, {n_clusters} clusters)",
                         use_container_width=True)

            st.markdown("### 🎨 Cores Munsell Detectadas")
            cols_cores = st.columns(n_clusters)
            for i, (center, munsell, prop) in enumerate(zip(centers, munsell_labels, proporcoes)):
                r, g, b = int(center[0]), int(center[1]), int(center[2])
                with cols_cores[i]:
                    st.markdown(
                        f"""<div style="background:rgb({r},{g},{b});height:60px;border-radius:8px;
                        border:2px solid #ccc;margin-bottom:6px;"></div>""",
                        unsafe_allow_html=True
                    )
                    st.caption(f"**{munsell}**")
                    st.caption(f"RGB: ({r},{g},{b})")
                    st.caption(f"Proporção: {prop*100:.1f}%")
                    h, s, v = hsv_corrigido[i]
                    st.caption(f"HSV: ({h:.0f}°, {s:.0f}%, {v:.0f}%)")
                    if estado_umidade == "Úmido":
                        st.caption("🔄 *Corrigido p/ seco*")

            st.plotly_chart(
                plotar_distribuicao_cores(centers, proporcoes, munsell_labels),
                use_container_width=True
            )

            if TF_AVAILABLE and features_tf is not None:
                st.success(f"🧠 TensorFlow MobileNetV2 extraiu **1.280 features** de textura da imagem. "
                           f"Desvio padrão das features: {np.std(features_tf):.4f} | "
                           f"Média: {np.mean(features_tf):.4f}")
            else:
                st.warning("⚠️ TensorFlow não disponível. Classificação baseada apenas em análise de cores.")

        # ─── Tab 2: Classificação EMBRAPA ─────────────────────────────
        with tabs[1]:
            st.subheader("Classificação segundo EMBRAPA SiBCS")
            st.plotly_chart(plotar_classificacao_barras(top3), use_container_width=True)

            for i, (tipo, score) in enumerate(top3):
                rank_class = ["", "rank2", "rank3"][i]
                rank_emoji = ["🥇", "🥈", "🥉"][i]
                info = EMBRAPA_SOLOS.get(tipo, {})

                with st.expander(f"{rank_emoji} {tipo} ({info.get('codigo','')}) — {score:.1f}% de probabilidade",
                                 expanded=(i == 0)):
                    c_a, c_b = st.columns([2, 1])
                    with c_a:
                        st.markdown(f"**Descrição:** {info.get('descricao','')}")
                        st.markdown(f"**Ocorrência no Brasil:** {info.get('area_brasil','')}")
                        st.markdown(f"**Biomas:** {', '.join(info.get('biomas',[]))}")
                        st.markdown(f"**Drenagem:** {info.get('drenagem','')}")
                        st.markdown(f"**Erodibilidade:** {info.get('erodibilidade','')}")
                    with c_b:
                        quim = info.get("quimica", {})
                        st.markdown("**Química do Solo:**")
                        st.markdown(f"- pH: {quim.get('ph','')}")
                        st.markdown(f"- CTC: {quim.get('ctc','')}")
                        st.markdown(f"- Sat. Bases: {quim.get('sat_bases','')}")
                        st.markdown(f"- Sat. Al³⁺: {quim.get('sat_aluminio','')}")

                    st.markdown("**Correções Gerais Recomendadas:**")
                    corr = info.get("correcao", {})
                    for chave, valor in corr.items():
                        icone = {"calagem": "🪨", "fosfatagem": "💊", "adubacao_npk": "🧪",
                                 "micronutrientes": "⚗️", "materia_organica": "🌿",
                                 "gessagem": "🔩", "drenagem": "💧", "irrigacao": "🚿",
                                 "manejo_erosao": "⛰️", "manejo_fisico": "🚜",
                                 "observacoes": "📌"}.get(chave, "•")
                        chave_fmt = chave.replace("_", " ").title()
                        st.markdown(f"{icone} **{chave_fmt}:** {valor}")

        # ─── Tab 3: Composição ─────────────────────────────────────────
        with tabs[2]:
            st.subheader("Composição Estimada do Solo")
            info_principal = EMBRAPA_SOLOS.get(solo_principal, {})
            comp = info_principal.get("composicao", {})

            st.plotly_chart(plotar_composicao(comp, solo_principal), use_container_width=True)

            st.markdown("### 📊 Faixas Típicas de Composição")
            dados_comp = []
            for comp_nome, (vmin, vmax) in comp.items():
                dados_comp.append({
                    "Componente": comp_nome.replace("_", " ").title(),
                    "Mínimo (%)": f"{vmin:.0f}",
                    "Máximo (%)": f"{vmax:.0f}",
                    "Média estimada (%)": f"{(vmin+vmax)/2:.0f}"
                })
            st.dataframe(pd.DataFrame(dados_comp), use_container_width=True, hide_index=True)

            st.markdown("### 🧪 Propriedades Químicas Estimadas")
            quim = info_principal.get("quimica", {})
            cc1, cc2 = st.columns(2)
            with cc1:
                ph_min, ph_max = quim.get("ph", (0, 0))
                st.metric("pH estimado (H₂O)", f"{ph_min:.1f} – {ph_max:.1f}")
                st.metric("CTC", quim.get("ctc", "—"))
            with cc2:
                st.metric("Saturação por Bases (V%)", quim.get("sat_bases", "—"))
                st.metric("Saturação por Al³⁺", quim.get("sat_aluminio", "—"))

            # Comparação top 3
            st.markdown("### 🔄 Comparação de Composição – Top 3 Classificações")
            comp_data = []
            for tipo, _ in top3:
                info_t = EMBRAPA_SOLOS.get(tipo, {})
                c_t = info_t.get("composicao", {})
                row = {"Solo": tipo}
                for k, (mn, mx) in c_t.items():
                    row[k.replace("_", " ").title()] = f"{mn}-{mx}%"
                comp_data.append(row)
            if comp_data:
                st.dataframe(pd.DataFrame(comp_data), use_container_width=True, hide_index=True)

        # ─── Tab 4: Recomendações Agrícolas ───────────────────────────
        with tabs[3]:
            st.subheader(f"Recomendações Agrícolas para: {solo_principal}")

            cultivos_ord = obter_cultivos_recomendados(solo_principal)
            if cultivos_ord:
                st.markdown("### 🌾 Culturas Recomendadas (por viabilidade)")
                badge_map = {
                    "Muito Alta": "badge-muito-alta",
                    "Alta": "badge-alta",
                    "Média": "badge-media",
                    "Baixa": "badge-baixa"
                }
                html_cultivos = "<div style='display:flex;flex-wrap:wrap;gap:8px;margin-bottom:1rem;'>"
                for cult, viab in cultivos_ord.items():
                    badge_cls = badge_map.get(viab, "badge-baixa")
                    html_cultivos += f"""<div style='padding:6px 12px;background:#f8f9fa;
                        border-radius:8px;border:1px solid #dee2e6;'>
                        <strong>{cult}</strong>
                        <span class='{badge_cls}' style='margin-left:6px;'>{viab}</span></div>"""
                html_cultivos += "</div>"
                st.markdown(html_cultivos, unsafe_allow_html=True)

            st.markdown("### 📋 Laudo Técnico por Cultura")
            culturas_disponiveis = [c for c in cultivos_ord.keys() if c in CULTURAS_DB]
            if not culturas_disponiveis:
                culturas_disponiveis = list(CULTURAS_DB.keys())

            cultura_sel = st.selectbox("Selecione a cultura para o laudo:", culturas_disponiveis)

            if cultura_sel:
                laudo = calcular_correcoes_cultura(solo_principal, cultura_sel, estado_umidade)
                if laudo:
                    lc1, lc2 = st.columns(2)
                    with lc1:
                        st.markdown("**📊 pH:**")
                        st.markdown(f"- pH do Solo Estimado: **{laudo['ph_solo']}**")
                        st.markdown(f"- pH Ideal para {cultura_sel}: **{laudo['ph_ideal']}**")
                        st.markdown(f"- Status de Calagem: {laudo['calagem']}")
                        st.markdown(f"- Produção Esperada: 🎯 {laudo['producao_esperada']}")
                    with lc2:
                        st.markdown("**🧪 Adubação NPK recomendada (kg/ha):**")
                        for elem, dose in laudo["npk"].items():
                            st.markdown(f"- **{elem}:** {dose} kg/ha")
                        st.markdown("**⚗️ Micronutrientes:**")
                        for micro in laudo["micronutrientes"]:
                            st.markdown(f"- {micro}")

                    st.info(f"📌 **Observações:** {laudo['observacoes']}")

            # Correções gerais do solo
            st.markdown("### 🪨 Programa de Correção Geral do Solo")
            corr_geral = EMBRAPA_SOLOS.get(solo_principal, {}).get("correcao", {})
            for chave, valor in corr_geral.items():
                icone_map = {
                    "calagem": "🪨 **Calagem:**",
                    "fosfatagem": "💊 **Fosfatagem:**",
                    "adubacao_npk": "🧪 **Adubação NPK:**",
                    "micronutrientes": "⚗️ **Micronutrientes:**",
                    "materia_organica": "🌿 **Matéria Orgânica:**",
                    "gessagem": "🔩 **Gessagem:**",
                    "drenagem": "💧 **Drenagem:**",
                    "irrigacao": "🚿 **Irrigação:**",
                    "manejo_erosao": "⛰️ **Manejo Anti-Erosão:**",
                    "manejo_fisico": "🚜 **Manejo Físico:**",
                    "observacoes": "📌 **Observações:**"
                }
                label = icone_map.get(chave, f"• **{chave.replace('_',' ').title()}:**")
                st.markdown(f"{label} {valor}")

        # ─── Tab 5: Localização & Bioma ────────────────────────────────
        with tabs[4]:
            st.subheader("Localização da Coleta & Contexto de Bioma")

            lc1, lc2 = st.columns([3, 2])
            with lc1:
                st.plotly_chart(plotar_mapa(lat, lon, bioma), use_container_width=True)
            with lc2:
                st.markdown(f"### 🌿 Bioma Detectado: **{bioma}**")
                st.markdown(f"**Coordenadas:** {lat:.4f}°, {lon:.4f}°")

                if score_biomas:
                    st.markdown("**Probabilidade por bioma:**")
                    for b, sc in sorted(score_biomas.items(), key=lambda x: -x[1]):
                        st.progress(sc, text=f"{b}: {sc*100:.0f}%")

                # Solos típicos do bioma
                solos_bioma = [
                    (k, v["codigo"]) for k, v in EMBRAPA_SOLOS.items()
                    if any(bioma in bi or bi in bioma for bi in v.get("biomas", []))
                ]
                if solos_bioma:
                    st.markdown(f"**Solos típicos do {bioma}:**")
                    for nome, cod in solos_bioma:
                        st.markdown(f"- {cod}: {nome}")

                # Contexto agronômico do bioma
                ctx_bioma = {
                    "Cerrado": "🌾 Maior fronteira agrícola do Brasil. Alto potencial para grãos (soja, milho). Requer correção intensiva de acidez.",
                    "Amazônia": "🌳 Solos de baixa fertilidade natural. Foco em sistemas agroflorestais. Alta sensibilidade ambiental.",
                    "Caatinga": "🌵 Semiárido. Irregularidade pluviométrica. Foco em culturas adaptadas à seca (mandioca, palma, caju).",
                    "Mata Atlântica": "🌿 Solos variados. Alta pressão antrópica. Foco em fruticultura, horticultura e café.",
                    "Pampa": "🐄 Campos subtropicais. Arroz irrigado e pecuária. Solo com bom potencial para culturas de inverno.",
                    "Pantanal": "🦜 Planície de inundação. Limitações por encharcamento. Pecuária extensiva predominante."
                }
                ctx = ctx_bioma.get(bioma, "")
                if ctx:
                    st.info(ctx)

    else:
        # Mostrar imagem prévia antes da análise
        col_prev, col_info = st.columns([1, 1])
        with col_prev:
            st.image(imagem, caption="📷 Imagem carregada – Clique em 'Analisar Solo' para processar",
                     use_container_width=True)
        with col_info:
            st.markdown("### 📋 Resumo dos Parâmetros")
            st.markdown(f"- **Arquivo:** {uploaded.name}")
            st.markdown(f"- **Tamanho:** {imagem.size[0]} × {imagem.size[1]} px")
            st.markdown(f"- **Coordenadas:** {lat:.4f}°, {lon:.4f}°")
            bioma_prev, _ = detectar_bioma(lat, lon)
            st.markdown(f"- **Bioma estimado:** {bioma_prev}")
            st.markdown(f"- **Umidade:** {estado_umidade}")
            st.markdown(f"- **Clusters:** {n_clusters} | **Método:** {metodo}")
            st.info("👆 Ajuste os parâmetros na barra lateral e clique em **🔬 Analisar Solo**")

    # ── Rodapé ────────────────────────────────────────────────────────────
    st.markdown("---")
    with st.expander("ℹ️ Sobre o Sistema"):
        st.markdown("""
        **Sistema EMBRAPA de Classificação de Solos por Imagem**

        Este sistema utiliza:
        - **TensorFlow MobileNetV2** (pré-treinado ImageNet) para extração de features de textura
        - **K-Means / Fuzzy C-Means** para segmentação de cores dominantes
        - **Notação Munsell** para caracterização de cor seguindo critérios EMBRAPA
        - **SiBCS** (Sistema Brasileiro de Classificação de Solos) da EMBRAPA
        - Correção automática de umidade (solo úmido → conversão para equivalente ar-seco)
        - Geolocalização por bioma para contexto agronômico regional

        **Referências:**
        - EMBRAPA. Sistema Brasileiro de Classificação de Solos, 3ª ed. Brasília, 2013.
        - Munsell Soil Color Charts. Grand Rapids: X-Rite, 2009.
        - Santos et al. Manual de Descrição e Coleta de Solo no Campo. EMBRAPA, 2015.

        **Desenvolvido por:** Professor Marcelo Claro | marceloclaro@gmail.com
        """)


if __name__ == "__main__":
    main()
