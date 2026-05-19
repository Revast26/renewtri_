import streamlit as st
import database


def show_food_inventory():

    st.header("📦 Alimentos Recebidos")

    st.subheader("Registrar Entrada de Alimentos")

    data = st.date_input("Data da entrega")

    fornecedor = st.text_input("Fornecedor")

    alimento = st.text_input("Nome do alimento")

    quantidade = st.number_input(
        "Quantidade (kg)",
        min_value=0.0,
        step=0.5
    )

    validade = st.date_input("Validade")

    observacoes = st.text_area("Observações")

    if st.button("Salvar Alimento"):

        database.executar_query(
            """
            INSERT INTO alimentos_recebidos
            (
                escola_id,
                data,
                fornecedor,
                alimento,
                quantidade_kg,
                validade,
                observacoes
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                1,
                str(data),
                fornecedor,
                alimento,
                quantidade,
                str(validade),
                observacoes
            )
        )

        st.success("Alimento registrado com sucesso!")

    st.markdown("---")

    st.subheader("📋 Histórico de Entradas")

    dados = database.buscar_dados("""
        SELECT
            data,
            fornecedor,
            alimento,
            quantidade_kg,
            validade
        FROM alimentos_recebidos
        ORDER BY data DESC
    """)

    if dados:

        for item in dados:

            st.container()

            st.write(f"📅 Data: {item[0]}")
            st.write(f"🏢 Fornecedor: {item[1]}")
            st.write(f"🍚 Alimento: {item[2]}")
            st.write(f"⚖ Quantidade: {item[3]} kg")
            st.write(f"⏳ Validade: {item[4]}")

            st.markdown("---")

    else:
        st.info("Nenhum alimento registrado.")