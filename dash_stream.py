import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static

# Carregar os dados
@st.cache_data
def load_data():
    df = pd.read_csv('houses_to_rent_v2.csv')
    return df

df = load_data()

st.title("Dashboard de Aluguel de Casas")

# Filtros interativos
cidade_selecionada = st.sidebar.selectbox("Selecione a cidade", df['city'].unique())
df_cidade = df[df['city'] == cidade_selecionada]

# 1. Gráfico de Barras - Média de Aluguel por Cidade
st.header(f"Média de Aluguel por Cidade")
media_aluguel_cidade = df.groupby('city')['rent amount (R$)'].mean().reset_index()
fig_barras = px.bar(media_aluguel_cidade, x='city', y='rent amount (R$)', title="Média de Aluguel por Cidade")
st.plotly_chart(fig_barras)

# 2. Histograma - Distribuição de Preços de Aluguel
st.header("Distribuição de Preços de Aluguel")
fig_hist = px.histogram(df_cidade, x='rent amount (R$)', nbins=20, title="Distribuição de Preços de Aluguel")
st.plotly_chart(fig_hist)

# 3. Gráfico de Dispersão - Relação entre Área e Preço
st.header(f"Relação entre Área e Preço de Aluguel")
fig_disp = px.scatter(df_cidade, x='area', y='rent amount (R$)', color='furniture', title="Área vs Preço de Aluguel")
st.plotly_chart(fig_disp)

# 4. Gráfico de Barras - Número de Quartos vs Preço de Aluguel
st.header("Número de Quartos vs Preço de Aluguel")
fig_quartos = px.bar(df_cidade, x='rooms', y='rent amount (R$)', title="Número de Quartos vs Preço de Aluguel")
st.plotly_chart(fig_quartos)

# 5. Mapa Interativo - Localização das Casas (sem latitude/longitude, mostrar como exemplo genérico)
st.header("Mapa das Casas para Aluguel (Exemplo)")
# Mapa sem dados de lat/long, criar mapa interativo com cidade como ponto de referência
if cidade_selecionada == 'São Paulo':
    loc = [-23.5505, -46.6333]  # Coordenadas de São Paulo
else:
    loc = [-30.0331, -51.23]  # Coordenadas de Porto Alegre

m = folium.Map(location=loc, zoom_start=12)
folium.Marker(location=loc, popup="Centro").add_to(m)
folium_static(m)

# Exibir a tabela de dados
st.header("Tabela de Dados")
st.write(df_cidade)
