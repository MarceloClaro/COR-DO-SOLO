import streamlit as st
import cv2
import numpy as np
from sklearn.cluster import KMeans
from skimage import io

def load_image(image_file):
    img = io.imread(image_file)
    return img

def segment_image(image, n_clusters):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixel_values = image.reshape((-1, 3))
    pixel_values = np.float32(pixel_values)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixel_values, n_clusters, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    segmented_image = centers[labels.flatten()]
    segmented_image = segmented_image.reshape(image.shape)
    return segmented_image

def display_image(image):
    st.image(image, use_column_width=True)

def main():
    st.title("Soil Color Classification App")
    st.text("Upload an image of the soil sample")

    image_file = st.file_uploader("Upload Image", type=['jpeg', 'png', 'jpg'])
    n_clusters = st.slider("Number of color clusters", 2, 10, 5)

    if image_file is not None:
        image = load_image(image_file)
        st.text("Original Image")
        display_image(image)

        st.text("Segmented Image")
        segmented_image = segment_image(image, n_clusters)
        display_image(segmented_image)

if __name__ == "__main__":
    main()
