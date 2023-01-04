import streamlit as st
import colorsys
from sklearn.cluster import KMeans
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2

st.title('CLASSIFICADOR DE COR DE SOLO - MUNSELL')

tipo_solo = st.sidebar.radio('Escolha o tipo de solo', ('Úmido', 'Seco'))

# Pergunte ao usuário para fazer o upload da imagem da amostra de solo
imagem_file = st.file_uploader('Selecione a imagem da amostra de solo', type='jpg')

st.markdown('O solo é uma camada fina e complexa da Terra que sustenta a vida vegetal e muitos outros organismos. Ele é composto de minerais, matéria orgânica, água e ar, e é responsável por fornecer nutrientes e água para as plantas. A cor do solo é importante para o estudo geográfico porque pode indicar o tipo e a quantidade de nutrientes presentes no solo, bem como o pH e a capacidade de retenção de água.')

def converte_munsell(r, g, b):
  # Converte os valores RGB em matiz, saturação e valor (HSV)
  matiz, saturacao, valor = cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2HSV)[0][0]
    
def converte_munsell(r, g, b):
  # Converte os valores RGB em matiz, saturação e valor (HSV)
  matiz, saturacao, valor = cv2.cvtColor(np.uint8([[[b, g, r]]]), cv2.COLOR_BGR2HSV)[0][0]

  # Mapeia os valores de matiz, saturação e valor resultantes para a tonalidade, o valor e o croma Munsell correspondentes mais próximos
  tonalidades = ['R', 'YR', 'Y', 'GY', 'G', 'BG', 'B', 'PB', 'P', 'RP']
  valores = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
  cromas = ['1/8', '1/4', '3/8', '1/2', '5/8', '3/4', '7/8', '1', '1 1/8', '1 1/4', '1 3/8', '1 1/2', '1 5/8', '1 3/4', '1 7/8', '2']
  tonalidade_munsell = tonalidades[int(matiz / 30)]
  valor_munsell = valores[int((valor / 255) * 10)]
  croma_munsell = cromas[int((saturacao / 255) * 16)]

  # Retorna a cor Munsell resultante
  return tonalidade_munsell

def classifica_cor_solo(imagem, largura, altura, num_clusters):
  # Redimensiona a imagem
  imagem = cv2.resize(imagem, (largura, altura))

  # Executa o clustering K-Means na imagem
  imagem = np.float32(imagem)
  criterio = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
  num_cores, labels, (centers) = cv2.kmeans(imagem, num_clusters, None, criterio, 10, cv2.KMEANS_RANDOM_CENTERS)

  # Conta o número de pixels em cada cluster
  contador_cores = np.zeros(num_clusters)
  for label in labels:
    contador_cores[label] += 1

  # Converte os valores RGB dos centros de cluster em cores Munsell
  cores = []
  for center in centers:
    r, g, b = center
    cores.append(converte_munsell(r, g, b))

  # Calcula as porcentagens de pixels em cada cor classificada
  porcentagens = []
  for contador in contador_cores:
    porcentagem = (contador / len(labels)) * 100
    porcentagens.append(porcentagem)

  # Retorna um dicionário com as porcentagens de pixels em cada cor classificada
  resultado = dict(zip(cores, porcentagens))
  return resultado

if tipo_solo == 'Úmido' and imagem_file is not None:
  # Lê a imagem da amostra de solo úmida
  imagem = cv2.imread(imagem_file)

  # Classifica a cor do solo úmido e obtém o resultado em um dicionário
  resultado = classifica_cor_solo(imagem, largura, altura, num_clusters)

 if tipo_solo == 'Úmido' and imagem_file is not None:
  # Lê a imagem da amostra de solo úmida
  imagem = cv2.imread(imagem_file)

  # Classifica a cor do solo úmido e obtém o resultado em um dicionário
  resultado = classifica_cor_solo(imagem, largura, altura, num_clusters)

  # Obtém as cores classificadas e as porcentagens de pixels em cada cor
  cores = list(resultado.keys())
  porcentagens = list(resultado.values())

  # Cria o gráfico de margem de erro e variância
  plt.figure()
  plt.title('Classificação de cor de solo - Munsell')
  plt.xlabel('Cores')
  plt.ylabel('Porcentagem de pixels')
  plt.errorbar(cores, porcentagens, fmt='o', ecolor='k')
  plt.xticks(rotation=90)
  plt.ylim(0, max(porcentagens) + 5)
  plt.tight_layout()

  # Exibe o gráfico no Streamlit
  st.pyplot()

 elif tipo_solo == 'Seco' and imagem_file is not None:
  # Lê a imagem da amostra de solo seco
  imagem = cv2.imread(imagem_file)

  # Classifica a cor do solo seco e obtém o resultado em um dicionário
  resultado = classifica_cor_solo(imagem, largura, altura, num_clusters)

  # Obtém as cores classificadas e as porcentagens de pixels em cada cor
  cores = list(resultado.keys())
  porcentagens = list(resultado.values())

  # Cria o gráfico de margem de erro e variância
  plt.figure()
  plt.title('Classificação de cores do solo seco')
plt.bar(cores, porcentagens, yerr=resultado['variancias'], capsize=10)
plt.ylabel('Porcentagem de pixels')
plt.xticks(rotation=45)

 
