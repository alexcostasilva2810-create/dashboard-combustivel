import streamlit as st
import pandas as pd

# O ID está na URL da sua planilha entre '/d/' e '/edit'
ID_PLANILHA = "1sNVY3-zRHn-Oa8sGJOF5GGcfUNSNWwOb9IfcNL3mYGc" 
URL = f"https://docs.google.com/spreadsheets/d/{ID_PLANILHA}/export?format=csv"

df = pd.read_csv(URL)
st.title("📊 Gestão de Combustível Online")
st.write(df) # Exibe a tabela de dados
