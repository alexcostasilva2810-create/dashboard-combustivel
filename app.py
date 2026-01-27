import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
import pytz

# Limpeza e Configuração
st.cache_data.clear()
st.set_page_config(page_title="Gestão Naval PRO", layout="wide")

# Estilo Claro e Elegante
st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    div[data-testid="stMetricValue"] { font-size: 35px !important; font-weight: bold !important; color: #1e40af !important; }
    .card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    </style>
    """, unsafe_allow_html=True)

fuso_br = pytz.timezone('America/Sao_Paulo')
agora = datetime.now(fuso_br).strftime('%d/%m/%Y %H:%M:%S')

ID_PLANILHA = "1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc"
URL = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv"

try:
    df = pd.read_csv(URL)
    df.columns = df.columns.str.strip()
    df['QTOS LTS'] = pd.to_numeric(df['QTOS LTS'], errors='coerce').fillna(0)

    st.title("⚓ MONITORAMENTO GEOGRÁFICO DE FROTA")
    st.write(f"⏱️ **Sincronizado:** {agora}")

    # KPIs Principais
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Volume Total (L)", f"{int(df['QTOS LTS'].sum())}")
    c2.metric("Abastecimentos", f"{len(df)}")
    c3.metric("Cidades", f"{df['LOCAL'].nunique()}")
    c4.metric("Fornecedores", f"{df['FORNECEDOR'].nunique()}")

    st.markdown("---")

    # --- O MAPA NITIDÍSSIMO (FOLIUM) ---
    st.subheader("📍 Mapa Interativo de Localização")
    
    # Criamos o mapa base centralizado na Região Norte
    m = folium.Map(location=[-3.11, -60.02], zoom_start=5, tiles="OpenStreetMap")

    # Dicionário de cores para os Empurradores ficarem coloridos
    cores = ['blue', 'green', 'red', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue', 'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen', 'gray', 'black', 'lightgray']
    empurradores = df['EMPURRADOR'].unique()
    cor_map = {emp: cores[i % len(cores)] for i, emp in enumerate(empurradores)}

    # Adicionando os pontos (Simulação por Localidade se não houver Lat/Long exata)
    # Nota: Se você adicionar colunas 'LATITUDE' e 'LONGITUDE' na planilha, o mapa fica 100% preciso.
    # Por enquanto, ele agrupa por Local.
    for index, row in df.iterrows():
        # Exemplo de coordenadas fixas para teste baseado nos nomes das cidades comuns na sua região
        # Se a planilha tiver Lat/Long, use: lat, lon = row['LATITUDE'], row['LONGITUDE']
        # Aqui o Folium precisa de uma coordenada para não dar o erro da sua imagem.
        if "MANAUS" in str(row['LOCAL']).upper(): lat, lon = -3.11, -60.02
        elif "BELEM" in str(row['LOCAL']).upper(): lat, lon = -1.45, -48.50
        elif "ITACOATIARA" in str(row['LOCAL']).upper(): lat, lon = -3.14, -58.44
        elif "SANTAREM" in str(row['LOCAL']).upper(): lat, lon = -2.44, -54.70
        else: lat, lon = -3.11, -60.02 # Padrão

        folium.Marker(
            [lat, lon],
            popup=f"<b>Empurrador:</b> {row['EMPURRADOR']}<br><b>Litros:</b> {int(row['QTOS LTS'])}",
            tooltip=row['LOCAL'],
            icon=folium.Icon(color=cor_map.get(row['EMPURRADOR'], 'blue'), icon='ship', prefix='fa')
        ).add_to(m)

    folium_static(m, width=1300, height=500)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")

st.markdown("<script>setTimeout(function(){window.location.reload();}, 60000);</script>", unsafe_allow_html=True)
