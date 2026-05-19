import streamlit as st


def show_sustainability() -> None:
    st.title("🌱 Educação Ambiental")
    st.caption("Conscientização, sustentabilidade e redução do desperdício alimentar.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("♻️ Kg economizados", "42 kg")

    with col2:
        st.metric("🌎 Redução de desperdício", "-18%")

    with col3:
        st.metric("🍽️ Aproveitamento alimentar", "84%")

    st.markdown("---")

    st.subheader("💡 Dicas sustentáveis")

    dicas = [
        "Evite produzir mais refeições do que a média de consumo registrada.",
        "Separe resíduos orgânicos para possíveis processos de compostagem.",
        "Registre as sobras diariamente para melhorar o planejamento da merenda.",
        "Incentive os alunos a colocarem no prato apenas o que pretendem consumir.",
        "Utilize campanhas educativas para conscientizar sobre desperdício alimentar.",
    ]

    for dica in dicas:
        st.success(dica)

    st.markdown("---")

    st.subheader("📚 Curiosidades ambientais")

    curiosidades = [
        "O desperdício de alimentos também representa desperdício de água, energia e trabalho.",
        "A compostagem transforma resíduos orgânicos em adubo natural.",
        "Reduzir desperdícios ajuda a escola a economizar recursos e diminuir impactos ambientais.",
    ]

    for curiosidade in curiosidades:
        st.info(curiosidade)

    st.markdown("---")

    st.subheader("🏫 Campanhas escolares")

    col1, col2 = st.columns(2)

    with col1:
        st.warning(
            """
            **🌱 Semana do Prato Limpo**

            Campanha para incentivar os alunos a evitarem desperdício durante a merenda.
            """
        )

    with col2:
        st.warning(
            """
            **♻️ Desafio Sustentável**

            Turmas podem participar de ações para reduzir resíduos e melhorar hábitos ambientais.
            """
        )

    st.markdown("---")

    st.subheader("🌿 Compostagem")

    st.markdown(
        """
        A compostagem é uma prática sustentável que transforma resíduos orgânicos em adubo natural.
        No contexto escolar, ela pode ser utilizada como ferramenta educativa, aproximando os alunos
        de temas como meio ambiente, consumo consciente e responsabilidade coletiva.
        """
    )