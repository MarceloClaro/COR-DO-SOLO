# Dashboard de Classificação de Cor do Solo (Cyberpunk Edition)

![CI](https://github.com/MarceloClaro/COR-DO-SOLO/actions/workflows/ci.yml/badge.svg)

Este projeto utiliza processamento de imagens e aprendizado de máquina para identificar cores de solo e sugerir classificações baseadas no Sistema Brasileiro de Classificação de Solos (SiBCS - Embrapa), com uma interface moderna estilo Cyberpunk.

## 🚀 Funcionalidades

O aplicativo gera um **Dashboard Completo** contendo:

1.  **Análise de Imagem:** Upload de amostras de solo **Seco** e **Úmido** para comparação direta.
2.  **Segmentação de Cores:** Utiliza algoritmos de agrupamento (K-Means ou Fuzzy C-Means) para identificar as cores dominantes da amostra.
3.  **Conversão Munsell:** Converte os valores RGB digitais para a notação Munsell.
4.  **Classificação Pedológica:** Infere a classe de solo provável (ex: Latossolo Vermelho, Gleissolo).
5.  **Interface Cyberpunk:** Design sofisticado com cores neon e modo escuro para melhor experiência do usuário.

## 🛠️ Como Usar

1.  Execute o aplicativo:
    ```bash
    streamlit run app.py
    ```
2.  Na barra lateral (**UPLOAD**):
    *   Faça o upload da foto do **Solo Seco** e/ou **Solo Úmido**.
3.  Ajuste os **PARÂMETROS**:
    *   Algoritmo (K-Means ou Fuzzy C-Means).
    *   Número de Clusters (K).
4.  Clique em **"INICIAR ANÁLISE"**.

## ⚠️ Limitações Importantes

*   **Iluminação:** A precisão da cor depende da qualidade da foto.
*   **Calibração:** Este software não substitui a análise em laboratório.

## 📚 Referências

*   **SiBCS:** Santos, H. G. et al. (2018). Sistema Brasileiro de Classificação de Solos.
*   **Munsell:** Munsell Soil Color Charts.

---
**Desenvolvedor:** Professor Marcelo Claro
