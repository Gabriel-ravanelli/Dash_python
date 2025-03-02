import streamlit as st
import plotly.express as px
from Medidas import vendas_df, df_quantidade_vendas_por_pais, df_quantidade_produtos_por_pais, df_agrupado

# Configuração do Streamlit
st.title("Dash de Vendas")

# Gráfico 1: Total de vendas por país
st.header("Total de Vendas por País")
fig1 = px.bar(df_quantidade_vendas_por_pais, x="País", y="Total Quantidade Vendida", title="Total de Vendas por País")
st.plotly_chart(fig1)

# Gráfico 2: Vendas por produto e país
st.header("Vendas por Produto e País")
fig2 = px.bar(df_quantidade_produtos_por_pais, x="País", y="Total Quantidade Vendida", color="Produto", barmode="group", title="Vendas por Produto e País")
st.plotly_chart(fig2)

# Gráfico 3: Lucro por país
st.header("Lucro por País")
fig3 = px.bar(df_agrupado, x="País", y="Lucro País(R$)", title="Lucro por País")
st.plotly_chart(fig3)

# Tabela: Dados detalhados
st.header("Dados Detalhados de Vendas")
st.dataframe(vendas_df)

