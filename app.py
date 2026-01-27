import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da Página
st.set_page_config(page_title="Gestão de Combustível PRO", layout="wide")

# Estilização Personalizada (Fundo e Cards)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { color: #00ffcc; font-size: 30px; }
    .stPlotlyChart { border-radius: 15px; box-shadow: 0px 4px 20px rgba(0, 255, 204, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# Link da sua Planilha
ID_PLANILHA = "1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc"
URL = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()

    st.title("🚢 Sistema de Controle de Combustível Fiscal")
    st.write(f"Dados atualizados em: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}")
    st.markdown("---")

    # --- INDICADORES TOPO ---
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Litros Totais", f"{df['QTOS LTS'].sum():,.0f} L")
    c2.metric("Abastecimentos", f"{len(df)}")
    c3.metric("Média/Abastecimento", f"{df['QTOS LTS'].mean():,.0f} L")
    c4.metric("Cidades Atendidas", f"{df['LOCAL'].nunique()}")

    st.markdown("### 📊 Análise por Empurrador")
    
    # Criando DataFrame de Resumo por Empurrador
    resumo_emp = df.groupby('EMPURRADOR').agg(
        Litros_Totais=('QTOS LTS', 'sum'),
        Qtd_Abastecimentos=('QTOS LTS', 'count')
    ).reset_index()

    col_left, col_right = st.columns(2)

    with col_left:
        # Gráfico de Barras Duplo: Litros e Qtd de Vezes
        fig_emp = go.Figure()
        fig_emp.add_trace(go.Bar(x=resumo_emp['EMPURRADOR'], y=resumo_emp['Litros_Totais'], 
                                 name='Litros Totais', marker_color='#00ffcc'))
        fig_emp.add_trace(go.Scatter(x=resumo_emp['EMPURRADOR'], y=resumo_emp['Qtd_Abastecimentos'], 
                                     name='Qtd Abastecimentos', yaxis='y2', mode='lines+markers', line=dict(color='#ffaa00', width=3)))
        
        fig_emp.update_layout(
            title="Volume (L) vs Frequência por Empurrador",
            yaxis=dict(title="Volume em Litros"),
            yaxis2=dict(title="Qtd de Vezes", overlaying='y', side='right'),
            template="plotly_dark",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_emp, use_container_width=True)

    with col_right:
        # Mapa de Calor por Localidade
        st.subheader("📍 Localização de Abastecimento")
        df_local = df.groupby(['LOCAL', 'ESTADO']).agg({'QTOS LTS': 'sum', 'EMPURRADOR': 'count'}).reset_index()
        df_local.columns = ['LOCAL', 'ESTADO', 'LITROS', 'VEZES']
        
        fig_map = px.scatter(df_local, x="LOCAL", y="LITROS", size="VEZES", color="ESTADO",
                             hover_name="LOCAL", size_max=60, title="Volume e Frequência por Local")
        fig_map.update_layout(template="plotly_dark")
        st.plotly_chart(fig_map, use_container_width=True)

    # --- TABELA FINAL ---
    with st.expander("📄 Visualizar Relatório Detalhado"):
        st.dataframe(df.style.highlight_max(axis=0, color='#004433'), use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
