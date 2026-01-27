import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Painel Fiscal", layout="wide")

# Conexão direta com a sua planilha
ID_PLANILHA = "1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc"
URL = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv"

st.title("📊 Dashboard Gestão de Combustível")

try:
    # Lendo os dados
    df = pd.read_csv(URL)
    
    # LIMPEZA AUTOMÁTICA: Remove espaços em branco antes ou depois dos nomes das colunas
    df.columns = df.columns.str.strip()

    # Criando os Cards de resumo (KPIs)
    c1, c2 = st.columns(2)
    c1.metric("Total de Lançamentos", len(df))
    # Somando a coluna exata da sua planilha
    if 'QTOS LTS' in df.columns:
        c2.metric("Volume Total (Lits)", f"{df['QTOS LTS'].sum():,.0f}")

    st.markdown("---")

    # Gráfico 1: Volume por Empurrador
    if 'EMPURRADOR' in df.columns and 'QTOS LTS' in df.columns:
        st.subheader("⛽ Volume por Empurrador")
        fig_bar = px.bar(df, x='EMPURRADOR', y='QTOS LTS', color='EMPURRADOR', text_auto='.2s')
        st.plotly_chart(fig_bar, use_container_width=True)

    # Gráfico 2: Distribuição por Estado
    if 'ESTADO' in df.columns:
        st.subheader("🗺️ Consumo por Estado")
        fig_pie = px.pie(df, values='QTOS LTS', names='ESTADO', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

except Exception as e:
    st.error(f"Erro na leitura dos dados: {e}")
    st.info("Dica: Verifique se a coluna 'QTOS LTS' está escrita exatamente assim na sua planilha Google.")
