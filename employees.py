import streamlit as st
import database


def show_employees():

    st.header("👩‍🍳 Gerenciamento de Merendeiras")

    st.subheader("Cadastrar Merendeira")

    nome = st.text_input("Nome")

    email = st.text_input("Email")

    senha = st.text_input(
        "Senha",
        type="password"
    )

    if st.button("Cadastrar Merendeira"):

        try:

            database.executar_query(
                """
                INSERT INTO merendeiras
                (
                    escola_id,
                    nome,
                    email,
                    senha,
                    ativo
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    1,
                    nome,
                    email,
                    senha,
                    1
                )
            )

            st.success("Merendeira cadastrada com sucesso!")

        except Exception as erro:

            st.error(f"Erro ao cadastrar: {erro}")

    st.markdown("---")

    st.subheader("📋 Merendeiras Cadastradas")

    dados = database.buscar_dados("""
        SELECT
            id,
            nome,
            email,
            ativo
        FROM merendeiras
        ORDER BY nome
    """)

    if dados:

        for item in dados:

            id_usuario = item[0]
            nome = item[1]
            email = item[2]
            ativo = item[3]

            col1, col2 = st.columns([4, 1])

            with col1:

                status = "🟢 Ativa" if ativo else "🔴 Inativa"

                st.write(f"👤 {nome}")
                st.write(f"📧 {email}")
                st.write(status)

            with col2:

                if ativo:

                    if st.button(
                        "Desativar",
                        key=f"desativar_{id_usuario}"
                    ):

                        database.executar_query(
                            """
                            UPDATE merendeiras
                            SET ativo = 0
                            WHERE id = ?
                            """,
                            (id_usuario,)
                        )

                        st.rerun()

                else:

                    if st.button(
                        "Ativar",
                        key=f"ativar_{id_usuario}"
                    ):

                        database.executar_query(
                            """
                            UPDATE merendeiras
                            SET ativo = 1
                            WHERE id = ?
                            """,
                            (id_usuario,)
                        )

                        st.rerun()

            st.markdown("---")

    else:

        st.info("Nenhuma merendeira cadastrada.")