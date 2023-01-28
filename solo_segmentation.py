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
    col_c.write('(MATIZ,VALORES,CROMA)') # imprime valores de h,c,v no console   
    col_c.write('{0},{1},{2}'.format (hue,value,chroma)) # imprime valores de h,l,s no console 
    #print(hue + " " + value + " " + chroma )# retorna valor de matiz e croma 

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

    st.subheader('Arquétipos Junguiano - Legenda de 45 cores ') # define subtítulo para a seção FONTE 14
1. st.write('Vermelho Vivo — Anima/Anímico: Vitalidade; Sombra: Impulsividade; Personalidade: Autocontrole.')
2. st.write('Rosa Brilhante — Anima/Anímico: Abundância; Sombra: Propensão ao Excesso; Personalidade: Equilíbrio.') 
3. st.write('Laranja Ardente — Anima/Anímico: Entusiasmo; Sombra: Imaturidade; Personalidade: Sabedoria. ')
4. st.write('Magenta Vibrante — Anima/Anímico: Criatividade; Sombra: Contrariedade; Personalidade: Flexibilidade.') 
5. st.write('Índigo Profundo — Anima/Anímico: Intuição; Sombra: Dúvida; Personalidade: Inteligência. ')
6. st.write('Verde Claro — Anima/Anímico: Renovação; Sombra: Insegurança; Personalidade: Autoconfiança.') 
7. st.write('Azul Elétrico — Anima/Anímico: Liberdade; Sombra: Desordem; Personalidade: Responsabilidade.') 
8. st.write('Amarelo Solar — Anima/Anímico: Otimismo; Sombra: Negatividade; Personalidade: Intencionalidade.') 
9. st.write('Lilás Suave — Anima/Anímico: Humildade; Sombra: Inadaptabilidade; Personalidade: Adaptabilidade. ')
10. st.write('Castanho Neutro — Anima/Anímico: Estabilidade; Sombra: Estagnação; Personalidade: Evolução. ')
11. st.write('Turquesa Brilhante — Anima/Anímico: Energia; Sombra: Impaciência; Personalidade: Paciência. ')
12. st.write('Cinza Algo — Anima/Anímico: Introversão; Sombra: Desalinho; Personalidade: Clareza. ')
13. st.write('Branco Radiante — Anima/Anímico: Pureza; Sombra: Falsidade; Personalidade: Honradez. ')
14. st.write('Azul Escuro — Anima/Anímico: Segurança; Sombra: Desconfiança; Personalidade: Tranquilidade.') 
15. st.write('Verde Escuro — Anima/Anímico: Estoicismo; Sombra: Frialdade; Personalidade: Afetuosidade. ')
16. st.write('Laranja Avermelhado — Anima/Anímico: Envolvimento; Sombra: Insegurança; Personalidade: Confiança.') 
17. st.write('Rosa Calorosa — Anima/Anímico: Carinho; Sombra: Medo; Personalidade: Coragem. ')
18. st.write('Vermelho Oculto — Anima/Anímico: Força; Sombra: Ira; Personalidade: Autocontrole.') 
19. st.write('Magenta Escuro — Anima/Anímico: Profundidade; Sombra: Desespero; Personalidade: Esperança.') 
20. st.write('Índigo Vintage — Anima/Anímico: Consciência; Sombra: Desesperança; Personalidade: Fé. ')
21. st.write('Verde Menta — Anima/Anímico: Calma; Sombra: Desânimo; Personalidade: Perseverança. ')
22. st.write('Azul Petróleo — Anima/Anímico: Liderança; Sombra: Rigidez; Personalidade: Suavidade. ')
23. st.write('Amarelo Luminoso — Anima/Anímico: Alegria; Sombra: Ansiedade; Personalidade: Autogoverno. ')
24. st.write('Lilás Atrevido — Anima/Anímico: Intriga; Sombra: Preconceito; Personalidade: Respeito. ')
25. st.write('Marrom Neutro — Anima/Anímico: Praticidade; Sombra: Comodismo; Personalidade: Determinação. ')
26. st.write('Turquesa Refinado — Anima/Anímico: Gratidão; Sombra: Resentimento; Personalidade: Agradecimento. ')
27. st.write('Cinza Confiante — Anima/Anímico: Resiliência; Sombra: Hiperestimulação; Personalidade: Autorespeito. ')
28. st.write('Branco Clássico — Anima/Anímico: Simplicidade; Sombra: Conformismo; Personalidade: Inovação. ')
29. st.write('Azul Marinho — Anima/Anímico: Iniciativa; Sombra: Intransigência; Personalidade: Aceitação. ')
30. st.write('Verde Vinho — Anima/Anímico: Experiência; Sombra: Ira reprimida; Personalidade: Autocura. ')
31. st.write('Pêssego Radiante — Anima/Anímico: Amizade; Sombra: Autossabotagem; Personalidade: Autocuidado. ')
32. st.write('Rosa Neutro — Anima/Anímico: Compaixão; Sombra: Submissão; Personalidade: Autonomia. ')
33. st.write('Vermelho Real — Anima/Anímico: Paixão; Sombra: Entrega Excessiva; Personalidade: Equilíbrio. ')
34. st.write('Magenta Radiante — Anima/Anímico: Vitalidade; Sombra: Desmantelamento; Personalidade: Integração. ')
35. st.write('Índigo Intenso — Anima/Anímico: Intuição; Sombra: Ilusões; Personalidade: Pragmatismo. ')
36. st.write('Verde Pastel — Anima/Anímico: Inspiração; Sombra: Imobilidade; Personalidade: Iniciativa. ')
37. st.write('Azul Vibrante — Anima/Anímico: Expressão; Sombra: Melancolia; Personalidade: Autoencorajamento. ')
38. st.write('Amarelo Quente — Anima/Anímico: Entusiasmo; Sombra: Sensibilidade Excessiva; Personalidade: Autocomando. ')
39. st.write('Lilás Pálido — Anima/Anímico: Admiração; Sombra: Preconceito; Personalidade: Abertura. ')
40. st.write('Bege Suave — Anima/Anímico: Simplicidade; Sombra: Inautenticidade; Personalidade: Autenticidade. ')
41. st.write('Turquesa Neutro — Anima/Anímico: Desprendimento; Sombra: Intensidade Excessiva; Personalidade: Equilíbrio. ')
42. st.write('Cinza Profundo — Anima/Anímico: Conhecimento; Sombra: Falta de Foco; Personalidade: Concentração. ')
43. st.write('Branco Puro — Anima/Anímico: Transcendência; Sombra: Enganar-se; Personalidade: Autoaceitação. ')
44. st.write('Azul Sereno — Anima/Anímico: Calma; Sombra: Indiferença; Personalidade: Sensibilidade. ')
45. st.write('Verde Musgo — Anima/Anímico: Natureza; Sombra: Desapego Excessivo; Personalidade: Comprometimento.')