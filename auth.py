import streamlit as st
import database
import utils


def init_session():
    """
    Cria variáveis de sessão do Streamlit.
    """

    if "logado" not in st.session_state:
        st.session_state.logado = False

    if "usuario" not in st.session_state:
        st.session_state.usuario = None

    if "tipo_usuario" not in st.session_state:
        st.session_state.tipo_usuario = None


def logout():
    """
    Faz logout do usuário.
    """

    st.session_state.logado = False
    st.session_state.usuario = None
    st.session_state.tipo_usuario = None

    st.rerun()


def cadastrar_escola():
    """
    Cadastro da instituição de ensino.
    """

    st.subheader("Cadastro da Instituição")

    nome = st.text_input("Nome da instituição")
    email = st.text_input("Email")
    cnpj = st.text_input("CNPJ")
    inep = st.text_input("Código INEP")
    senha = st.text_input("Senha", type="password")

    if st.button("Cadastrar instituição"):

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

            st.success(f"Instituição cadastrada com sucesso!")
            st.info(f"Código da escola: {codigo_escola}")

        except Exception as erro:
            st.error(f"Erro ao cadastrar: {erro}")


def login_escola():
    """
    Login da instituição.
    """

    st.subheader("Login da Instituição")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar como instituição"):

        usuario = database.buscar_dados(
            """
            SELECT * FROM escolas
            WHERE email = ? AND senha = ?
            """,
            (email, senha)
        )

        if usuario:

            st.session_state.logado = True
            st.session_state.usuario = usuario[0]
            st.session_state.tipo_usuario = "instituicao"

            st.success("Login realizado com sucesso!")
            st.rerun()

        else:
            st.error("Email ou senha incorretos.")


def login_merendeira():
    """
    Login da merendeira.
    """

    st.subheader("Login da Merendeira")

    email = st.text_input("Email da merendeira")
    codigo_escola = st.text_input("Código da escola")
    senha = st.text_input("Senha", type="password")

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
    """
    Tela principal de autenticação.
    """

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