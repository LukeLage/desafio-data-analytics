## Importação de bibliotecas usadas nesse projeto

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import plotly.express as px

## Carregamento dos dados
df = pd.read_csv('data\customer_shopping_data.csv')
print(df.head())

st.title('Desafio Data Analytics - InsightFlow')
st.write('Desafio final do Projeto Desenvolve Itabira, onde os alunos assumem o papel de analistas de dados e são desafiados a extrair insights valiosos para um e-commerce e responder perguntas estratéficas.')

## Análise de dados
print(df.describe())
print(df.info())

print('Quantidade de pedidos feitos em geral: ', df['invoice_no'].nunique())