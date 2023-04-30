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


soil_dict = {
    "7.5YR5/4": "Argissolo Vermelho-Amarelo - Bahia - O Argissolo Vermelho-Amarelo é um solo de grau de fertilidade médio a alto, com capacidade para suportar culturas agrícolas e pastagens. Quanto à umidade, pode variar de média a baixa, dependendo das condições climáticas locais. Entre as carências mais comuns neste solo estão o déficit de matéria orgânica e nutrientes como fósforo e potássio. A vegetação típica desse solo na região é a caatinga, sendo uma vegetação adaptada às condições climáticas de baixa umidade e chuvas irregulares. Em termos de reflorestamento, algumas opções de plantas nativas para serem usadas são o angico, aroeira e jatobá. Quanto a cultivos agrícolas, o solo é adequado para o cultivo de grãos como milho e feijão, e também para frutas como manga e caju.",
    "10YR3/3": "Neossolo Regolítico - Pernambuco - O Neossolo Regolítico é um solo pouco espesso e com baixa fertilidade natural. Apesar disso, ele pode ser utilizado para cultivos de ciclo curto, como hortaliças e plantas ornamentais. A vegetação típica do Neossolo Regolítico é a caatinga arbustiva e arbórea, com espécies adaptadas à baixa umidade.",
    "2.5YR5/6": "Argissolo Amarelo - Ceará - O Argissolo Amarelo é um solo de baixa fertilidade natural e com grande parte da matéria orgânica acumulada na camada superficial. Apesar disso, ele pode ser utilizado para culturas de ciclo curto e pastagens, desde que haja um manejo adequado. A vegetação típica do Argissolo Amarelo é a caatinga arbustiva e arbórea, com espécies adaptadas às condições de baixa umidade e chuvas irregulares.",
    "10YR4/3": "Luvissolo Crômico - Paraíba - O Luvissolo Crômico é um solo com baixa fertilidade natural e com propriedades físicas que podem dificultar a infiltração de água. Apesar disso, ele pode ser utilizado para cultivos de ciclo curto e pastagens, desde que haja um manejo adequado. A vegetação típica desse solo é a caatinga arbustiva e arbórea.",
    "2.5YR5/4": "Cambissolo Háplico - Rio Grande do Norte - O Cambissolo Háplico é um solo pouco espesso e com baixa fertilidade natural. Apesar disso, ele pode ser utilizado para cultivos de ciclo curto, como hortaliças e plantas ornamentais. A vegetação típica desse solo é a caatinga arbustiva e arbórea, com espécies adaptadas à baixa umidade e chuvas irregulares.",
    "7R/0": "Luvissolo Crômico - Paraíba - O Luvissolo Crômico é um solo com baixa fertilidade natural e com propriedades físicas que podem dificultar a infiltração de água. Apesar disso, ele pode ser utilizado para cultivos de ciclo curto e pastagens, desde que haja um manejo adequado. A vegetação típica desse solo é a caatinga arbustiva e arbórea.",
    
}

def rgb_to_munsell(center, col_c):
    r,g,b = center[0][0],center[0][1],center[0][2]
    col_c.title('Valores para RGB')
    col_c.write('{0},{1},{2}'.format (r,g,b))
    print('passei dentro func')
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
    else:
        chroma = "9"
    return hue + value + "/" + chroma


    col_c.title('Valores para munsell') # define título para a seção 
    col_c.write('(MATIZ,VALORES,CROMA)') # imprime valores de h,c,v no console   
    col_c.write('{0},{1},{2}'.format (value,hue,chroma)) # imprime valores de h,l,s no console 
    #print(Value + hue + "/" + chroma )# retorna valor de matiz e croma 

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

munsell_notation = rgb_to_munsell(center[0][0], center[0][1], center[0][2])
soil_type = soil_dict.get(munsell_notation, "NÃO CADASTRADO")


     print("Tipo de solo correspondente:")
     print(soil_type)

    print("R,G,B") # imprime no console
    print(center[0]) # imprime no console 

    #print("Munsell") # imprime no console
    #print(rgb_to_munsell(center[0][0],center[0][1],center[0][2]))
    #printsoil_dict.get(munsell_notation, "NÃO CADASTRADO")
    st.button('__________________', on_click = rgb_to_munsell(center,col_c)) # imprime no console
    

   

    st.write('FONTE:  https://pteromys.melonisland.net/munsell/') # imprime no console
    st.write('') # imprime no console
