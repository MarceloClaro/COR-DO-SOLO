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
st.image('https://lh6.googleusercontent.com/hiRKdv5UxSXINPZa_bYOf_s2X37WB67MAqwom1r1qzmKZsfCJF1RrLe_zlISG2vfOGeJwuBpTklRx409cgF2-Xo=w1280') # insere imagem da carta de munsell
st.title('Geomaker - Clube de Pintura e Terapia Junguiana ') # define título para a seção 
st.subheader('Arquétipos Junguiano ') # define subtítulo para a seção FONTE 12
st.write('Prof. Marcelo Claro / marceloclaro@geomaker.org') # define texto para a seção
st.write('https://orcid.org/0000-0001-8996-2887') # define texto para a seção
st.write('Whatsapp - (88)98158-7145') # define texto para a seção
st.write('https://www.geomaker.org') # define texto para a seção



#st.sidebar.subheader('configurações de visualização')

image = st.file_uploader(label = 'Faça o upload da sua imagem',
                         type = ['jpg','png','jpeg'] )# define a seção para upload de imagem 


# converter rgb para munsell


col_a,col_b,col_c = st.columns(3) # define a seção para upload de imagem  



if image is not None: # se imagem for diferente de nulo 

    #print(dir(image.name)) # imprime no console
    
    print('passei') # imprime no console
    #plt.imshow(img) # mostra imagem no console
    #plt.show() # mostra imagem no console
    
    col_a.title('Imagem original') # define título para a seção
    col_a.image(image) # mostra imagem no console
    #plt.imshow(img) # mostra imagem no console
    #plt.show() # mostra imagem no console


    file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8) # converte imagem para array de bytes 
    opencv_image = cv2.imdecode(file_bytes, 1) # converte imagem para array de bytes 
    
    #img = cv2.imread(img_array) # leia a imagem
    img = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB) #converte para rgb 
    Z = img.reshape((-1,3)) # remodela para uma lista de pixels 
    Z = np.float32(Z) # converter para np.float32
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0) # define critérios, número de clusters(K) e aplica kmeans()
    K = 1 # número de clusters
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS) # converte para valores de 8 bits
    center = np.uint8(center) # converte para uint8
    print('calculado o center') # imprime no console 
    res = center[label.flatten()] # converte de volta para a imagem de 3 canais da imagem de 1 canal
    #col_b.image() # mostra imagem no console
    res2 = res.reshape((img.shape)) # mostra a imagem
    col_b.title('Imagem processada')# define título para a seção    
    col_b.image(res2) # mostra imagem no console 
    #plt.imshow(res2)
    #plt.show() 


    print("R,G,B") # imprime no console
    print(center[0]) # imprime no console 

    #print("Munsell") # imprime no console
    #print(rgb_to_munsell(center[0][0],center[0][1],center[0][2]))
    st.button('__________________', on_click = rgb_to_munsell(center,col_c)) # imprime no console
    

   

    st.write('FONTE:  https://pteromys.melonisland.net/munsell/') # imprime no console
    st.write('') # imprime no console

