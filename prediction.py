from datetime import date, timedelta

import pandas as pd
import streamlit as st

import database as db
from utils import format_kg, format_percent, metric_card, page_header


def show_prediction(school_id: int) -> None:
    page_header(
        "Previsão Inteligente",
        "Simulação baseada em médias, histórico de consumo e tendência simples de desperdício.",
        "Análise preditiva simples",
    )

    production = db.production_df(school_id)
    if production.empty or len(production) < 3:
        st.info("Cadastre pelo menos três produções para gerar recomendações inteligentes.")
        return

    df = production.copy()
    df["data"] = pd.to_datetime(df["data"])
    df = df.sort_values("data")

    last_14 = df[df["data"] >= df["data"].max() - pd.Timedelta(days=14)]
    last_30 = df[df["data"] >= df["data"].max() - pd.Timedelta(days=30)]
    average_meals = last_14["refeicoes_produzidas"].mean()
    average_waste = last_14["desperdicio_kg"].mean()
    waste_rate = last_30["desperdicio_kg"].sum() / last_30["refeicoes_produzidas"].sum() * 100

    weekday = (date.today() + timedelta(days=1)).weekday()
    weekday_history = df[df["data"].dt.weekday == weekday]
    if not weekday_history.empty:
        recommended = int(round((average_meals * 0.55) + (weekday_history["refeicoes_produzidas"].tail(6).mean() * 0.45)))
    else:
        recommended = int(round(average_meals))

    current_month = pd.Timestamp.today().to_period("M")
    previous_month = current_month - 1
    current_waste = df[df["data"].dt.to_period("M") == current_month]["desperdicio_kg"].sum()
    previous_waste = df[df["data"].dt.to_period("M") == previous_month]["desperdicio_kg"].sum()
    saved = max(float(previous_waste - current_waste), 0.0)

    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Recomendação", f"{recommended} refeições", "Preparo sugerido para amanhã")
    with col2:
        metric_card("Taxa atual", format_percent(waste_rate), "Últimos 30 dias")
    with col3:
        metric_card("Economia mensal", format_kg(saved), "Comparação com mês anterior")

    st.success(f"Recomendação: preparar {recommended} refeições amanhã.")
    st.info(f"Taxa de desperdício atual: {format_percent(waste_rate)}.")
    st.success(f"{format_kg(saved)} foram economizados este mês.")

    st.subheader("Como a previsão foi calculada")
    st.markdown(
        f"""
        <div class="info-card">
            <p><strong>Média dos últimos 14 dias:</strong> {average_meals:.0f} refeições por registro.</p>
            <p><strong>Média de desperdício recente:</strong> {average_waste:.1f} kg por registro.</p>
            <p><strong>Comparação histórica:</strong> a recomendação combina média recente com registros do mesmo dia da semana.</p>
            <p><strong>Leitura operacional:</strong> se a taxa passar de 10%, a equipe deve reduzir preparo inicial e acompanhar aceitação do cardápio.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if waste_rate > 10:
        st.warning("A taxa está acima da meta sugerida de 10%. Revise cardápios com baixa aceitação e dias de menor frequência.")
    elif waste_rate > 6:
        st.info("A taxa está controlada, mas ainda há espaço para reduzir sobras com ajustes finos por turno.")
    else:
        st.success("A taxa está em nível muito bom para demonstração do MVP.")

    st.subheader("Histórico usado na análise")
    st.dataframe(
        df.tail(12).sort_values("data", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
