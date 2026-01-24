# Dashboard de Classificação de Cor do Solo (Munsell/Embrapa)

![CI](https://github.com/MarceloClaro/COR-DO-SOLO/actions/workflows/ci.yml/badge.svg)

Este projeto utiliza processamento de imagens e aprendizado de máquina para identificar cores de solo e sugerir classificações baseadas no Sistema Brasileiro de Classificação de Solos (SiBCS - Embrapa).

## 🚀 Funcionalidades

O aplicativo gera um **Dashboard Completo** contendo:

1.  **Análise de Imagem:** Upload de amostras de solo **Seco** e **Úmido** para comparação direta.
2.  **Segmentação de Cores:** Utiliza algoritmos de agrupamento (K-Means ou Fuzzy C-Means) para identificar as cores dominantes da amostra, ignorando ruídos.
3.  **Conversão Munsell:** Converte os valores RGB digitais para a notação Munsell (Matiz, Valor, Croma) padrão utilizada na pedologia.
4.  **Classificação Pedológica:** Infere a classe de solo provável (ex: Latossolo Vermelho, Gleissolo) baseada nas regras de cor da Embrapa.
5.  **Estatísticas de Validação:** Apresenta métricas de erro médio e desvio padrão para avaliar a qualidade da segmentação digital.

## 🛠️ Como Usar

1.  Execute o aplicativo:
    ```bash
    streamlit run solo_segmentation.py
    ```
2.  Na barra lateral (**Configurações**):
    *   Faça o upload da foto do **Solo Seco** e/ou **Solo Úmido**.
    *   Escolha o método de clusterização (K-Means é geralmente mais rápido, Fuzzy C-Means lida melhor com transições suaves).
    *   Ajuste o número de cores dominantes (K). O padrão é 3.
3.  Clique em **"Gerar Dashboard de Análise"**.
4.  Analise os resultados apresentados nos painéis de classificação e validação.

## ⚠️ Limitações Importantes

*   **Iluminação:** A precisão da cor depende da qualidade da foto. Fotos em sombra ou com balanço de branco incorreto gerarão classificações erradas.
*   **Calibração:** Este software não substitui a análise em laboratório ou o uso da carta física de Munsell em campo por um profissional, pois não há calibração de cor da câmera do dispositivo.
*   **Inferência:** A classificação de solo apresentada é uma sugestão baseada exclusivamente na cor. A classificação real exige análise química, física e morfológica do perfil.

## 📚 Referências

*   **SiBCS:** Santos, H. G. et al. (2018). Sistema Brasileiro de Classificação de Solos. 5. ed. Brasília, DF: Embrapa.
*   **Munsell:** Munsell Soil Color Charts.

---
**Desenvolvedor:** Professor Marcelo Claro
