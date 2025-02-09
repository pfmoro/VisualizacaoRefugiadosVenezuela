# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 09:04:10 2025

@author: PC
"""

# data_viz.py
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import streamlit as st
from scipy.stats import spearmanr
from numpy.lib.stride_tricks import as_strided
from numpy.lib import pad
import plotly.subplots as sp

def rolling_spearman_slow(seqa, seqb, window):
    stridea = seqa.strides[0]
    ssa = as_strided(seqa, shape=[len(seqa) - window + 1, window], strides=[stridea, stridea])
    strideb = seqa.strides[0]
    ssb = as_strided(seqb, shape=[len(seqb) - window + 1, window], strides =[strideb, strideb])
    corrs = [spearmanr(a, b)[0] for (a,b) in zip(ssa, ssb)]
    return pad(corrs, (window - 1, 0), 'constant', constant_values=np.nan)

def plot_scatter_from_csv(csv_path, key, y_col1, y_col2,y_col3):
    # Lê o arquivo CSV
    df = pd.read_csv(csv_path,sep=";",encoding='latin-1')
    
    # Remove linhas com NaN nas colunas especificadas para plotagem
    df_plot = df[[key, y_col1, y_col2, y_col3]].dropna(how='any')
    
    # Cria um gráfico de dispersão para a primeira coluna Y
    trace1 = go.Scatter(
        x=df_plot[key],
        y=df_plot[y_col1].astype(float),
        mode='lines+markers',
        name=y_col1
    )
    
    # Cria um gráfico de dispersão para a segunda coluna Y
    trace2 = go.Scatter(
        x=df_plot[key],
        y=df_plot[y_col2].astype(float),
        mode='lines+markers',
        name=y_col2
    )
    # Cria um gráfico de dispersão para a segunda coluna Y
    trace3 = go.Scatter(
        x=df_plot[key],
        y=df_plot[y_col3].astype(float),
        mode='lines+markers',
        name=y_col3
    )
    #Usaremos subplots:
    fig = sp.make_subplots(rows=3, cols=1)
    fig.update_layout(height=600, width=800,
    barmode='stack',
    title='Numero de Refugiados e indices de segurança institucional',
    )
    
    # Define os dados que serão plotados

    fig.add_trace(trace1,row=1, col=1)
    fig.add_trace(trace2,row=2, col=1)
    fig.add_trace(trace3,row=3, col=1)
    
    # Plota o gráfico no Streamlit
    st.plotly_chart(fig)

# A função pode ser chamada passando o caminho do arquivo CSV e as colunas desejadas
# Por exemplo, se o arquivo CSV se chama 'dados.csv', e as colunas são 'Year', 'GDP Variation', 'Crude Oil Year Average Variation %'
# plot_scatter_from_csv('dados.csv', 'Year', 'GDP Variation', 'Crude Oil Year Average Variation %')

def plot_corr_chart_from_csv(csv_path, x_col, y_col1, y_col2, window=5):
    # Lê o arquivo CSV
    df = pd.read_csv(csv_path,sep=";",encoding='latin-1')
    
    # Remove linhas com NaN nas colunas especificadas para plotagem
    df_plot = df[[x_col, y_col1, y_col2]].dropna(how='any')
    
    # Converte as colunas para float
    df_plot[y_col1] = df_plot[y_col1].astype(float)
    df_plot[y_col2] = df_plot[y_col2].astype(float)
    
    # Calcula a correlação rolante e os resíduos
    df_plot['correlacao_rolante'] = rolling_spearman_slow(df_plot[y_col1].values, df_plot[y_col2].values, window)
    df_plot['residuos'] = df_plot[y_col1] - df_plot[y_col2]

    # Cria a figura com subplots
    fig = sp.make_subplots(rows=3, cols=1, subplot_titles=(y_col1, y_col2, 'Correlação Rolante', 'Resíduos'))

    # Adiciona os traços para os dois primeiros gráficos de dispersão
    trace1 = go.Scatter(x=df_plot[x_col], y=df_plot[y_col1], mode='lines+markers', name=y_col1)
    trace2 = go.Scatter(x=df_plot[x_col], y=df_plot[y_col2], mode='lines+markers', name=y_col2)
    fig.add_trace(trace1, row=1, col=1)
    fig.add_trace(trace2, row=1, col=1)

    # Adiciona o gráfico da correlação rolante
    trace3 = go.Scatter(x=df_plot[x_col][window-1:], y=df_plot['correlacao_rolante'], mode='lines', name='Correlação Rolante (Spearman)')
    fig.add_trace(trace3, row=2, col=1)

    # Adiciona o gráfico de resíduos
    trace4 = go.Scatter(x=df_plot[x_col], y=df_plot['residuos'], mode='lines+markers', name='Resíduos')
    fig.add_trace(trace4, row=3, col=1)

    # Encontrar os índices onde a correlação em módulo é maior que 0.7
    indices_correlacao_alta = np.where(np.abs(df_plot['correlacao_rolante']) > 0.7)[0]
    intervalos = []
    for i in range(len(indices_correlacao_alta)):
        if i == 0 or indices_correlacao_alta[i] != indices_correlacao_alta[i-1] + 1:
            inicio = indices_correlacao_alta[i]
        if i == len(indices_correlacao_alta) - 1 or indices_correlacao_alta[i] != indices_correlacao_alta[i+1] - 1:
            fim = indices_correlacao_alta[i]
            intervalos.append((inicio, fim))

    # Atualiza o layout com as formas para destacar os intervalos de alta correlação
    fig.update_layout(height=800, width=1000,
                      title_text="Comparação entre Variação do PIB e do Preço do Petróleo, mais Correlação e Resíduos",
                      shapes=[
                          dict(
                              type='rect',
                              x0=df_plot[x_col].iloc[inicio],
                              y0=min(df_plot[y_col1].min(), df_plot[y_col2].min()),
                              x1=df_plot[x_col].iloc[fim],
                              y1=max(df_plot[y_col1].max(), df_plot[y_col2].max()),
                              fillcolor='Lightgrey',
                              opacity=0.5,
                              line=dict(
                                  width=0,
                              ),
                          )
                          for inicio, fim in intervalos
                      ]
    )

    # Plota o gráfico no Streamlit
    st.plotly_chart(fig)
    
def plot_hybrid_chart_from_csv(csv_path, var_x, var_y, var_y_2,var_y_3, window=5, adjust=True):
    # Lê o arquivo CSV
    df_plot = pd.read_csv(csv_path,sep=";",encoding='latin-1')
    df_plot[var_x]=df_plot[var_x].astype(float)
    if adjust:
        df_plot[var_y]=df_plot[var_y].astype(float)*1e6 #Ajuste de ordem de grandeza do PIB  
    
    # Remove linhas com NaN nas colunas especificadas para plotagem
    df_plot = df_plot[[var_x, var_y, var_y_2,var_y_3]].dropna(how='any')
    
    #Usaremos subplots:
    fig = sp.make_subplots(rows=2, cols=1)
    
    #Cria um gráfico de dispersão para var_x
    trace1 = go.Scatter(
        x=df_plot[var_x],
        y=df_plot[var_y].astype(float),
        mode='lines+markers',
        name=var_x
    )
    
    # Gráfico de Exportação venezuela
    trace2 = go.Bar(
        x=df_plot[var_x],
        y=df_plot[var_y_2],
        name='Mineral Fuels',
    )
    
    trace3 = go.Bar(
        x=df_plot[var_x],
        y=df_plot[var_y_3],
        name='Other Products',
    )
    
    fig.update_layout(height=600, width=800,
        barmode='stack',
        title='Pauta de exportação venezuelana e PIB',
    )
    
    # Define os dados que serão plotados
    #data = [trace1, trace2, trace3]
    fig.add_trace(trace1,row=2, col=1)
    fig.add_trace(trace2,row=1, col=1)
    fig.add_trace(trace3,row=1, col=1)

     # Plota o gráfico no Streamlit
    st.plotly_chart(fig)