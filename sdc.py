'''
Sistema de cores munsell para solo
'''

#Bibliotecas aplicadas
import cv2
import numpy as np
import pandas as pd
import argparse

# Criando analisador de argumentos para obter o caminho da imagem na linha de comando
ap = argparse.ArgumentParser()
ap.add_argument('image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

#Ler a imagem com opencv
img = cv2.imread(img_path)

# declarar variáveis globais
clicked = False
r = g = b = xpos = ypos = 0

#Lendo arquivo csv com pandas e dando nomes a cada coluna
index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('cores.csv', names=index, header=None)

#função para calcular a distância mínima de todas as cores e obter a cor mais correspondente
#acho que o problema esta aqui...
def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

#função para obter as coordenadas x, y do clique duplo do mouse
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('COR DE SOLO-SISTEMA MUNSELL. DI/LATTES: PROJETO ANTENADO. Codigo CI: JR9F00000001 - AUTOR: MARCELO CLARO')
cv2.setMouseCallback('COR DE SOLO-SISTEMA MUNSELL. DI/LATTES: PROJETO ANTENADO. Codigo CI: JR9F00000001 - AUTOR: MARCELO CLARO',draw_function)

while(1):

    cv2.imshow("COR DE SOLO-SISTEMA MUNSELL. DI/LATTES: PROJETO ANTENADO. Codigo CI: JR9F00000001 - AUTOR: MARCELO CLARO",img)
    if (clicked):

        # cv2.rectangle (imagem, ponto inicial, ponto final, cor, espessura) -1 preenche o retângulo inteiro 
        cv2.rectangle(img,(20,20), (750,60), (b,g,r), -1)

        # Criando sequência de texto para exibição (nome da cor e valores RGB)
        text = getColorName(r,g,b) + ' R='+ str(r) +  ' G='+ str(g) +  ' B='+ str(b)

        # cv2.putText (imgem, texto, início, fonte (0-7), fonte Escala, cor, espessura, tipo de linha)
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        #Para cores muito claras, exibiremos o texto na cor preta
        if r >= 95 or g >= 95 or b >= 95:
            print('passou do limite!!')
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)

        clicked=False

    # Quebre o loop quando o usuário pressionar a tecla 'esc'
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
