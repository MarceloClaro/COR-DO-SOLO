'''
Sistema de cores munsell para solo
'''

from image_to_rgb import color_counter
from sys import argv as args
from pandas import read_csv
import cv2

img_path = args[1]
img = cv2.imread(img_path)

index=["color", "color_name", "hex", "R", "G", "B"]
csv = read_csv('cores.csv', names=index, header=None)

cc = color_counter(img_path)
img_total = cc['total']
img_matrix = cc['matrix']
img_colors = cc['colors']
del cc

def getColorName(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

clicked = r = g = b = 0
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global r,g,b, clicked, img_matrix
        r, g, b = img_matrix[x][y]
        clicked = 1

cv2.namedWindow('COR DE SOLO - SISTEMA MUNSELL')
cv2.setMouseCallback('COR DE SOLO - SISTEMA MUNSELL', draw_function)

while 1:
    cv2.imshow('COR DE SOLO - SISTEMA MUNSELL', img)
    if (clicked):
        text_color = (0, 0, 0)
        if r >= 95 or g >= 95 or b >= 95:
            text_color = (255, 255, 255)

        color_name = f'{getColorName(r,g,b)} {(r, g, b)}'
        color_percentage = f'{img_colors[(r, g, b)]*100/img_total}'
        text = f'{color_name} : {color_percentage}% of image'

        cv2.rectangle(img, (20,20), (900,60), (r, g, b), -1)
        cv2.putText  (img, text, (50,50), 2, 0.8, text_color, 2, cv2.LINE_AA)

        clicked = 0

    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
