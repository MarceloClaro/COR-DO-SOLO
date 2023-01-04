idebar.subheader('configurações de visualização')

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
    
