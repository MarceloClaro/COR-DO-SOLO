# **[CASO -  identificar cor do solo pela carta de Munsell usando o Python e a inteligência artificial.](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwi3uobiysv7AhVkrZUCHdWoA1MQFnoECAwQAQ&url=https%3A%2F%2Fbdm.unb.br%2Fbitstream%2F10483%2F16494%2F1%2F2016_ThalitaLuziaGuimaraes_tcc.pdf&usg=AOvVaw2pcgmk6duyN8PXmU4heZHK/)**



---


**Com este roteiro de aprendizagem, você terá uma visão do universo da IA e da Pedologia.** 

**Saiba no final como criar um modelo de IA que possa determinar a cor do solo pela carta de Munsell em uma foto.**

## **[APLICATIVO DE PARA DETERMINAR A COR DO SOLO PELA CARTA DE MUNSELL](https://marceloclaro-cor-do-solo-solo-segmentation-m8n8f0.streamlit.app/)**
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


Usar inteligência artificial (IA) para reconhecer as cores Munsell é importante para a ciência do solo, pois elimina a variabilidade nos resultados causada pela subjetividade humana. Sistemas alimentados por inteligência artificial foram bem-sucedidos ao identificar as cores do solo em diferentes partes do planeta, como no Brasil (COSTA et al., 2018).

 A inteligência artificial proporciona diversos benefícios para a mensuração e avaliação da cor do solo, como maior exatidão, segurança e constância. A inteligência artificial também diminui o tempo e o número de trabalhadores necessários para classificar e avaliar o solo, permitindo o processamento de dados com mais celeridade e eficiência.

Este artigo discute as vantagens de usar IA para classificar o solo pelas cores Munsell. Inicialmente, será apresentada a história do sistema de cores Munsell e como ele é aplicado na classificação do solo. Depois, veremos como a IA pode identificar cores Munsell, o seu potencial para tirar a variabilidade humana na determinação da cor e aumentar a precisão, confiabilidade e consistência. Por fim, discutiremos os benefícios da inteligência artificial para classificar e avaliar o solo com menos tempo e trabalhadores.

A cor do solo é o método oficial de classificação do solo pelo Departamento de Agricultura dos Estados Unidos desde 1951. Desde então, a comunidade de estudos do solo tem usado este método, de acordo com Simonson (1993), aplicado no atual Sistema Brasileiro de Classificação de Solos (EMBRAPA, 2013). A coloração do solo é uma das primeiras características a serem percebidas num perfil de solo, pois é de fácil visualização. Sendo assim, também é empregado como um predicado para identificação e caracterização do solo.

Segundo FERNANDEZ & SCHULZE (1992) e SCHAETZL & ANDERSON (2005), através da coloração do solo, é possível inferir informações sobre o relevo, vegetação e clima da região, bem como propriedades peculiares do solo, tais como mineralogia e concentração de matéria orgânica. O Munsell Color System, de 1950, classifica as cores em três componentes: Hue, Value e Chroma. Hue é a cor espectral dominante, Value é a luminosidade e Chroma é a saturação da cor. A tabela Munsell Soil Color Chart tem sido amplamente utilizada para determinar a cor do solo, pois é fácil e rápida de ser aplicada no campo. Este gráfico é composto por uma variedade de padrões de cores, com notações Munsell de valor de matiz/croma correspondentes abaixo de cada um, segundo Dalmolin et al. (2005) e Schanda (2007).

O Comitê Internacional de Colorimetria definiu diversos espaços colorimétricos para estabelecer as cores em três estímulos, como o espaço xyY, em 1931. Onde x e y representam a cromaticidade e Y representa a luminosidade (Ohta & Robertson, 2006). Rossel et al (2006) compararam o sistema Munsell com o espaço colorimétrico xyY e encontraram correlações satisfatórias entre o matiz e a coordenada y, o croma e a coordenada x e o valor com o estímulo Y. No entanto, esse método usual de determinar a coloração do solo é subjetivo, pois é influenciado por fatores como as características da luz que incide no solo e a percepção visual dos espectadores (Melville & Atkinson, 1985).

O objetivo desta pesquisa foi comparar os métodos usados para determinar a cor do solo, utilizando a Carta de Munsell e a Inteligência Artificial, a fim de avaliar a precisão de cada um e possíveis diferenças entre os dois. Os tons dos horizontes de superfície e subsuperfície de cinco solos em Crateús, Ceará, foram mensurados em condições controladas, o que excluiu a subjetividade e a margem de erro humano, permitindo uma caracterização mais acurada da cor (BOTELLHO et al.,2006). Além do método de comparação visual, também foi pesquisada a utilização de Inteligência Artificial com uma aplicação web.


---


# **REVISÃO BIBLIOGRÁFICA**
---

## **COLORAÇÃO DO SOLO**

