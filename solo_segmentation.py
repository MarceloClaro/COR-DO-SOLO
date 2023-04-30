#replace the script's seaborn library with matplotlib
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

import numpy as np
import cv2
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans
import colorsys

# Define the function to convert RGB to Munsell
def rgb_to_munsell(r, g, b):
    h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0)
    h = h*360
    if h < 20:
        hue = "R"
    elif h < 40:
        hue = "YR"
    elif h < 75:
        hue = "Y"
    elif h < 155:
        hue = "GY"
    elif h < 190:
        hue = "G"
    elif h < 260:
        hue = "BG"
    elif h < 290:
        hue = "B"
    elif h < 335:
        hue = "PB"
    else:
        hue = "P"
    if l < 0.25:
        value = "2.5"
    elif l < 0.3:
        value = "3"
    elif l < 0.4:
        value = "4"
    elif l < 0.5:
        value = "5"
    elif l < 0.6:
        value = "6"
    elif l < 0.7:
        value = "7"
    elif l < 0.8:
        value = "8"
    else:
        value = "10"
    if s < 0.1:
        chroma = "0"
    elif s < 0.2:
        chroma = "1"
    elif s < 0.3:
        chroma = "2"
    elif s < 0.4:
        chroma = "3"
    elif s < 0.5:
        chroma = "4"
    elif s < 0.6:
        chroma = "5"
    elif s < 0.7:
        chroma = "6"
    elif s < 0.8:
        chroma = "7"
    elif s < 0.9:
        chroma = "8"
    elif s < 1.0:
        chroma = "9"
    else:
        chroma = "0"

    return value + hue + "/" + chroma

# Load and show the image
st.title("Classificação de Solo")
uploaded_file = st.file_uploader("Escolha a imagem", type="jpg")
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagem', use_column_width=True)
    img = cv2.imread(uploaded_file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.show()

    
    # Reshape the image to a list of pixels
    Z = img.reshape((-1,3))
    Z = np.float32(Z)

    # Define the criteria, number of clusters(K) and apply k-means()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 1
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)

    # Convert the image to 8-bit values
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))

    # Display the image and the corresponding Munsell notation
    plt.imshow(res2)
    plt.title(rgb_to_munsell(center[0][0], center[0][1], center[0][2]))
    st.pyplot()

    soil_dict = {
        "7.5YR5/4": "Argissolo Vermelho-Amarelo - Bahia .",
        "10YR3/3": "Neossolo Regolítico - Pernambuco - .",
        "2.5YR5/4": "Cambissolo Háplico - Rio Grande do Norte -",
        "7R/0": "Luvissolo Crômico - Paraíba - ",
        
    }     

    munsell_notation = rgb_to_munsell(center[0][0], center[0][1], center[0][2])
    soil_type = soil_dict.get(munsell_notation, "NÃO CADASTRADO")


    st.write("Tipo de solo correspondente:")
    st.write(soil_type)

    # Run your Streamlit app
if __name__ == '__main__':
    app()
