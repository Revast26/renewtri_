import pandas as pd
import plotly.express as px
import streamlit as st

import database as db
from utils import format_int, format_kg, format_percent, metric_card, page_header, plotly_layout


def calculate_metrics(production: pd.DataFrame, inventory: pd.DataFrame) -> dict[str, float]:
    meals = float(production["refeicoes_produzidas"].sum()) if not production.empty else 0.0
    waste = float(production["desperdicio_kg"].sum()) if not production.empty else 0.0
    received = float(inventory["quantidade_kg"].sum()) if not inventory.empty else 0.0
    waste_rate = (waste / meals * 100) if meals else 0.0

    if not production.empty:
        production = production.copy()
        production["data"] = pd.to_datetime(production["data"])
        current_month = pd.Timestamp.today().to_period("M")
        previous_month = current_month - 1
        current_waste = production[production["data"].dt.to_period("M") == current_month]["desperdicio_kg"].sum()
        previous_waste = production[production["data"].dt.to_period("M") == previous_month]["desperdicio_kg"].sum()
        saved = max(float(previous_waste - current_waste), 0.0)
    else:
        saved = 0.0

    return {
        "meals": meals,
        "waste": waste,
        "received": received,
        "waste_rate": waste_rate,
        "saved": saved,
    }


def show_dashboard(school_id: int) -> None:
    page_header(
        "Dashboard principal",
        "Acompanhe produção, desperdício, estoque recebido e indicadores de sustentabilidade em tempo real.",
        "Gestão inteligente da merenda",
    )

    production = db.production_df(school_id)
    inventory = db.inventory_df(school_id)
    metrics = calculate_metrics(production, inventory)

    cols = st.columns(5)
    with cols[0]:
        metric_card("Refeições produzidas", format_int(metrics["meals"]), "Total registrado")
    with cols[1]:
        metric_card("Desperdício registrado", format_kg(metrics["waste"]), "Soma em kg")
    with cols[2]:
        metric_card("Alimentos recebidos", format_kg(metrics["received"]), "Entradas no estoque")
    with cols[3]:
        metric_card("Taxa de desperdício", format_percent(metrics["waste_rate"]), "Kg por refeição")
    with cols[4]:
        metric_card("Quilos economizados", format_kg(metrics["saved"]), "Comparação mensal")

    if production.empty:
        st.info("Ainda não há produção registrada. Use os cadastros para alimentar o dashboard.")
        return

    chart_df = production.copy()
    chart_df["data"] = pd.to_datetime(chart_df["data"])
    chart_df["semana"] = chart_df["data"].dt.to_period("W").astype(str)
    chart_df["mes"] = chart_df["data"].dt.to_period("M").astype(str)

    weekly = chart_df.groupby("semana", as_index=False)["desperdicio_kg"].sum()
    monthly = chart_df.groupby("mes", as_index=False).agg(
        refeicoes_produzidas=("refeicoes_produzidas", "sum"),
        desperdicio_kg=("desperdicio_kg", "sum"),
    )
    monthly["taxa_desperdicio"] = monthly["desperdicio_kg"] / monthly["refeicoes_produzidas"] * 100

    left, right = st.columns([1, 1])
    with left:
        fig = px.bar(
            weekly.tail(10),
            x="semana",
            y="desperdicio_kg",
            color_discrete_sequence=["#0f9f6e"],
            labels={"semana": "Semana", "desperdicio_kg": "Desperdício (kg)"},
        )
        st.plotly_chart(plotly_layout(fig, "Desperdício semanal"), use_container_width=True)

    with right:
        fig = px.line(
            monthly,
            x="mes",
            y="taxa_desperdicio",
            markers=True,
            color_discrete_sequence=["#0b6fb8"],
            labels={"mes": "Mês", "taxa_desperdicio": "Taxa (%)"},
        )
        st.plotly_chart(plotly_layout(fig, "Evolução mensal da taxa de desperdício"), use_container_width=True)

    period_df = chart_df.sort_values("data").tail(28).copy()
    period_df["periodo"] = period_df["data"].apply(
        lambda value: "Últimos 14 dias" if value >= period_df["data"].max() - pd.Timedelta(days=13) else "14 dias anteriores"
    )
    comparison = period_df.groupby("periodo", as_index=False).agg(
        refeicoes=("refeicoes_produzidas", "sum"),
        desperdicio=("desperdicio_kg", "sum"),
    )
    comparison_long = comparison.melt(id_vars="periodo", var_name="indicador", value_name="valor")
    fig = px.bar(
        comparison_long,
        x="periodo",
        y="valor",
        color="indicador",
        barmode="group",
        color_discrete_map={"refeicoes": "#0b6fb8", "desperdicio": "#0f9f6e"},
        labels={"periodo": "Período", "valor": "Total", "indicador": "Indicador"},
    )
    st.plotly_chart(plotly_layout(fig, "Comparação entre períodos recentes"), use_container_width=True)

    st.subheader("Últimos registros")
    st.dataframe(
        production.head(8),
        use_container_width=True,
        hide_index=True,
        column_config={
            "data": "Data",
            "turno": "Turno",
            "refeicoes_produzidas": "Refeições",
            "desperdicio_kg": "Desperdício (kg)",
            "alimentos_utilizados": "Alimentos utilizados",
            "registrado_por": "Registrado por",
        },
    )
