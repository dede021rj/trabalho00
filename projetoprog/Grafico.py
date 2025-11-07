import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==============================
# 1️⃣ Leitura dos dados
# ==============================
caminho_csv = "bq-results-20251105-191211-1762369940755.csv"

# Tenta carregar o CSV e mostra erro se não for encontrado
try:
    df = pd.read_csv(caminho_csv)
except FileNotFoundError:
    st.error("❌ Arquivo CSV não encontrado. Coloque o arquivo na mesma pasta do app.")
    st.stop()

# ==============================
# 2️⃣ Título e introdução
# ==============================
st.title("📊 Comparativo de Despesa Total / PIB por Estado")
st.write("""
Este aplicativo permite comparar o percentual de **Despesa Total em relação ao PIB** 
entre **dois estados brasileiros** em um determinado ano.
""")

# ==============================
# 3️⃣ Seleção dos filtros
# ==============================
if not {"sigla_uf", "ano", "despesa_total_pib"}.issubset(df.columns):
    st.error("⚠️ O arquivo CSV não contém as colunas necessárias: 'sigla_uf', 'ano' e 'despesa_total_pib'.")
    st.stop()

# Remove valores ausentes e organiza
df = df.dropna(subset=["sigla_uf", "ano", "despesa_total_pib"])
estados = sorted(df["sigla_uf"].unique())
anos = sorted(df["ano"].unique())

col1, col2 = st.columns(2)
with col1:
    estado1 = st.selectbox("Selecione o primeiro estado:", estados, index=0)
with col2:
    estado2 = st.selectbox("Selecione o segundo estado:", estados, index=1)

ano = st.selectbox("Selecione o ano:", anos, index=len(anos) - 1)

# ==============================
# 4️⃣ Filtra os dados
# ==============================
df_filtrado = df[(df["sigla_uf"].isin([estado1, estado2])) & (df["ano"] == ano)]

if df_filtrado.empty:
    st.warning("⚠️ Não há dados disponíveis para essa combinação de estados e ano.")
else:
    # ==============================
    # 5️⃣ Criação do gráfico
    # ==============================
    fig, ax = plt.subplots(figsize=(8, 4))
    cores = ["#1f77b4", "#ff7f0e"]

    barras = ax.bar(df_filtrado["sigla_uf"], df_filtrado["despesa_total_pib"] * 100, color=cores)

    for i, v in enumerate(df_filtrado["despesa_total_pib"]):
        ax.text(i, v * 100 + 0.02, f"{v * 100:.2f}%", ha="center", fontweight="bold")

    ax.set_title(f"Percentual da Despesa Total em relação ao PIB ({ano})", fontsize=14, pad=15)
    ax.set_xlabel("Estado")
    ax.set_ylabel("Despesa Total / PIB (%)")

    st.pyplot(fig)

    # ==============================
    # 6️⃣ Exibe tabela com dados
    # ==============================
    st.write("### 🔢 Dados utilizados")
    st.dataframe(df_filtrado[["sigla_uf", "ano", "despesa_total_pib"]])
