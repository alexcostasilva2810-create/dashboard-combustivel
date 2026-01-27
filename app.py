import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Forçar atualização dos dados (Sem Cache)
st.cache_data.clear()

st.set_page_config(page_title="Dashboard Naval PRO", layout="wide")

# --- DESIGN ESTILO TABLET (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(180deg, #001f3f 0%, #000a1a 100%);
        color: white;
    }
    /* Estilização dos Cards de Métricas */
    .metric-card {
        background: rgba(0, 150, 255, 0.1);
        border: 1px solid rgba(0, 242, 255, 0.3);
        border-radius: 15px;
        padding: 20px;
        text-align: center;
    }
    .metric-value {
        font-size: 35px !important;
        font-weight: bold !important;
        color: #00f2ff !important;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
    }
    .metric-label {
        font-size: 16px;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# Link da sua Planilha
ID_PLANILHA = "1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc"
URL = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    # --- CABEÇALHO ---
    st.title("⚓ MONITORAMENTO DE FROTA E COMBUSTÍVEL")
    st.markdown(f"🕒 **Última Atualização:** {pd.Timestamp.now().strftime('%H:%M:%S')}")

    # --- LINHA 1: MÉTRICAS ESTILO INDICADOR (KPIs) ---
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f'<div class="metric-card"><p class="metric-label">Volume Total</p><p class="metric-value">{df["QTOS LTS"].sum():,.0f} L</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><p class="metric-label">Abastecimentos</p><p class="metric-value">{len(df)}</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><p class="metric-label">Cidades</p><p class="metric-value">{df["LOCAL"].nunique()}</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><p class="metric-label">Fornecedores</p><p class="metric-value">{df["FORNECEDOR"].nunique()}</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- LINHA 2: GRÁFICOS PROFISSIONAIS ---
    c_left, c_right = st.columns([6, 4])

    with c_left:
        st.subheader("📊 Litros e Frequência por Empurrador")
        # Agrupando dados
        resumo = df.groupby('EMPURRADOR').agg({'QTOS LTS': 'sum', 'ID': 'count'}).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(x=resumo['EMPURRADOR'], y=resumo['QTOS LTS'], name='Litros', marker_color='#0077ff'))
        fig.add_trace(go.Scatter(x=resumo['EMPURRADOR'], y=resumo['ID'], name='Qtd Abastecimento', yaxis='y2', line=dict(color='#00f2ff', width=4)))
        
        fig.update_layout(
            yaxis=dict(title="Volume (L)", gridcolor='rgba(255,255,255,0.1)'),
            yaxis2=dict(title="Frequência", overlaying='y', side='right'),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="white"), template="plotly_dark", height=450
        )
        st.plotly_chart(fig, use_container_width=True)

    with c_right:
        st.subheader("📍 Top Localidades")
        # Gráfico circular de locais
        df_loc = df.groupby('LOCAL').size().reset_index(name='Vezes').sort_values('Vezes', ascending=False).head(5)
        fig_pizza = px.pie(df_loc, values='Vezes', names='LOCAL', hole=0.6, 
                           color_discrete_sequence=px.colors.sequential.Cyan_r)
        fig_pizza.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), showlegend=False)
        fig_pizza.update_traces(textinfo='label+percent')
        st.plotly_chart(fig_pizza, use_container_width=True)

except Exception as e:
    st.warning("Conectando ao banco de dados...")

# Atualização automática (JavaScript oculto para refresh a cada 60s)
st.markdown("<script>setTimeout(function(){window.location.reload();}, 60000);</script>", unsafe_allow_html=True)
