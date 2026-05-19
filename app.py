import streamlit as st

import auth
import database
from dashboard import show_dashboard
from food_production import show_food_production
from food_inventory import show_food_inventory
from employees import show_employees
from reports import show_reports
from prediction import show_prediction

def menu_lateral():
    """
    Cria o menu lateral do sistema.
    """

    st.sidebar.title("🌱 Renewtri")

    st.sidebar.markdown("---")

    st.sidebar.write(
        f"Usuário: {st.session_state.tipo_usuario}"
    )

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
    """
    Função principal do app.
    """

    st.set_page_config(
        page_title="Renewtri",
        page_icon="🌱",
        layout="wide"
    )

    database.init_db()

    auth.init_session()

    st.title("🌱 Renewtri")
    st.caption(
        "Plataforma inteligente para gestão da merenda escolar, redução do desperdício alimentar e promoção da sustentabilidade em escolas públicas."
    )

    st.markdown("---")

    # Usuário NÃO logado
    if not st.session_state.logado:

        auth.tela_autenticacao()

    # Usuário logado
    else:

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
            st.header("🌱 Sustentabilidade")
            st.info("Educação ambiental em construção.")


if __name__ == "__main__":
    main()