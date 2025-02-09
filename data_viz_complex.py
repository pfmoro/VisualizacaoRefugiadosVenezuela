# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 22:39:07 2025

@author: PC
"""

import pandas as pd
import numpy as np
import plotly.graph_objs as go
import streamlit as st
import plotly.subplots as sp
from statsmodels.tsa.stattools import grangercausalitytests
import data_viz
from scipy.stats import  linregress

def granger_results(gc_res, test='ssr_chi2test'):
    p_values_list = []

# Itera sobre os resultados de cada lag e extrai o p-value do ssr_chi2test
    for lag, results in gc_res.items():
        p_value = results[0][test][1]
        p_values_list.append((lag, p_value))
    
        # Criando o DataFrame
        df_p_values = pd.DataFrame(p_values_list, columns=['lag', 'p_value'])
    return df_p_values

#plotar gráfico com causalidade de granger:
def plot_granger_viz(csv_path, key, var_x, var_y_opt,window=5,maxlag=6):
    # Lê o arquivo CSV
    df_plot = pd.read_csv(csv_path,sep=";",encoding='latin-1')
    var_y=var_y_opt[0]
    df_plot=df_plot[[key, var_x, var_y]].dropna(how='any')
    df_plot[var_x]=df_plot[var_x].astype(float)
    df_plot[var_y]=df_plot[var_y].astype(float)
    #Criar correlação Rolante:
    df_plot['correlacao_rolante']=data_viz.rolling_spearman_slow(df_plot[var_x].astype(float).values,df_plot[var_y].astype(float).values,window=window)
    #residuos de modelo linear ajustado:
    slope, intercept, r_value, p_value, std_err = linregress(df_plot[var_x], df_plot[var_y])
    df_plot['y_pred'] = slope * df_plot[var_x] + intercept
    df_plot['residuos']=df_plot[var_y]-df_plot['y_pred']
    #obtem causalidade de granger:
    gc_res = grangercausalitytests(df_plot[[var_x,var_y]],maxlag=maxlag)
    df_p_values=granger_results(gc_res)
    
    #Usaremos subplots:
    fig = sp.make_subplots(rows=2, cols=2)
    
    # Cria um gráfico de dispersão para var_x
    trace1 = go.Scatter(
        x=df_plot[key],
        y=df_plot[var_x].astype(float),
        mode='lines+markers',
        name=var_x
    )
    
    # Cria um gráfico de dispersão para var_y
    trace2 = go.Scatter(
        x=df_plot[key],
        y=df_plot[var_y].astype(float),
        mode='lines+markers',
        name=var_y
    )
    
    # Gráfico de correlação (usaremos um scatter plot simples para demonstrar)
    trace3 = go.Scatter(
        x=df_plot[key],
        y=df_plot['correlacao_rolante'],
        mode='lines',
        name='Correlação Rolante (Spearman)'
    )
    
    # Gráfico de resíduos
    trace4 = go.Scatter(
        x=df_plot[key],
        y=df_plot['residuos'],
        mode='lines+markers',
        name='Resíduos'
    )
    
    # Gráfico de pvalue dos lags Granger
    trace5 = go.Bar(
        x=df_p_values['lag'],
        y=1-df_p_values['p_value'],
        name='Significância do Atraso (causalidade Granger)'
    )
    
    layout_trace5 = go.Layout(
        xaxis=dict(title='Lag', dtick=1),  # dtick=1 para mostrar todos os lags no eixo x
        yaxis=dict(title='1 - p-value', range=[0, 1], tickformat='.2f'),  # Formata os ticks para 2 casas decimais
        shapes=[
            dict(
                type='line',
                x0=0,
                y0=0.95,
                x1=df_p_values['lag'].max(),
                y1=0.95,
                line=dict(
                    color='red',
                    width=2,
                    dash='dashdot',  # Pode ser 'solid', 'dash', 'dot' ou 'dashdot'
                ),
                layer='below'  # Garante que a linha esteja atrás das barras
            )
        ],
        title='Significância dos Lags na Causalidade de Granger',
        showlegend=False  # Pode ser True se você quiser mostrar a legenda apenas para este subplot
    )
    
    
    # Encontrar os índices onde a correlação em módulo é maior que 0.7
    indices_correlacao_alta = np.where(np.abs(df_plot['correlacao_rolante']) > 0.7)[0]
    
    # Inicializar uma lista para armazenar os intervalos de início e fim
    intervalos = []
    # Encontrar os subintervalos consecutivos
    for i in range(len(indices_correlacao_alta)):
        if i == 0 or indices_correlacao_alta[i] != indices_correlacao_alta[i-1] + 1:
            # Início de um novo intervalo
            inicio = indices_correlacao_alta[i]
        if i == len(indices_correlacao_alta) - 1 or indices_correlacao_alta[i] != indices_correlacao_alta[i+1] - 1:
            # Fim de um intervalo
            fim = indices_correlacao_alta[i]
            intervalos.append((inicio, fim))
    
    # Define os dados que serão plotados
    data = [trace1, trace2, trace3, trace4, trace5]
    fig.add_trace(trace1,row=1, col=1)
    fig.add_trace(trace2,row=1, col=1)
    fig.add_trace(trace3,row=2, col=1)
    fig.add_trace(trace4,row=2, col=2)
    fig.add_trace(trace5,row=1, col=2)
    
    # Adicionando a linha horizontal apenas para o trace5 (segundo subplot)
    fig.add_shape(
        dict(
            x0=0,
            y0=0.95,
            x1=df_p_values['lag'].max(),
            y1=0.95,
            line=dict(
                color='red',
                width=2,
                dash='dashdot',
            ),
        ),
        row=1,
        col=2,
    )
    
    fig.update_layout(height=600, width=800,
                      title_text="Comparação entre {} e {}, mais Correlação e Resíduos".format(var_x, var_y),
                      shapes=[
            # Adicionar uma forma para cada intervalo de alta correlação
            dict(
                type='rect',
                x0=df_plot['Year'].iloc[inicio],
                y0=-1, # Aqui você pode querer ajustar para o mínimo da sua nova variável var_x
                x1=df_plot['Year'].iloc[fim],
                y1=1, # Aqui você pode querer ajustar para o máximo da sua nova variável var_x
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