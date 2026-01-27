try:
    df = pd.read_csv(URL)
    
    # Isso remove espaços extras e deixa tudo igual para o Python não se perder
    df.columns = df.columns.str.strip() 

    # --- KPIs ---
    col1, col2 = st.columns(2)
    col1.metric("Total de Pedidos", len(df))
    # Usamos o nome exato da sua coluna: 'QTOS LTS'
    col2.metric("Total de Litros", f"{df['QTOS LTS'].sum():,.0f}")

    st.markdown("---")

    # --- GRÁFICOS ---
    graf_col1, graf_col2 = st.columns(2)

    with graf_col1:
        st.subheader("Volume por Empurrador")
        # Criando o gráfico com a coluna 'EMPURRADOR'
        fig_barras = px.bar(df, x="EMPURRADOR", y="QTOS LTS", color="EMPURRADOR")
        st.plotly_chart(fig_barras, use_container_width=True)

    with graf_col2:
        st.subheader("Consumo por Estado")
        # Criando o gráfico com a coluna 'ESTADO'
        fig_pizza = px.pie(df, values="QTOS LTS", names="ESTADO", hole=0.4)
        st.plotly_chart(fig_pizza, use_container_width=True)

except Exception as e:
    st.error(f"Ainda há um erro nos nomes das colunas: {e}")
