import streamlit as st
import pandas as pd
import numpy as np
import cv2
import colorsys
from sklearn.cluster import KMeans

def rgb_to_munsell(rgb):
    r, g, b = rgb[0], rgb[1], rgb[2]
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
        chroma = "0.5"
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
    else:
        chroma = "9"
    return f"{hue}{value}/{chroma}"

def main():
    st.title("Image Segmentation with k-Means Clustering")
    st.write("Enter the file path for the image:")
    file_path = st.text_input("Image file path:", "image.jpg")
    image = cv2.imread(file_path)
    st.write("Enter the value of k for k-means clustering:")
    k = st.number_input("k:", value=3, min_value=1, max_value=10)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.reshape((image.shape[0] * image.shape[1], 3))
    kmeans = KMeans(n_clusters=k)
    labels = kmeans.fit_predict(image)
    centers = kmeans.cluster_centers_.astype(int)
    centers_rgb = [tuple(center) for center in centers]
    centers_munsell = [rgb_to_munsell(center) for center in centers_rgb]
    st.write(f"Munsell notation for each cluster center: {centers_munsell}")

if __name__ == "__main__":
    main()

