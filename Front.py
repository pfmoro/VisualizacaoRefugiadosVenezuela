# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 08:40:34 2025

@author: PC
"""
# app.py
import streamlit as st
import data_viz
import data_viz_complex

# Cria as abas
aba1, aba2, aba3, aba4, aba5 = st.tabs(["Refugiados Venezuela", "PIB e Petróleo",
                            "Refugiados e Petróleo", 
                            "Refugiados e Segurança Institucional",
                            "Conclusão"])

# Conteúdo da Aba 1
with aba1:
    st.header("Crise de Refugiados na Venezuela")
    st.write("Seja bem vindo(a), esta é uma jornada pela crise de refugiados venzuelana")
    st.write("Nesta ferramenta exploraremos dados que oferecem insights sobre as causas da crise e uma visão da situação atual")
    st.write("Siga pelas demais abas, nesta jornada guiada")

# Conteúdo da Aba 2
with aba2:
    st.header("PIB Venezuela e Preço do Petróleo ")
    st.write("Exibimos aqui um comparativo da correlação entre o PIB da Venezuela e o preço do petróleo")
    st.write("e uma evolução do volume de exportações da venezuela coma  representatividade do petroleo")
    st.write("Aqui podemos observar como a economia deste país é dependente do petróleo")
     # Chama a função para plotar o gráfico com as colunas especificadas
    data_viz.plot_corr_chart_from_csv("FullDataset.csv", 'Year', 'GDP Variation', 'Crude Oil Year Average Variation %')
    st.write("abaixo vemos a evolução do volume exportado pela venezuela e como o volume de petróleo vem perdendo signficância")
    data_viz.plot_hybrid_chart_from_csv("FullDataset.csv", 'Year', 'GDP', 'Mineral fuels, mineral oils and products of their distillation','Other')
    
    
# Conteúdo da Aba 3
with aba3:
    st.header("Refugiados e Petróleo")
    st.write("Nesta aba usaremos causalidade de granger, para mostrar que o pétroleo e PIB impactaram o volume de refugiados")
    st.write("É possível notar que a variação do preço do petróleo antecipa movimentos de refugiados, como pode ser visto")
    st.write("pela significância da causalidade de granger")
    data_viz_complex.plot_granger_viz("FullDataset.csv", 'Year', 'refugees normalized', ['Crude Oil Year Average Variation %',
       'Crude Oil Year Average Variation % Lag +',
       'Crude Oil Year Average Variation % Lag 2+',
       'Crude Oil Year Average Variation % Lag 3+'],window=5,maxlag=6)
with aba4:
    st.header("Refugiados e Segurança institucional")
    st.write("As primeiras visualizações mostram uma causa econômica para a crise venezuelana")
    st.write("Todavia é simplista achar que esta é a única causa para um evento tão complexo")
    st.write("Aqui usaremos os indices de democracia da The Economist")
    st.write("e o índice de percepção de corrupção da transparência internacional")
    st.write("para mostrar que o volume de refugiados começou seu crescimento")
    st.write("juntamente com a queda da venezuela nestes dois rankings")
    data_viz.plot_scatter_from_csv("FullDataset.csv", 'Year', 'Refugees Venezuela', 'Corruption Perception Index', 'Democracy Index')

with aba5:
    st.header("Conclusão")
    st.write("Nossos dados mostram que a crise de refugiados venezuelana")
    st.write("Apresenta causas econômicas e políticas")
    st.write("A solução para este crise passa pela resolução dos desafios")
    st.write("institucionais do país e também por uma reconstrução econômica do mesmo")