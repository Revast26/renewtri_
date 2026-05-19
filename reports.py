import streamlit as st
import pandas as pd
import plotly.express as px
import database


def show_reports():

    st.header("📑 Relatórios")

    dados = database.buscar_dados("""
        SELECT
            data,
            refeicoes_produzidas,
            desperdicio_kg
        FROM producao_alimentar
        ORDER BY data
    """)

    if not dados:

        st.warning("Nenhum dado encontrado.")
        return

    df = pd.DataFrame(
        dados,
        columns=[
            "Data",
            "Refeições",
            "Desperdício KG"
        ]
    )

    st.subheader("📋 Dados Registrados")

    st.dataframe(df, use_container_width=True)

    st.markdown("---")

    total_refeicoes = df["Refeições"].sum()

    total_desperdicio = df["Desperdício KG"].sum()

    taxa = 0

    if total_refeicoes > 0:

        taxa = (
            total_desperdicio / total_refeicoes
        ) * 100

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🍽 Total de refeições",
        int(total_refeicoes)
    )

    col2.metric(
        "🗑 Total desperdício",
        f"{total_desperdicio:.1f} kg"
    )

    col3.metric(
        "📉 Taxa de desperdício",
        f"{taxa:.2f}%"
    )

    st.markdown("---")

    st.subheader("📉 Desperdício por período")

    fig = px.bar(
        df,
        x="Data",
        y="Desperdício KG",
        color="Desperdício KG",
        title="Desperdício registrado"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("📈 Produção alimentar")

    fig2 = px.line(
        df,
        x="Data",
        y="Refeições",
        markers=True,
        title="Produção de refeições"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    st.markdown("---")

    st.subheader("🌱 Impacto Sustentável")

    economia = max(
        0,
        100 - total_desperdicio
    )

    st.success(
        f"O Renewtri ajudou a evitar aproximadamente {economia:.1f} kg de desperdício."
    )