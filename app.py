import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Carregando a logo
logo = Image.open('logo.png')

def create_df_analitico():
    df = pd.read_csv('gborpgto.csv')
    df.columns = df.columns.str.strip()  # Limpeza dos nomes das colunas
    
    # Remoção dos pontos dos números e conversão para tipo numérico
    df['Valor_Recebido'] = pd.to_numeric(df['Valor_Recebido'].str.replace('.', '').str.replace(',', '.'))
    df['Encargos'] = pd.to_numeric(df['Encargos'].str.replace('.', '').str.replace(',', '.'))
    df['comissao'] = pd.to_numeric(df['comissao'].str.replace('.', '').str.replace(',', '.'))

    return df

# Carregando o DataFrame
df = create_df_analitico()

# Valor total recuperado (soma do campo Valor Recebido)
valor_total_recuperado = df['Valor_Recebido'].sum()

# Valor dos juros recuperados pela portes (soma campo Encargos)
valor_juros_recuperados = df['Encargos'].sum()

# Remuneracao Portes (soma campo comissao)
remuneracao_portes = df['comissao'].sum()

# Quantidade de Clientes Pagos (contagem de linhas do arquivo)
quantidade_clientes_pagos = df.shape[0]

# Exibição dos cards com os valores filtrados
st.sidebar.image(logo)

# Título com a cor cinza
st.markdown("<h1 style='color: grey;'>Análise UNIMED</h1>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("**Valor Recup** R$ {:.2f}".format(float(valor_total_recuperado)))

with col2:
    st.info("**Juros Recup** R$ {:.2f}".format(float(valor_juros_recuperados)))

with col3:
    st.info("**Remuneração** R$ {:.2f}".format(float(remuneracao_portes)))

with col4:
    st.info("**Clientes Pagos** {}".format(quantidade_clientes_pagos))

# Convertendo a coluna 'Data_Pagamento' para o tipo datetime
df['Data_Pagamento'] = pd.to_datetime(df['Data_Pagamento'])

# Sumarizando os valores por dia
df_sumarizado = df.groupby('Data_Pagamento').agg({'Valor_Recebido': 'sum', 'Encargos': 'sum'}).reset_index()

# Criando um subplot com dois eixos y
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Adicionando a linha de Valor Recebido no eixo y1
fig.add_trace(go.Scatter(x=df_sumarizado['Data_Pagamento'], y=df_sumarizado['Valor_Recebido'], mode='lines', name='Valor Recup', line=dict(color='blue')))

# Adicionando a linha de Encargos no eixo y2
fig.add_trace(go.Scatter(x=df_sumarizado['Data_Pagamento'], y=df_sumarizado['Encargos'], mode='lines', name='Juros', line=dict(color='red')), secondary_y=True)

# Configurando layout
fig.update_layout(title='Valor Recup. mais Juros por Dia',
                  yaxis=dict(title='Valor Recup. (R$)', titlefont=dict(color='blue')),  # Configurações do eixo y1
                  yaxis2=dict(title='Juros Recup. (R$)', titlefont=dict(color='red'), overlaying='y', side='right'))  # Configurações do eixo y2

# Exibindo o gráfico
st.plotly_chart(fig)

# Gráfico de barras estilo funil do valor recuperado pelo campo 'Remunerado'
df_funil = df.groupby('Remunerado').size().reset_index(name='Count')
df_funil['Percentual'] = df_funil['Count'] / df_funil['Count'].sum() * 100

fig_funil = px.funnel(df_funil, x='Percentual', y='Remunerado', title='Funil Recuperado/Remunerado"')
fig_funil.update_layout(yaxis_title='Remunerado', xaxis_title='Percentual (%)')
st.plotly_chart(fig_funil)

##

# Criando um DataFrame para os totais de Encargos e Comissao
df_totais = pd.DataFrame({
    'Tipo': ['Juros', 'Comissao'],
    'Total': [valor_juros_recuperados, remuneracao_portes]
})

# Criando o gráfico de barras
fig_barras = px.bar(df_totais, x='Tipo', y='Total', color='Tipo', title='Totais de Juros pagam 70.21% Comissao')

# Configurando o layout do gráfico de barras
fig_barras.update_layout(xaxis_title='Tipo', yaxis_title='Total (R$)')

# Exibindo o gráfico de barras
st.plotly_chart(fig_barras)

##

# Convertendo a coluna 'Atraso' para o tipo numérico
df['Atraso'] = pd.to_numeric(df['Atraso'])

# Criando o boxplot horizontal
fig_boxplot_horizontal = px.box(df, x='Atraso', orientation='h', title='Boxplot Horizontal do Atraso')

# Exibindo o boxplot horizontal
st.plotly_chart(fig_boxplot_horizontal)

##

# Carregando o arquivo CSV com os dados sumarizados e ordenados
df_sumarizado_ordenado = pd.read_csv('acao.csv')

# Criando o gráfico de rosca (donut chart) com o Plotly Express
fig = px.pie(df_sumarizado_ordenado, values='Valor', names='Ação', title='Gráfico de Rosca (Donut Chart) - Percentual por Ação', hole=0.5)

# Personalizando o layout do gráfico
fig.update_traces(textinfo='percent+label', pull=[0.1] * len(df_sumarizado_ordenado))

# Exibindo o gráfico diretamente no app Streamlit
st.plotly_chart(fig)

