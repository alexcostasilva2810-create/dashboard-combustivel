import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")
st.cache_data.clear()

# --- AQUI É ONDE VOCÊ MEXE NO TAMANHO ---
TAMANHO_NUMERO = "80px"       # Mude para 90px, 100px se quiser maior
TAMANHO_LEGENDA = "35px"      # Texto em cima do número
COR_NUMERO = "#00ffcc"        # Verde Neon
COR_FUNDO_CARD = "#001529"    # Azul Escuro

st.markdown(f"""
    <style>
    .stApp {{ background-color: #000b1a; color: white; }}
    
    /* ESTILO DO CARD */
    div[data-testid="stMetric"] {{
        background-color: {COR_FUNDO_CARD}; border: 4px solid #00d4ff;
        border-radius: 25px; padding: 50px !important; text-align: center;
    }}

    /* ESTILO DO NÚMERO (O DADO) */
    div[data-testid="stMetricValue"] {{
        font-size: {TAMANHO_NUMERO} !important; 
        font-weight: 900 !important; 
        color: {COR_NUMERO} !important;
    }}

    /* ESTILO DA LEGENDA (O TEXTO) */
    label[data-testid="stMetricLabel"] {{ 
        font-size: {TAMANHO_LEGENDA} !important; 
        font-weight: 800 !important;
        color: white !important;
    }}
    </style>
    """, unsafe_allow_html=True)
