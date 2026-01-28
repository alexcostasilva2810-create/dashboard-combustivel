iimport streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import pytz

# Configuração e Limpeza
st.set_page_config(page_title="ZION MONITORAMENTO", layout="wide")
st.cache_data.clear()

# --- ESTILO: AZUL ESCURO PREMIUM + NÚMEROS 50px ---
st.markdown("""
    <style>
    .stApp { background-color: #000b1a; color: white; }
    .zion-header {
        background: linear-gradient(90deg, #001f3f, #00d4ff);
        color: white; padding: 20px; border-radius: 15px;
        font-size: 40px; font-weight: bold; text-align: center;
        margin-bottom: 30px; border-bottom: 4px solid #00d4ff;
    }
    /* Estilo dos Cards KPIs */
    div[data-testid="stMetric"] {
        background-color: #001529; border: 2px solid #003366;
        border-radius: 20px; padding: 25px; text-align: center;
    }
    /* NÚMEROS TAMANHO 50px COLORIDOS */
    div[data-testid="stMetricValue"] { font-size: 50px !important; font-weight: bold !important; }
    
    /* Cores por Categoria */
    [data-testid="stMetric"]:nth-child(1) div[data-testid="stMetricValue"] { color: #00ffcc !important; } /* Volume */
    [data-testid="stMetric"]:nth-child(2) div[data-testid="stMetricValue"] { color: #ffcc00 !important; } /* Qtd */
    [data-testid="stMetric"]:nth-child(3) div[data-testid="stMetricValue"] { color: #0099ff !important; } /* Forn */
    [data-testid="stMetric"]:nth-child(4) div[data-testid="stMetricValue"] { color: #ff3333 !important; } /* Cidades */
    
    label[data-testid="stMetricLabel"] { color: #cccccc !important; font-size: 18px !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="zion-header">ZION MONITORAMENTO</div>', unsafe_allow_html=True)

# Coordenadas fixas para o mapa não falhar mais
coords_br = {
    'PA': [-1.45, -48.50], 'AM': [-3.11, -60.02], 'RR': [2.82, -60.67],
    'AP': [0.03, -51.06], 'MA': [-2.53, -44.30], 'MT': [-12.64, -55.42],
    'RO': [-8.76, -63.90], 'TO': [-10.18, -48.33], 'AC': [-9.97, -67.81]
}

URL = "https://docs.google.com/spreadsheets/d/1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)
    
    # Injetando coordenadas no mapa para garantir nitidez
    df['lat'] = df['ESTADO'].map(lambda x: coords_br.get(str(x).upper(), [None, None])[0])
    df['lon'] = df['ESTADO'].map(lambda x: coords_br.get(str(x).upper(), [None, None])[1])

    # --- FILTRO DROPDAWN ---
    st.sidebar.header("⚙️ FILTROS")
    lista_forn = ["TODOS"] + sorted(df['FORNECEDOR'].unique().tolist())
    forn_sel = st.sidebar.selectbox("Escolha o Fornecedor:", lista_forn)

    if forn_sel != "TODOS":
        df = df[df['FORNECEDOR'] == forn_sel]

    # --- LINHA 1: KPIs GIGANTES ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Volume Total (L)", f"{int(df['QTOS LTS'].sum())}")
    c2.metric("Abastecimentos", len(df))
    top_f = df['FORNECEDOR'].value_counts().idxmax() if not df.empty else "---"
    c3.metric("Maior Fornecedor", top_f)
    c4.metric("Cidades Atendidas", df['LOCAL'].nunique())

    st.markdown("---")

    # --- LINHA 2: MAPA E RANKING ---
    col_mapa, col_rank = st.columns([2.5, 1.5])

    with col_mapa:
        st.subheader("📍 Mapa de Operações (Norte/Nordeste)")
        fig_map = px.scatter_mapbox(df.dropna(subset=['lat']), 
                                    lat="lat", lon="lon", 
                                    size="QTOS LTS", color="EMPURRADOR",
                                    hover_name="LOCAL", zoom=4, height=500,
                                    color_discrete_sequence=px.colors.qualitative.G10)
        fig_map.update_layout(mapbox_style="carto-darkmatter", margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig_map, use_container_width=True)

    with col_rank:
        st.subheader("🏢 Fornecedores por Volume")
        df_f = df.groupby('FORNECEDOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS')
        fig_f = px.bar(df_f, x='QTOS LTS', y='FORNECEDOR', orientation='h', 
                       text_auto=True, color_discrete_sequence=['#00d4ff'])
        fig_f.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', height=450)
        st.plotly_chart(fig_f, use_container_width=True)

    # --- LINHA 3: PERFORMANCE EMPURRADOR ---
    st.markdown("---")
    st.subheader("🚢 Volume Abastecido por Empurrador")
    df_emp = df.groupby('EMPURRADOR')['QTOS LTS'].sum().reset_index().sort_values('QTOS LTS', ascending=False)
    fig_emp = px.bar(df_emp, x='EMPURRADOR', y='QTOS LTS', text_auto=True, 
                     color='QTOS LTS', color_continuous_scale='Blues')
    fig_emp.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_emp, use_container_width=True)

except Exception as e:
    st.error(f"Erro na Planilha: {e}")

# Refresh 30s
st.markdown("""<script>setTimeout(function(){ window.location.reload(); }, 30000);</script>""", unsafe_allow_html=True)
