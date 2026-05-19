import streamlit as st
import database
import utils


def init_session():
    if "logado" not in st.session_state:
        st.session_state.logado = False

    if "usuario" not in st.session_state:
        st.session_state.usuario = None

    if "tipo_usuario" not in st.session_state:
        st.session_state.tipo_usuario = None


def logout():
    st.session_state.logado = False
    st.session_state.usuario = None
    st.session_state.tipo_usuario = None
    st.rerun()


def cadastrar_escola():
    st.subheader("Cadastro da Instituição")

    nome = st.text_input("Nome da instituição", key="cadastro_nome")
    email = st.text_input("Email", key="cadastro_email")
    cnpj = st.text_input("CNPJ", key="cadastro_cnpj")
    inep = st.text_input("Código INEP", key="cadastro_inep")
    senha = st.text_input("Senha", type="password", key="cadastro_senha")

    if st.button("Cadastrar instituição"):

        if not nome or not email or not cnpj or not inep or not senha:
            st.warning("Preencha todos os campos.")
            return

        if not utils.validar_cnpj(cnpj):
            st.error("CNPJ inválido.")
            return

        codigo_escola = utils.gerar_codigo_escola()

        try:
            database.executar_query(
                """
                INSERT INTO escolas
                (nome, email, cnpj, inep, senha, codigo_escola)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (nome, email, cnpj, inep, senha, codigo_escola)
            )

            st.success("Instituição cadastrada com sucesso!")
            st.info(f"Código da escola: {codigo_escola}")

        except Exception as erro:
            st.error(f"Erro ao cadastrar: {erro}")


def login_escola():
    st.subheader("Login da Instituição")

    email = st.text_input("Email", key="login_instituicao_email")
    cnpj = st.text_input("CNPJ", key="login_instituicao_cnpj")
    senha = st.text_input("Senha", type="password", key="login_instituicao_senha")

    if st.button("Entrar como instituição"):

        usuario = database.buscar_dados(
            """
            SELECT * FROM escolas
            WHERE email = ? AND cnpj = ? AND senha = ?
            """,
            (email, cnpj, senha)
        )

        if usuario:
            st.session_state.logado = True
            st.session_state.usuario = usuario[0]
            st.session_state.tipo_usuario = "instituicao"
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Email, CNPJ ou senha incorretos.")


def login_merendeira():
    st.subheader("Login da Merendeira")

    email = st.text_input("Email da merendeira", key="login_merendeira_email")
    codigo_escola = st.text_input("Código da escola", key="login_merendeira_codigo")
    senha = st.text_input("Senha", type="password", key="login_merendeira_senha")

    if st.button("Entrar como merendeira"):

        usuario = database.buscar_dados(
            """
            SELECT m.*
            FROM merendeiras m
            JOIN escolas e ON m.escola_id = e.id
            WHERE m.email = ?
            AND m.senha = ?
            AND e.codigo_escola = ?
            AND m.ativo = 1
            """,
            (email, senha, codigo_escola)
        )

        if usuario:
            st.session_state.logado = True
            st.session_state.usuario = usuario[0]
            st.session_state.tipo_usuario = "merendeira"
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Dados inválidos.")


def tela_autenticacao():
    st.markdown(
        """
        <div style="text-align:center; margin-bottom: 25px;">
            <h1 style="font-family: Lora, serif; font-size: 56px; margin-bottom: 0;">
                Renewtri
            </h1>
            <p style="font-size: 20px; color: #4b5563;">
                Menos desperdício, mais futuro
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    aba1, aba2, aba3 = st.tabs([
        "Login Instituição",
        "Login Merendeira",
        "Cadastro Instituição"
    ])

    with aba1:
        login_escola()

    with aba2:
        login_merendeira()

    with aba3:
        cadastrar_escola()