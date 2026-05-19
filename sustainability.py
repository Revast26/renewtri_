import streamlit as st


def show_sustainability():
    st.header("🌱 Sustentabilidade")

    st.subheader("Educação ambiental")

    st.write(
        """
        O Renewtri incentiva práticas sustentáveis dentro das escolas públicas,
        promovendo conscientização ambiental e redução do desperdício alimentar.
        """
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.success("♻️ Compostagem: restos orgânicos podem virar adubo para hortas escolares.")
        st.info("🍎 Reaproveitamento: reduzir sobras ajuda a economizar recursos.")
        st.warning("🗑️ Separação de resíduos: separar lixo orgânico e reciclável melhora a coleta seletiva.")

    with col2:
        st.success("🌳 Consciência ambiental: pequenas ações geram grandes impactos.")
        st.info("📚 Educação sustentável: alunos aprendem sobre consumo consciente.")
        st.warning("💧 Uso inteligente: reduzir desperdício também economiza água e energia.")
        