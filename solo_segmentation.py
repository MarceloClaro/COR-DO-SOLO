import streamlit as st  # import streamlit library for creating GUI
import pandas as pd # import pandas library for manipulating data in tabular format
import numpy as np # import numpy for manipulating data in matrix format
import cv2 # import opencv for image manipulation
import colorsys # import colorsys for converting rgb to munsell

# define function to convert rgb to munsell
def rgb_to_munsell(center,col_c): 
    r,g,b = center[0][0],center[0][1],center[0][2] # define variables for each color channel
    col_c.title('Valores para RGB') # define title for section
    col_c.write('{0},{1},{2}'.format (r,g,b)) # print r,g,b values to console
    h, l, s = colorsys.rgb_to_hls(r/255.0, g/255.0, b/255.0) # convert rgb to hls
    h = h*360 # convert h from 0-1 to 0-360
    # map h to munsell hue notation
    if h < 20: # if h is less than 20
        hue = "R" # hue is red
    elif h < 40: # if h is less than 40
        hue = "YR" # hue is red-yellow
    elif h < 75: # if h is less than 75
        hue = "Y" # hue is yellow
    elif h < 155: # if h is less than 155
        hue = "GY" # hue is green-yellow
    elif h < 190: # if h is less than 190
        hue = "G" # hue is green
    elif h < 260: # if h is less than 260
        hue = "BG" # hue is blue-green
    elif h < 290: # if h is less than 290
        hue = "B" # hue is blue
    elif h < 335: # if h is less than 335
        hue = "PB" # hue is purple-blue
    else:
        hue = "P" # hue is purple
    # map l to munsell value notation
    if l < 0.25: # if l is less than 0.25
        value = "2.5" # value is 10
    elif l < 0.3: # if l is less than 0.3
        value = "3" # value is 20
    elif l < 0.4: # if l is less than 0.4
        value = "4" # value is 20
    elif l < 0.5: # if l is less than 0.4
        value = "5" # value is 20
    elif l < 0.6: # if l is less than 0.6
        value = "6"  # value is 30
    elif l < 0.7: # if l is less than 0.4
        value = "7" # value is 20
    elif l < 0.8: # if l is less than 0.8
        value = "8" # value is 40
    else: 
        value = "10" # value is 50
    # map s to munsell chroma notation
    if s < 0.1: # if s is less than 0

    elif s < 0.2: # if s is less than 0.2
        chroma = "2" # chroma is 2
    elif s < 0.3: # if s is less than 0.3
        chroma = "4" # chroma is 4
    elif s < 0.4: # if s is less than 0.4
        chroma = "6" # chroma is 6
    elif s < 0.5: # if s is less than 0.5
        chroma = "8" # chroma is 8
    elif s < 0.6: # if s is less than 0.6
        chroma = "10" # chroma is 10
    elif s < 0.7: # if s is less than 0.7
        chroma = "12" # chroma is 12
    elif s < 0.8: # if s is less than 0.8
        chroma = "14" # chroma is 14
    elif s < 0.9: # if s is less than 0.9
        chroma = "16" # chroma is 16
    else:
        chroma = "18" # chroma is 18
    # return munsell notation as string
    return "{0} {1}/{2}".format(hue, value, chroma)

# example usage
center = np.array([[255, 0, 0]]) # red
col_c = st.empty() # create Streamlit widget
munsell_notation = rgb_to_munsell(center, col_c)
print(munsell_notation) # prints "R 10/18"
