# **[CASO -  identificar cor do solo pela carta de Munsell usando o Python e a inteligência artificial.](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi3uobiysv7AhVkrZUCHdWoA1MQFnoECAwQAQ&url=https%3A%2F%2Fbdm.unb.br%2Fbitstream%2F10483%2F16494%2F1%2F2016_ThalitaLuziaGuimaraes_tcc.pdf&usg=AOvVaw2pcgmk6duyN8PXmU4heZHK/)**



---


**Com este roteiro de aprendizagem, você terá uma visão do universo da IA e da Pedologia.** 

**Saiba no final como criar um modelo de IA que possa determinar a cor do solo pela carta de Munsell em uma foto.**

## **[ APLICATIVO DE PARA DETERMINAR A COR DO SOLO PELA CARTA DE MUNSELL] (https://marceloclaro-cor-do-solo-solo-segmentation-m8n8f0.streamlit.app/)**
https://marceloclaro-cor-do-solo-solo-segmentation-m8n8f0.streamlit.app/

---
**Professor: Marcelo Claro.**

marcelo.laranjeira@prof.educrateus.com.br

Whatsapp:(88)98158-7145  (https://www.geomaker.org/)


---

GRUPO DE ESTUDOS DE GEOTECNOLOGIAS E IA.   — GEOGRAFIA FAÇA VOCÊ MESMO  https://chat.whatsapp.com/HxqPo7PitMJDM0cJlCfPxu 
DRIVE DE PESQUISA DO GRUPO* — https://drive.google.com/drive/folders/19IJ2KUb24-mNGFsVgJYfKEKeONy90vYH?usp=sharing  
TELEGRAM- https://t.me/geografiaifce  

---



# **INTRODUÇÃO**

---


A cor é o primeiro indicador visual de um perfil de solo. É muito fácil perceber-(lhe), pois tem a função de identificar e caracterizar as propriedades do solo no campo.
A partir da coloração do solo, bem como de outras características do terreno, como mineralogia e teor de matéria orgânica, é possível inferir diversas informações sobre a topografia, vegetação e clima de uma região (FERNANDEZ & SCHULZE, 1992; SCHAETZL & ANDERSON, 2005).
Em 1951, o USDA escolheu o Munsell Chart Visual Comparison Standard para determinar a cor do solo como o método oficial de classificação do solo. Desde então, cientistas que pesquisam o solo usa o sistema de cores Munsell (SIMONSON, 1993). Esse sistema  é um método bastante utilizado para determinar a coloração do solo. Dividindo-se  a cor em três componentes: Hue (Matiz), Value (Valores) e Chroma (Croma). A cor principal espectral é o matiz, enquanto o valor é a luminosidade ou a escuridão de uma cor. O croma, no que lhe concerne, é a pureza de uma cor. 
As cartas Munsell Soil Swatches apresentam uma variedade de cores encontradas em diferentes tipos de solo, cada uma com uma abertura para que se possa comparar uma amostra do solo. A descrição Munsell para cada padrão de cor é a seguinte: valor de matiz/croma. Os pigmentos de terra são bastante usados globalmente devido à simplicidade e celeridade de serem aplicados em plantações.
A atribuição incorreta das cores das amostras de solo em um gráfico de Munsell requer a compreensão de alguns problemas associados ao diagrama. Dentre os problemas, está a dificuldade de compreender como o diagrama foi elaborado sob condições de iluminação específicas.
A carta Munsell oferece uma gama limitada de cores, o que pode dificultar a classificação exata de uma amostra de solo. Além disso, há uma controvérsia em relação ao processo manual de classificação de cores na tabela de Munsell, uma vez que avaliai-se as condições de aplicação em determinados campos, o que pode ser demorado e trabalhoso.  É importante ressaltar que a Carta de Munsell é elaborada em papel, facilitando a deterioração, principalmente na análise manual de cor em solo úmido. Além disso, essa ferramenta tem um alto custo para muitos usuários. 
O foco principal deste projeto era elaborar um método computadorizado para analisar com exatidão a coloração do solo através de imagens. Um grupo de fotografias de terra com diferentes cores foi usado para testar o algoritmo, que se mostrou bem-sucedido e de baixo custo, uma vez que analisa fotos de solo em campo, tanto secas quanto úmidas, capturadas por celulares.


---

## **COR DO SOLO**

---


As cores do solo são usadas para adicionar beleza e simbolismo à pintura corporal, pinturas rupestres e outras formas de arte. As cores derivadas do solo variam de amarelo e laranja a vermelho e marrom. Cada cor tem seu próprio significado e significado em diferentes culturas. Eles foram usados ​​pela primeira vez pelo povo aborígine da Austrália, que usava ocre, um pigmento amarelo-avermelhado, para pintar seus corpos para cerimônias e cerimônias. Escavações em cavernas na Austrália indicam que o ocre foi amplamente usado pelos primeiros australianos entre 57.000 e 71.000 anos atrás. Os nativos americanos Chusmas da Califórnia também usaram subtons em suas obras de arte. Eles usam hematita, um pigmento vermelho, para pintar listras e manchas vermelhas em seus corpos e tocas. Além da hematita, a tribo Chusmas também utilizava a argila branca para pintura corporal e rituais de cura. As cores do solo têm sido usadas há séculos e ainda são usadas hoje. (GUIMARÃES, 2016).


Ainda hoje, as cores da terra são proeminentes no artesanato, onde os pigmentos da terra são usados ​​como corantes. O projeto Cores da Terra (CARVALHO et al., 2007) foi desenvolvido pelo Departamento de Solos da Universidade Federal de Viçosa (UFV) para ensinar a fazer tintas de solo para pintar casas. As marcas de roupas havaianas são conhecidas por tingir todas as suas roupas com argila vermelha. Minerais são comumente usados ​​na indústria farmacêutica como ingredientes ou como excipientes para exibir propriedades terapêuticas. Também é muito utilizado em spas e centros de beleza (CARRETERO & POZO, 2009). Além das propriedades físicas, mecânicas e térmicas dos minerais, propriedades visuais como pigmentos e opacificantes são amplamente utilizadas para melhorar as propriedades organolépticas de produtos farmacêuticos (CARRETERO & POZO, 2009).

Cientistas russos começaram a prestar atenção à cor do solo no início do século XIX e começaram a descrevê-la em termos de matiz, luminosidade e saturação na década de 1920 (ZAKHAROV, 1927). Nos Estados Unidos, as propriedades de cor do solo não foram incluídas no sistema de classificação até 1914. Segundo Guimarães (2016), quando a Divisão de Solos do Departamento de Agricultura dos Estados Unidos (USDA) publicou uma lista de 22 nomes de fundos de cores de solo, não havia padrões de cores até então. O USDA, juntamente com a Munsell Company, preparou uma série de tabelas de cores para uso no Soil Survey Manual de 1951 (SOIL SURVEY STAFF, 1993). Desde então, o sistema de cores Munsell (MUNSELL SOIL COLOR COMPANY, 1950) e uma nova lista de nomes têm sido usados ​​e recomendados pelo USDA para determinar a cor do solo (SIMONSON, 1993). O sistema começa a ser adotado por pesquisadores de solo em todo o mundo.

Em 1949, a MUNSELL SOIL COLOR COMPANY criou o Sistema Americano de Classificação de Solos. Em 1950, a EMBRAPA começou a desenvolver um novo sistema de classificação de solos brasileiro que evoluiu desse antigo sistema de classificação. (EMBRAPA, 2013) A primeira versão do SiBCS foi lançada em 1999 e desde então foi revisada várias vezes. O diagrama de Munsell (MUNSELL SOIL COLOR COMPANY, 1950) serve como padrão para classificar as cores do solo no Sistema Brasileiro de Classificação de Solos - SiBCS.


---


## **IMPORTANCIA DA COR DO SOLO**

---


Mudanças na cor do solo fornecem informações sobre as propriedades físicas do solo. Essas mudanças podem ser resultado da topografia, vegetação, ventilação, clima, minerais, profundidade e matriz. Além disso, as mudanças de cor podem indicar a concentração de matéria orgânica no solo, grau de intemperismo, material de origem ou temperatura. Além disso, essas mudanças podem indicar informações sobre a classificação do solo, diferenciação estratigráfica e propriedades ambientais (FERNANDEZ & SCHULZE, 1992; SCHAETZL & ANDERSON 2005).

--- 


## **PROBLEMATIZAÇÃO**

---
A correspondência incorreta de amostras de solo com cores em um gráfico de Munsell requer a compreensão de alguns problemas associados ao diagrama. Um desses problemas é a dificuldade de entender como o diagrama foi criado sob condições de iluminação específicas. A carta Munsell permite apenas um número limitado de cores, o que pode dificultar a classificação precisa de uma amostra de solo. Além disso, o processo manual de classificação de cores na tabela de Munsell pode ser demorado e trabalhoso.


---

# **OBJETIVO**

---

O objetivo deste projeto foi desenvolver um método automatizado para classificar a cor do solo usando visão computacional. O método foi desenvolvido e testado usando um conjunto de dados de imagens coloridas do solo. Os resultados mostraram que o método conseguiu classificar com precisão as imagens coloridas do solo no conjunto de dados.
O conjunto de dados usado neste projeto é o conjunto de dados de imagens foi tirado do Sistema Brasileiro de Classificação de Solos (SiBCS). O conjunto de dados contém imagens coloridas do solo de sete locais diferentes. Além, das imagens, efetuadas em campo sob diferentes condições de iluminação e as amostras de solo que foram classificadas usando a tabela de cores do solo de Munsell.

---

# **METODOLOGIA**

---

O método desenvolvido neste projeto utiliza visão computacional com tecnicas de clusterização para extrair informações de cores das imagens coloridas do solo. A informação da cor RGB (Red, Green e Blue), depois de convertida em Munsell, é então usada para classificar as imagens coloridas do solo nas categorias de cores de solo Munsell apropriadas. A precisão da classificação do método foi testada usando o Munsell Soil Color Book.


---

# **RESULTADOS**

---
Os resultados mostraram que o método conseguiu classificar com precisão as imagens coloridas do solo no conjunto de dados. A precisão da classificação foi maior para as imagens coloridas do solo obtidas sob as condições de iluminação mais uniformes.

---

# **CONCLUSÃO**


---

Conclusão — O método desenvolvido neste projeto pode ser usado para classificar com precisão as imagens coloridas do solo. O método é particularmente útil para classificar imagens coloridas do solo tiradas sob condições de iluminação não uniformes.

---
