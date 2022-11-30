import streamlit as st  # importar biblioteca streamlit para criar interface gráfica 
#import plotly_express as px # importar biblioteca plotly express para criar gráficos  
import pandas as pd # importar biblioteca pandas para manipular dados em formato de tabela 
import numpy as np # importa numpy para manipular dados em formato de matriz  
import cv2 #import opencv #importar biblioteca opencv para manipular imagens 
#import csv # importar csv para manipular arquivos csv  
import colorsys # importar colorsys para converter rgb para munsell  
#from matplotlib import pyplot as plt # importa pyplot para criar gráficos 
from sklearn.cluster import KMeans # importa k-means para segmentação de imagens 
#from PIL import Image # importa biblioteca para manipular imagens  



def rgb_to_munsell(center,col_c): # define função para converter rgb para munsell
    r,g,b = center[0][0],center[0][1],center[0][2] # define variáveis para cada canal de cor  
    #print("R,G,B") # imprime no console  
    #print(center[0]) # imprime no console  
    col_c.title('Valores para RGB') # define título para a seção 
    col_c.write('{0},{1},{2}'.format (r,g,b)) # imprime valores de r,g,b no console  
    print('passei dentro func') # imprime no console    
    h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0) #converter rgb para hls 
    h = h*360 # converter h de 0-1 para 0-360 
    if h < 20: # se h for menor que 20
        hue = "R" # matiz é vermelho
    elif h < 40: # se h for menor que 40
        hue = "YR" # matiz é vermelho-amarelo
    elif h < 75: # se h for menor que 75
        hue = "Y" # matiz é amarelo
    elif h < 155: # se h for menor que 155
        hue = "GY" # matiz é verde-amarelo
    elif h < 190: # se h for menor que 190
        hue = "G" # matiz é verde
    elif h < 260: # se h for menor que 260
        hue = "BG" # matiz é verde-azulado
    elif h < 290: # se h for menor que 290
        hue = "B" # matiz é azul
    elif h < 335: # se h for menor que 335
        hue = "PB" # matiz é roxo-azul
    else:
        hue = "P" # matiz é roxo
    if l < 0.25: # se l for menor que 0,2
        value = "2.5" # valor é 10
    elif l < 0.3: # se l for menor que 0.4
        value = "3" # valor é 20
    elif l < 0.4: # se l for menor que 0.4
        value = "4" # valor é 20
    elif l < 0.5: # se l for menor que 0.4
        value = "5" # valor é 20
    elif l < 0.6: # se l for menor que 0.6
        value = "6"  # valor é 30
    elif l < 0.7: # se l for menor que 0.4
        value = "7" # valor é 20
    elif l < 0.8: #  se l for menor que0.8
        value = "8" # valor é 40
    else: 
        value = "10" # valor é 50
    if s < 0.1: # se s for menor que 0,1
        chroma = "0" # croma é 0
    elif s < 0.2: # se s for menor que 0.2
        chroma = "1" # croma é 1
    elif s < 0.3: # se s for menor que 0.3
        chroma = "2" # croma é 2
    elif s < 0.4: # se s for menor que 0.4
        chroma = "3" # croma é 3
    elif s < 0.5: # se s for menor que 0.5
        chroma = "4" # croma é 4
    elif s < 0.6: # se s for menor que 0.6
        chroma = "5" # croma é 5
    elif s < 0.7:  # se s for menor que 0.7
        chroma = "6" # croma é 6
    elif s < 0.8: # se s for menor que 0.8
        chroma = "7" # croma é 7
    elif s < 0.9:  # se s for menor que 0.9
        chroma = "8" # croma é 8
    elif s < 1.0: # se s for menor que 1.0
        chroma = "9" # croma é 9
    col_c.title('Valores para munsell') # define título para a seção    
    col_c.write('{0},{1},{2}'.format (hue,value,chroma)) # imprime valores de h,l,s no console 
    #print(hue + " " + value + " " + chroma )# retorna valor de matiz e croma 

st.image('https://lh6.googleusercontent.com/hiRKdv5UxSXINPZa_bYOf_s2X37WB67MAqwom1r1qzmKZsfCJF1RrLe_zlISG2vfOGeJwuBpTklRx409cgF2-Xo=w1280') # insere imagem da carta de munsell
st.title('Geomaker - Laboratório de Geografia ') # define título para a seção 
st.subheader('Classificar a cor do solo pela carta de Munsell') # define subtítulo para a seção FONTE 12
st.write('Prof. Marcelo Claro / marceloclaro@geomaker.org') # define texto para a seção
st.write('Whatsapp - (88)98158-7145') # define texto para a seção
st.write('https://www.geomaker.org') # define texto para a seção

#st.sidebar.subheader('configurações de visualização')

image = st.file_uploader(label = 'faça o upload da sua imagem',
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
    st.write('(MATIZ,VALORES,CROMA)') # define texto para a seção

   

    st.write('FONTE:  https://pteromys.melonisland.net/munsell/') # imprime no console
    