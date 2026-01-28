import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================================
# CONTROLE DE TAMANHO DOS GRÁFICOS (MEXA AQUI)
# =========================================================
TAMANHO_NUMERO_BARRA = 40    # Os números que ficam em cima/dentro das barras
TAMANHO_LETRAS_EIXOS = 30    # Nomes dos Empurradores e Fornecedores (Eixos X e Y)
TAMANHO_TITULOS_GRAFICO = 35 # Títulos acima dos gráficos
# =========================================================

st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")

# Estilo para os KPIs do topo continuarem gigantes (80px)
st.markdown(f"""
    <style>
    .stApp {{ background-color: #000b1a; color: white; }}
    div[data-testid="stMetricValue"] {{ font-size: 80px !important; font-weight: 900 !important; color: #00ffcc !important; }}
    label[data-testid="stMetricLabel"] {{ font-size: 30px !important; font-weight: bold !important; color: white !important; }}
    </style>
    """, unsafe_allow_html=True)

URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    # Painéis Superiores
    c1, c2 = st.columns(2)
    c1.metric("TOTAL COMPRADO (L)", f"{int(df['QTOS LTS'].sum()):,}".replace(",", "."))
    c2.metric("ABASTECIMENTOS", len(df))

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"<h3 style='text-align:center; font-size:{TAMANHO_TITULOS_GRAFICO}px;'>🚢 LITROS POR EMPURRADOR</h3>", unsafe_allow_html=True)
        resumo_emp = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index()
        fig1 = px.bar(resumo_emp, x='EMPURRADOR', y='QTOS LTS', text_auto='.2s', color_discrete_sequence=['#00ffcc'])
        
        # --- AQUI É ONDE MUDA O QUE VOCÊ CIRCULOU ---
        fig1.update_traces(textfont_size=TAMANHO_NUMERO_BARRA, textposition='outside')
        fig1.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(size=TAMANHO_LETRAS_EIXOS), title=dict(font=dict(size=TAMANHO_LETRAS_EIXOS))),
            yaxis=dict(tickfont=dict(size=TAMANHO_LETRAS_EIXOS), title=dict(font=dict(size=TAMANHO_LETRAS_EIXOS)))
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown(f"<h3 style='text-align:center; font-size:{TAMANHO_TITULOS_GRAFICO}px;'>🏢 RANKING FORNECEDORES</h3>", unsafe_allow_html=True)
        df_forn = df['FORNECEDOR'].value_counts().reset_index()
        fig2 = px.bar(df_forn, x='count', y='FORNECEDOR', orientation='h', text_auto=True, color_discrete_sequence=['#00d4ff'])
        
        # --- AQUI É ONDE MUDA O QUE VOCÊ CIRCULOU ---
        fig2.update_traces(textfont_size=TAMANHO_NUMERO_BARRA, textposition='outside')
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(tickfont=dict(size=TAMANHO_LETRAS_EIXOS), title=dict(font=dict(size=TAMANHO_LETRAS_EIXOS))),
            yaxis=dict(tickfont=dict(size=TAMANHO_LETRAS_EIXOS), title=dict(font=dict(size=TAMANHO_LETRAS_EIXOS)))
        )
        st.plotly_chart(fig2, use_container_width=True)

except Exception as e:
    st.error(f"Erro: {e}")
