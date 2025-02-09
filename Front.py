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
aba1, aba2, aba3, aba4 = st.tabs(["Refugiados Venezuela", "PIB e Petróleo",
                            "PIB e Pauta de Exportação", 
                            "Refugiados e Segurança Institucional"])

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
    st.write("Aqui podemos observar como a economia deste país é dependente do petróleo")
     # Chama a função para plotar o gráfico com as colunas especificadas
    data_viz.plot_corr_chart_from_csv("FullDataset.csv", 'Year', 'GDP Variation', 'Crude Oil Year Average Variation %')
    data_viz.plot_hybrid_chart_from_csv("FullDataset.csv", 'Year', 'GDP', 'Mineral fuels, mineral oils and products of their distillation','Other')
    
    
# Conteúdo da Aba 3
with aba3:
    st.header("Conteúdo da Aba 3")
    st.write("Na terceira aba, podemos incluir informações adicionais ou configurações.")
    data_viz_complex.plot_granger_viz("FullDataset.csv", 'Year', 'refugees normalized', ['Crude Oil Year Average Variation %',
       'Crude Oil Year Average Variation % Lag +',
       'Crude Oil Year Average Variation % Lag 2+',
       'Crude Oil Year Average Variation % Lag 3+'],window=5,maxlag=6)
with aba4:
    st.header("Conteúdo da Aba 4")
    data_viz.plot_scatter_from_csv("FullDataset.csv", 'Year', 'Refugees Venezuela', 'Corruption Perception Index', 'Democracy Index')