---
Os pigmentos do solo são usados ​​para criar as cores de muitas civilizações. Os aborígenes australianos utilizavam o ocre, extraído do solo, para a pintura corporal em todas as cerimônias importantes da vida, desde o nascimento até a morte (TAÇON, 2004). Em cavernas, descobriu-se que o ocre foi usado pelos australianos há 57.000-71.000 anos (THORNE et al., 1999). Os Chusmas, que viviam no centro e sul da Califórnia, usavam hematita em suas pinturas rupestres vermelhas (GRANT, 1965). Os Chusmas também utilizavam a argila branca para unções corporais e rituais de cura (ROBINSON, 2004).

A cor do solo ainda é um destaque no artesanato e os pigmentos do solo são usados como corantes. O projeto Cores da Terra, descrito por CARVALHO et al. (2007), desenvolvido pelo Departamento de Solos da Universidade Federal de Viçosa (UFV), ensina a produzir tintas com base em solo para pintar residências. Na ilha do Havaí, uma marca de vestuário é bastante famosa pelo fato de todas as suas peças serem tingidas com terra vermelha.

Minerais são usados frequentemente na indústria farmacêutica como elementos ativos, por conta das suas propriedades curativas, ou como substâncias inertes. Também é comum utilizá-los em spas e clínicas de estética, conforme CARRETERO & POZO (2009). Os autores também mencionam que os pigmentos e opacificantes são usados para melhorar as propriedades organolépticas de medicamentos. 

As argilas são ativos em cosméticos, como máscaras faciais. São aconselhadas no tratamento de derrames na pele, como inchaços e oleosidade, pelo seu poder de aspirar óleos e toxinas (CARRETERO, 2002). Há uma grande variedade de cores (branco, amarelo, cinza, verde, etc.) e cada uma das argilas usadas em procedimentos estéticos tem uma função específica que depende de suas propriedades físico-químicas, conforme LÓPEZ-GALINDO et al. (2007) apontam.

A cor do solo é uma característica importante na ciência do solo. Pelo seu aspecto e características facilmente identificáveis, a cor do solo é largamente utilizada para classificar e interpretar os solos, conforme SANTOS et al. (2005) relata.

Solos escuros eram considerados férteis, enquanto os claros eram tachados de improdutivos. Columela, um escritor romano do primeiro século, discordava desta opinião ao considerar a infertilidade de solos pretos de pântanos e a alta fertilidade dos solos claros da Líbia, conforme salientam LAPIDO-LOUREIRO et al. (2009).

Os habitantes indígenas Xicrin, na reserva Kayapó-Xicrin, classificaram os solos pelas cores branco, vermelho, amarelo e preto. Além da tonalidade, a textura, a existência de pedras e a umidade do terreno também são considerados, de acordo com COOPER et al. (2005).

Os cientistas russos começaram a se concentrar na coloração dos solos no início do século XIX.

Durante a década de 1920, começaram a descrever a cor do solo de acordo com a tonalidade, brilho e saturação cita ZAKHAROV, (1927). Nos Estados Unidos, a cor do solo não foi considerada até 1914, quando o Departamento de Agricultura dos Estados Unidos  (USDA)   publicou uma lista com vinte e dois nomes para cores de solo. A partir de 1951, o manual de levantamento de solo adota uma série de cartas de cores preparadas pela Munsell Company, como afirma o SOIL SURVEY STAFF (1993).  

A partir daquele momento, o sistema de cores de Munsell (MUNSELL SOIL COLOR COMPANY, 1950) e uma nova lista de nomes foram adotados e recomendados pela USDA para determinar as cores dos solos (SIMONSON, 1993). Esse método de classificação foi adotado por especialistas em solo de todos os continentes.

O SiBCS (Sistema Brasileiro de Classificação de Solos), segundo a EMBRAPA (2013), surge como uma melhoria do sistema americano de classificação. Ele começou a ser desenvolvido no ano de 1950, sendo a sua primeira edição publicada no ano de 1999. O Sistema Brasileiro de Classificação de Solos utiliza a carta de Munsell (MUNSELL SOIL COLOR COMPANY, 1950) como referência para classificar a cor do solo.


---

## **RELEVÂNIA**

---


A coloração é uma característica física que pode revelar muito sobre o solo, como, por exemplo, a alteração do tom pode ser uma reação a variações de relevo, vegetação, profundidade, clima, arejo, material de origem, grau de intemperismo, mineralogia e concentração de matéria orgânica. O mesmo pode revelar suas características, classificação e horizonte, além de influenciar sua temperatura, conforme as obras de FERNANDEZ & SCHULZE (1992) e SCHAETZL & ANDERSON (2005).

