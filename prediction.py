import streamlit as st
import pandas as pd
import database


def show_prediction():

    st.header("🤖 Previsão Inteligente")

    dados = database.buscar_dados("""
        SELECT
            refeicoes_produzidas,
            desperdicio_kg
        FROM producao_alimentar
    """)

    if not dados:

        st.warning(
            "Cadastre produções alimentares para gerar previsões."
        )

        return

    df = pd.DataFrame(
        dados,
        columns=[
            "Refeições",
            "Desperdício"
        ]
    )

    media_refeicoes = df["Refeições"].mean()

    media_desperdicio = df["Desperdício"].mean()

    recomendacao = int(media_refeicoes * 0.95)

    economia = max(
        0,
        100 - df["Desperdício"].sum()
    )

    st.subheader("📊 Indicadores Inteligentes")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "🍽 Média de refeições",
        f"{media_refeicoes:.0f}"
    )

    col2.metric(
        "🗑 Taxa média de desperdício",
        f"{media_desperdicio:.1f} kg"
    )

    col3.metric(
        "🌱 Kg economizados",
        f"{economia:.1f} kg"
    )

    st.markdown("---")

    st.subheader("🧠 Recomendações do Sistema")

    st.success(
        f"Recomendação: preparar aproximadamente {recomendacao} refeições amanhã."
    )

    if media_desperdicio > 10:

        st.warning(
            "Atenção: a taxa de desperdício está elevada."
        )

    else:

        st.info(
            "A taxa de desperdício está sob controle."
        )

    st.markdown("---")

    st.subheader("🌱 Impacto Sustentável")

    st.write(
        """
        O Renewtri analisa os dados registrados para ajudar escolas a:
        
        ✅ reduzir desperdícios
        
        ✅ otimizar produção
        
        ✅ melhorar planejamento alimentar
        
        ✅ fortalecer práticas sustentáveis
        """
    )