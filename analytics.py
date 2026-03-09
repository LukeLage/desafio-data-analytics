## Importação de bibliotecas usadas nesse projeto

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px
import sqlite3

# Coneção com o banco de dados SQLite
data = pd.read_csv('data/customer_shopping_data.csv')
conn = sqlite3.connect('data/customer_shopping_data.db')
data.to_sql('customer_shopping_data', conn, if_exists='replace', index=False)

## Carregamento dos dados
df = pd.read_sql_query('SELECT * FROM customer_shopping_data', conn)
df['invoice_date'] = pd.to_datetime(df['invoice_date'], format='%d/%m/%Y')
print(df.head()) 

## Análise de dados
print(df.describe())
print(df.info())

df['seasons'] = df['invoice_date'].dt.month % 12 // 3 + 1
df['seasons'] = df['seasons'].map({1: 'Verão', 2: 'Outono', 3: 'Inverno', 4: 'Primavera'})

print(df['seasons'].value_counts())

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
            ['Moda faixa étaria', 'Número de Clientes por Gênero', 'Faixa étaria média'],
        )
    
    estacao_container = st.container(border = True)
    with estacao_container:
        vendas_estacao = st.select_slider(
            'Vendas baseadas nas estações: ',
            options= df['seasons'].unique().tolist()
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

# Métricas apresentadas em formato de cards, usando a função st.metric do Streamlit

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
        if opcoes_metricas_clientes == 'Número de Clientes por Gênero':
            clientes_genero = df['gender'].value_counts()
            st.metric (label=clientes_genero.index[0], value=clientes_genero.values[0])
            st.metric (label=clientes_genero.index[1], value=clientes_genero.values[1])
        elif opcoes_metricas_clientes == 'Faixa étaria média':
            media_idade = df['age'].mean()
            st.metric(label='Faixa Etária Média', value=f'{media_idade:.2f} anos')
        elif opcoes_metricas_clientes == 'Moda faixa étaria':
            moda_idade = df['age'].mode()[0]
            st.metric(label='Faixa Etária Moda', value=f'{moda_idade} anos')

with informacoes_basicas3:
    metricas_estacoes = st.container(border = True)
    with metricas_estacoes:
        st.header('Vendas por Estação (Milhões)')
        if vendas_estacao == 'Verão':
            vendas_verao = (df[df['seasons'] == 'Verão']['price'] * 
            df[df['seasons'] == 'Verão']['quantity']).sum()
            st.metric(label='Vendas no Verão', value=f'R$ {vendas_verao / 1000000:.2f}')
        elif vendas_estacao == 'Outono':
            vendas_outono = (df[df['seasons'] == 'Outono']['price'] * 
            df[df['seasons'] == 'Outono']['quantity']).sum()
            st.metric(label='Vendas no Outono', value=f'R$ {vendas_outono / 1000000:.2f}')
        elif vendas_estacao == 'Inverno':
            vendas_inverno = (df[df['seasons'] == 'Inverno']['price'] * 
            df[df['seasons'] == 'Inverno']['quantity']).sum()
            st.metric(label='Vendas no Inverno', value=f'R$ {vendas_inverno / 1000000:.2f}')
        elif vendas_estacao == 'Primavera':
            vendas_primavera = (df[df['seasons'] == 'Primavera']['price'] * 
            df[df['seasons'] == 'Primavera']['quantity']).sum()
            st.metric(label='Vendas na Primavera', value=f'R$ {vendas_primavera / 1000000 :.2f}')

# Gráficos usados para visualização de dados

grafico1, grafico2 = st.columns(2)

with grafico1:
    metodo_pagamento = df['payment_method'].value_counts()
    fig1 = px.pie(metodo_pagamento, values=metodo_pagamento.values, names=metodo_pagamento.index, title='Métodos de Pagamento')
    st.plotly_chart(fig1)
with grafico2:
    localidades = df['shopping_mall'].value_counts()
    fig2 = px.bar(localidades, x=localidades.index, y=localidades.values, title='Localidades de Compras dos Clientes', labels={'x': 'Localidade', 'y': 'Número de Clientes'})
    st.plotly_chart(fig2)

# Fechando a conexão com o banco de dados
conn.close()