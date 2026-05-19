import streamlit as st
import pandas as pd
import plotly.express as px
import database


def show_dashboard():
    st.header("📊 Dashboard")

    dados_producao = database.buscar_dados("""
        SELECT data, refeicoes_produzidas, desperdicio_kg
        FROM producao_alimentar
        ORDER BY data
    """)

    dados_alimentos = database.buscar_dados("""
        SELECT quantidade_kg
        FROM alimentos_recebidos
    """)

    if dados_producao:
        df = pd.DataFrame(
            dados_producao,
            columns=["Data", "Refeições Produzidas", "Desperdício KG"]
        )
    else:
        df = pd.DataFrame({
            "Data": ["Seg", "Ter", "Qua", "Qui", "Sex"],
            "Refeições Produzidas": [180, 200, 190, 210, 185],
            "Desperdício KG": [12, 10, 8, 7, 6]
        })

    total_refeicoes = int(df["Refeições Produzidas"].sum())
    total_desperdicio = float(df["Desperdício KG"].sum())

    if total_refeicoes > 0:
        taxa_desperdicio = (total_desperdicio / total_refeicoes) * 100
    else:
        taxa_desperdicio = 0

    if dados_alimentos:
        total_alimentos = sum(item[0] for item in dados_alimentos)
    else:
        total_alimentos = 55

    quilos_economizados = max(0, 50 - total_desperdicio)

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("🍽 Refeições", total_refeicoes)
    col2.metric("🗑 Desperdício", f"{total_desperdicio:.1f} kg")
    col3.metric("📦 Alimentos recebidos", f"{total_alimentos:.1f} kg")
    col4.metric("📉 Taxa de desperdício", f"{taxa_desperdicio:.1f}%")
    col5.metric("🌱 Kg economizados", f"{quilos_economizados:.1f} kg")

    st.markdown("---")

    st.subheader("📉 Desperdício semanal")

    fig = px.bar(
        df,
        x="Data",
        y="Desperdício KG",
        text="Desperdício KG",
        title="Desperdício registrado por dia"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🍽 Refeições produzidas")

    fig2 = px.line(
        df,
        x="Data",
        y="Refeições Produzidas",
        markers=True,
        title="Evolução da produção alimentar"
    )

    st.plotly_chart(fig2, use_container_width=True)