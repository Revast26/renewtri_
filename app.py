import streamlit as st

import auth
import database
from dashboard import show_dashboard
from food_production import show_food_production
from food_inventory import show_food_inventory
from employees import show_employees
from reports import show_reports
from prediction import show_prediction
from sustainability import show_sustainability


def menu_lateral():
    st.sidebar.markdown(
        """
        <div style="padding: 8px 0 18px 0;">
            <h1 style="font-size: 28px; margin-bottom: 4px; color: #ffffff;">
                Renewtri
            </h1>
            <p style="font-size: 14px; color: #d1d5db; margin-top: 0;">
                Gestão inteligente da merenda escolar
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.markdown("---")

    st.sidebar.markdown(
        f"""
        **Escola:** CETI Prefeito João Mendes Olímpio de Melo  
        **Perfil:** {st.session_state.tipo_usuario.capitalize()}
        """
    )

    st.sidebar.markdown("---")

    pagina = st.sidebar.radio(
        "Navegação",
        [
            "Dashboard",
            "Produção Alimentar",
            "Alimentos Recebidos",
            "Merendeiras",
            "Relatórios",
            "Previsão Inteligente",
            "Sustentabilidade"
        ]
    )

    st.sidebar.markdown("---")

    if st.sidebar.button("Sair"):
        auth.logout()

    return pagina


def main():
    st.set_page_config(
        page_title="Renewtri",
        page_icon="R",
        layout="wide"
    )

    database.init_db()
    database.criar_dados_demo()
    auth.init_session()

    st.title("Renewtri")
    st.caption("Menos desperdício, mais futuro")

    st.markdown("---")

    if not st.session_state.logado:
        auth.tela_autenticacao()
        return

    pagina = menu_lateral()

    if pagina == "Dashboard":
        show_dashboard()

    elif pagina == "Produção Alimentar":
        show_food_production()

    elif pagina == "Alimentos Recebidos":
        show_food_inventory()

    elif pagina == "Merendeiras":
        show_employees()

    elif pagina == "Relatórios":
        show_reports()

    elif pagina == "Previsão Inteligente":
        show_prediction()

    elif pagina == "Sustentabilidade":
        show_sustainability()


if __name__ == "__main__":
    main()