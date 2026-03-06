## Importação de bibliotecas usadas nesse projeto

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px

## Carregamento dos dados
df = pd.read_csv('data\customer_shopping_data.csv')
df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%d/%m/%Y')
print(df.head()) 

## Análise de dados
print(df.describe())
print(df.info())

# Visualização de dados
st.title('Desafio Data Analytics - InsightFlow')

# Sidebar do app de vizualização de dados

sidebar = st.sidebar
with sidebar:
    st.header('Para melhor entendimento do projeto')
    
    informacoes = st.container()
    with informacoes: 
        informacoes_click = st.button('Informações do Projeto')
        limpar_click = st.button('Limpar Informações', type = 'primary')

    metricas_vendas = st.container(border = True)
    with metricas_vendas: 
        opcoes_metricas_vendas = st.radio(
            'Selecione a métrica de vendas que deseja visualizar: ',
            ['Total de Vendas', 'Média de Vendas por Cliente', 'Média Gasta por Cliente'],
        )
        
    metricas_clientes = st.container(border = True)
    with metricas_clientes:
        opcoes_metricas_clientes = st.radio(
            'Selecione a métrica de clientes que deseja visualizar: ',
            ['Número de Clientes por Gênero', 'Faixa étaria média', 'Número de Clientes'],
        )
    
    data_compras = st.container(border = True)
    with data_compras:
        slider_data_compras = st.select_slider(
            'Selecione o intervalo de datas que deseja analisar: ',
            options= df['invoice_date'].unique(), 
            value = (df['invoice_date'].min(), df['invoice_date'].max())
        )

    contatos = st.container(border = True)
    with contatos: 
        st.write('Contatos:')
        st.write('LinkedIn: https://www.linkedin.com/in/luke-malaquias-lage-04022a232/')
        st.write('GitHub: https://github.com/LukeLage')
        st.write('E-mail: lukelage646@gmail.com')

if informacoes_click:
    st.write('Desafio final do Projeto Desenvolve Itabira, onde os alunos assumem o papel de analistas de dados e são desafiados a extrair insights valiosos para um e-commerce e responder perguntas estratéficas.')
    st.write('Feito por Luke Malaquias Lage')
if limpar_click:
    st.write('')

informacoes_basicas1, informacoes_basicas2, informacoes_basicas3 = st.columns(3)

with informacoes_basicas1: 
    metricas_vendas = st.container(border = True)
    with metricas_vendas:
        st.header('Métricas de Vendas')
        if opcoes_metricas_vendas == 'Total de Vendas':
            total_vendas = df['invoice_no'].count()
            st.metric(label='Total de Vendas', value=total_vendas)
        elif opcoes_metricas_vendas == 'Média de Vendas por Cliente':
            media_vendas_cliente = df.groupby('customer_id')['invoice_no'].count().mean()
            st.metric(label='Média de Vendas por Cliente', value=media_vendas_cliente)
        elif opcoes_metricas_vendas == 'Média Gasta por Cliente':
            df['gasto'] = df['price'] * df['quantity']
            media_gasto_cliente = df.groupby('customer_id')['gasto'].mean().mean()
            st.metric(label='Média Gasta por Cliente', value=f'R$ {media_gasto_cliente:.2f}')

with informacoes_basicas2: 
    metricas_clientes = st.container(border = True)
    with metricas_clientes:
        st.header('Métricas de Clientes')
        

with informacoes_basicas3: 
    data_compras = st.container(border = True)
    with data_compras: 
        st.header('Vendas por Intervalo')
        df_filtrado = df[(df['invoice_date'] >= slider_data_compras[0]) & (df['invoice_date'] <= slider_data_compras[1])]
        valor_vendas = (df_filtrado['price'] * df_filtrado['quantity']).sum()
        quantidade_vendas = df_filtrado['quantity'].sum()
        st.metric(label='Total de Vendas', value=f'R$ {valor_vendas:.2f}')
        st.metric(label='Quantidade Vendida', value=quantidade_vendas)

descrepancia_genero = df['gender'].value_counts()
fig_genero = px.pie(values=descrepancia_genero.values, names=descrepancia_genero.index, title='Descrepância de Gênero')
st.plotly_chart(fig_genero)