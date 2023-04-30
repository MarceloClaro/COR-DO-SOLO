import streamlit as st
import pandas as pd
import numpy as np
import cv2
import colorsys
from sklearn.cluster import KMeans

def rgb_to_munsell(center, col_c):
    r, g, b = center[0][0], center[0][1], center[0][2]
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    h = h * 360

    hue_table = {20: "R", 40: "YR", 75: "Y", 155: "GY", 190: "G", 260: "BG", 290: "B", 335: "PB"}
    hue = next((v for k, v in hue_table.items() if h < k), "P")

    lightness_table = {0.25: "2.5", 0.3: "3", 0.4: "4", 0.5: "5", 0.6: "6", 0.7: "7", 0.8: "8"}
    value = next((v for k, v in lightness_table.items() if l < k), "10")

    saturation_table = {0.1: "0", 0.2: "1", 0.3: "2", 0.4: "3", 0.5: "4", 0.6: "5", 0.7: "6", 0.8: "7", 0.9: "8"}
    chroma = next((v for k, v in saturation_table.items() if s < k), "0")

    col_c.title('Valores para RGB')
    col_c.write(f'{r}, {g}, {b}')
    st.write(f'Munsell: {hue}{value}/{chroma}')

def main():
    st.title("Conversão RGB para Munsell")
    st.write("Insira uma imagem para converter as cores para o sistema Munsell")
    uploaded_file = st.file_uploader("Selecione um arquivo de imagem", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8
