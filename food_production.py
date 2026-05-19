import streamlit as st
import database


def show_food_production():

    st.header("🍽 Produção Alimentar")

    st.subheader("Registrar Produção")

    data = st.date_input("Data")

    turno = st.selectbox(
        "Turno",
        ["Manhã", "Tarde", "Noite"]
    )

    refeicoes = st.number_input(
        "Quantidade de refeições",
        min_value=0,
        step=1
    )

    alimentos = st.text_area(
        "Alimentos utilizados"
    )

    desperdicio = st.number_input(
        "Desperdício (kg)",
        min_value=0.0,
        step=0.1
    )

    observacoes = st.text_area(
        "Observações"
    )

    if st.button("Salvar Produção"):

        database.executar_query(
            """
            INSERT INTO producao_alimentar
            (
                escola_id,
                data,
                turno,
                refeicoes_produzidas,
                alimentos_utilizados,
                desperdicio_kg,
                observacoes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                1,
                str(data),
                turno,
                refeicoes,
                alimentos,
                desperdicio,
                observacoes
            )
        )

        st.success("Produção registrada com sucesso!")

    st.markdown("---")

    st.subheader("📋 Histórico de Produção")

    dados = database.buscar_dados("""
        SELECT
            data,
            turno,
            refeicoes_produzidas,
            desperdicio_kg
        FROM producao_alimentar
        ORDER BY data DESC
    """)

    if dados:

        for item in dados:

            st.container()

            st.write(f"📅 Data: {item[0]}")
            st.write(f"⏰ Turno: {item[1]}")
            st.write(f"🍽 Refeições: {item[2]}")
            st.write(f"🗑 Desperdício: {item[3]} kg")

            st.markdown("---")

    else:
        st.info("Nenhuma produção cadastrada.")