import pandas as pd
import streamlit as st
import plotly.express as px

# Função para formatar valores no padrão brasileiro
def formatar_moeda_brasileira(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# Carrega o DataFrame
vendas_df = pd.read_excel("faturamento_multinacional.xlsx")

# Remove espaços extras nos nomes das colunas
vendas_df.columns = vendas_df.columns.str.strip()

# Lista das colunas financeiras
colunas_moedas = [
    "Preço Unitário (R$)", "Receita Bruta (R$)", "Custo do Produto (R$)", 
    "Margem de Lucro (R$)", "Descontos Aplicados (R$)", "Impostos (R$)", "Receita Líquida (R$)"
]

# Filtra apenas colunas que existem no DataFrame
colunas_existentes = [col for col in colunas_moedas if col in vendas_df.columns]

# Verifica se as colunas necessárias existem no DataFrame vendas_df
colunas_necessarias = ["Receita Líquida (R$)", "Custo do Produto (R$)", "Impostos (R$)", "País"]
for col in colunas_necessarias:
    if col not in vendas_df.columns:
        print(f"Erro: A coluna '{col}' não existe no DataFrame.")

# Cria uma nova coluna no DataFrame vendas_df chamada "Lucro País(R$)"
vendas_df["Lucro País(R$)"] = vendas_df["Receita Líquida (R$)"] - vendas_df["Custo do Produto (R$)"] - vendas_df["Impostos (R$)"]

# Agrupa o DataFrame vendas_df pela coluna "País"
df_agrupado = vendas_df.groupby('País').agg({
    "Receita Líquida (R$)": "sum",  # Soma a "Receita Líquida (R$)" para cada país.
    "Lucro País(R$)": "sum"         # Soma o "Lucro País(R$)" para cada país.
}).reset_index()

# Agrupa o DataFrame vendas_df pela coluna "País" e soma a "Quantidade Vendida"
df_quantidade_vendas_por_pais = vendas_df.groupby("País").agg({
    "Quantidade Vendida": "sum"
}).reset_index()

# Renomeia a coluna "Quantidade Vendida" para "Total Quantidade Vendida"
df_quantidade_vendas_por_pais = df_quantidade_vendas_por_pais.rename(columns={
    "Quantidade Vendida": "Total Quantidade Vendida"
})

# Agrupa o DataFrame vendas_df pelas colunas "País" e "Produto"
df_quantidade_produtos_por_pais = vendas_df.groupby(['País', 'Produto']).agg({
    "Quantidade Vendida": "sum"  # Soma a quantidade vendida por país e produto.
}).reset_index()

# Renomeia a coluna "Quantidade Vendida" para "Total Quantidade Vendida"
df_quantidade_produtos_por_pais = df_quantidade_produtos_por_pais.rename(columns={
    "Quantidade Vendida": "Total Quantidade Vendida"
})

# Aplica a formatação para as colunas monetárias
colunas_monetarias = ["Receita Líquida (R$)", "Custo do Produto (R$)", "Impostos (R$)", "Lucro País(R$)", "Total Quantidade Vendida"]
for col in colunas_monetarias:
    if col in df_agrupado.columns:
        df_agrupado[col] = df_agrupado[col].apply(formatar_moeda_brasileira)
    if col in df_quantidade_vendas_por_pais.columns:
        df_quantidade_vendas_por_pais[col] = df_quantidade_vendas_por_pais[col].apply(formatar_moeda_brasileira)
    if col in df_quantidade_produtos_por_pais.columns:
        df_quantidade_produtos_por_pais[col] = df_quantidade_produtos_por_pais[col].apply(formatar_moeda_brasileira)
    if col in vendas_df.columns:
        vendas_df[col] = vendas_df[col].apply(formatar_moeda_brasileira)

# Exibe os DataFrames formatados
print("DataFrame Agrupado:")
print(df_agrupado)

print("\nDataFrame de Quantidade de Vendas por País:")
print(df_quantidade_vendas_por_pais)

print("\nDataFrame de Quantidade de Vendas por Produto e País:")
print(df_quantidade_produtos_por_pais)

print("\nDataFrame Original (Vendas Detalhadas):")
print(vendas_df)

# Exibe os DataFrames no Streamlit
st.title("Dashboard de Vendas")

st.header("Total de Vendas por País")
st.dataframe(df_quantidade_vendas_por_pais)

st.header("Vendas por Produto e País")
st.dataframe(df_quantidade_produtos_por_pais)

st.header("Lucro por País")
st.dataframe(df_agrupado)

st.header("Dados Detalhados de Vendas")
st.dataframe(vendas_df)