Estudos procuram estabelecer a análise da cor como um método mais rápido e econômico para determinar algumas propriedades do solo, em relação aos métodos tradicionais. De acordo com BARRON & TORRENT (1986), CAMPOS et al. (2003) e MADEIRA NETTO et al. (1997), é possível identificar e quantificar os óxidos de ferro analisando a cor do solo. Já Braumann et al. (2016) e Schulze et al. (1993) avaliaram a correlação entre a cor do solo e a concentração e composição de matéria orgânica.

A coloração é uma característica relevante para identificar e descrever o solo, comparada com os padrões da carta de Munsell, que diferencia algumas classes de solos no atual Sistema Brasileiro de Classificação de Solos (EMBRAPA, 2013). Um exemplo disso é quando determinamos o nome no segundo nível categórico de Argissolos, Latossolos e Nitossolos, sendo a cor o fator que os diferencia quando as outras características são idênticas.

Como apontado por Escadafal et al. (1989), a coloração do solo também é relevante para o sensoriamento à distância. Estudaram a correlação entre a coloração do solo e as faixas do LANDSAT e obtiveram coeficientes de correlação maiores que 0,90 (90%) nas cores medidas com a carta de Munsell. 

Já Mattikalli (1997) utilizou a reactância, a razão entre a intensidade da radiação total refletida e da radiação total incidente, para determinar a cor de 76 solos. Como os intervalos espectrais coincidiram com as bandas do sensor multiespectral (MSS) do LANDSAT, pode-se usá-lo para identificar e mapear solos em áreas extensas ou inacessíveis com imagens de satélite.


---

## **ORICTOGNOSIA**

---

A Orictognosia é o ramo da ciência que se dedica ao estudo dos minerais e à sua identificação. A mineralogia está ligada ao material de origem e ao nível de intemperismo do solo, como referido por SCHAETZL & ANDERSON, (2005).

Quando se examinam os Neossolos que tiveram pouca evolução pedogenética, percebe-se que são arenosos ou franco-arenosos porque são ricos em quartzo. Esses tipos de solo geralmente são carentes de matéria orgânica e óxidos de ferro. De acordo com AZEVEDO (2006) e EMBRAPA (2013), têm pouca pigmentação, são mais claros e esbranquiçados.

Já os Latossolos, terrenos com drenagem e intemperizados, têm uma cor avermelhada ou amarelada devido aos óxidos de ferro, que influenciam as propriedades dos solos, especialmente a cor. A presença desses minerais, conforme os autores STONER & BAUMGARDNER (1981), pode mascarar a influência de outros elementos sobre a cor do solo. Se os teores de óxidos de ferro forem superiores a 4%, eles podem ocultar o efeito da matéria orgânica, conforme os autores.

De acordo com DALMOLIN et al. (2005), os óxidos de ferro têm cores diferentes devido à absorção seletiva da luz na região do visível, provocada pela transição de elétrons na camada orbital. A goethita absorve um comprimento de onda menor, apresentando maior reflectância que a hematita, como relataram VITORELLO & GALVÃO (1996) e KOSMAS et al. (1984). Stoner et al. (1991) notaram que a predominância da hematita no solo aumenta a capacidade de absorção de luz, deixando-o mais opaco. 

A goethita é o óxido de ferro hidratado mais presente nos terrenos. Ela pode ser encontrada nas regiões tropicais e temperadas e deixa o solo amarelado. Já a hematita, um óxido de ferro não-hidratado, deixa o solo com uma tonalidade forte e avermelhada. Em exemplares que são heterogêneos, a hematita, apesar de ser uma quantidade minúscula, costuma mascarar a goethita, de forma que ela pareça vermelha, de acordo com Resende (1976), Schaetzl & Anderson (2005) e Schwertmann (1988). Os solos tropicais e subtropicais geralmente têm uma coloração mais alaranjada devido aos níveis variados de hematita e goethita presentes neles.

Já os terrenos de climas temperados são caracterizados pela goethita e, geralmente, não possuem hematita em sua composição, logo, são mais alaranjados ou acastanhados, conforme apontam SCHWERTMANN & TAYLOR (1989).

Quando o solo está saturado de água por um longo período ou em situações anaeróbicas, o ferro presente nele sofre uma redução, deixando-o com uma coloração cinzenta. Este processo é característico dos Gleissolos sendo conhecido como gleização, de acordo com SCHWERTMANN (2008).

A cor que cada mineral apresenta decorre da interação com a luz visível, dependendo da estrutura cristalina e do tamanho das partículas. Solos com mais goethita são mais amarelos, enquanto os com menos tendem a ser acinzentados. Partículas de hematita maiores são mais púrpuras que as menores, conforme Torrent & Schwertmann (1987).

A Tabela 1 mostra os minerais do solo e suas formulações correspondentes. Além disso, relaciona-os à notação de cor Munsell; o tamanho das partículas interfere na coloração, como Santos et al. (2005) traduziu os nomes das cores.

Tabela 1. Notação de Munsell para a cor de minerais, de acordo com Marilyn & Pearson (2000).



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
