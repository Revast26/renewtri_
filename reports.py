from datetime import date, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

import database as db
from utils import format_int, format_kg, format_percent, metric_card, page_header, plotly_layout


def show_reports(school_id: int) -> None:
    page_header(
        "Relatórios",
        "Filtre períodos, compare resultados e gere uma visão clara para prestação de contas e apresentação.",
        "Análise de dados",
    )

    col_start, col_end = st.columns(2)
    with col_start:
        start = st.date_input("Data inicial", value=date.today() - timedelta(days=30))
    with col_end:
        end = st.date_input("Data final", value=date.today())

    if start > end:
        st.error("A data inicial não pode ser posterior à data final.")
        return

    production = db.production_df(school_id, start.isoformat(), end.isoformat())
    inventory = db.inventory_df(school_id, start.isoformat(), end.isoformat())

    meals = production["refeicoes_produzidas"].sum() if not production.empty else 0
    waste = production["desperdicio_kg"].sum() if not production.empty else 0.0
    received = inventory["quantidade_kg"].sum() if not inventory.empty else 0.0
    rate = waste / meals * 100 if meals else 0.0
    baseline_rate = 12.0
    saved = max((baseline_rate - rate) / 100 * meals, 0.0) if meals else 0.0

    cols = st.columns(5)
    with cols[0]:
        metric_card("Refeições", format_int(meals), "Período filtrado")
    with cols[1]:
        metric_card("Desperdício", format_kg(waste), "Período filtrado")
    with cols[2]:
        metric_card("Taxa", format_percent(rate), "Desperdício/refeições")
    with cols[3]:
        metric_card("Recebidos", format_kg(received), "Alimentos no período")
    with cols[4]:
        metric_card("Economizados", format_kg(saved), "Contra meta de 12%")

    if production.empty:
        st.info("Nenhum registro encontrado para o período selecionado.")
        return

    production["data"] = pd.to_datetime(production["data"])
    by_day = production.groupby("data", as_index=False).agg(
        refeicoes=("refeicoes_produzidas", "sum"),
        desperdicio=("desperdicio_kg", "sum"),
    )
    by_day["taxa"] = by_day["desperdicio"] / by_day["refeicoes"] * 100

    left, right = st.columns(2)
    with left:
        fig = px.area(
            by_day,
            x="data",
            y="desperdicio",
            color_discrete_sequence=["#0f9f6e"],
            labels={"data": "Data", "desperdicio": "Desperdício (kg)"},
        )
        st.plotly_chart(plotly_layout(fig, "Desperdício no período"), use_container_width=True)
    with right:
        fig = px.line(
            by_day,
            x="data",
            y="refeicoes",
            markers=True,
            color_discrete_sequence=["#0b6fb8"],
            labels={"data": "Data", "refeicoes": "Refeições"},
        )
        st.plotly_chart(plotly_layout(fig, "Refeições produzidas"), use_container_width=True)

    if not inventory.empty:
        inv = inventory.groupby("alimento", as_index=False)["quantidade_kg"].sum().sort_values(
            "quantidade_kg", ascending=False
        )
        fig = px.bar(
            inv,
            x="alimento",
            y="quantidade_kg",
            color="quantidade_kg",
            color_continuous_scale=["#dff6ef", "#0f9f6e"],
            labels={"alimento": "Alimento", "quantidade_kg": "Kg recebidos"},
        )
        st.plotly_chart(plotly_layout(fig, "Alimentos recebidos por tipo"), use_container_width=True)

    st.subheader("Tabela de produção")
    st.dataframe(production, use_container_width=True, hide_index=True)

    st.subheader("Tabela de alimentos recebidos")
    st.dataframe(inventory, use_container_width=True, hide_index=True)

    if st.button("Registrar resumo deste relatório"):
        summary = (
            f"{format_int(meals)} refeições, {format_kg(waste)} de desperdício, "
            f"taxa {format_percent(rate)} e {format_kg(received)} recebidos."
        )
        db.save_report(school_id, "Relatório operacional", start.isoformat(), end.isoformat(), summary)
        st.success("Resumo salvo na tabela de relatórios.")
