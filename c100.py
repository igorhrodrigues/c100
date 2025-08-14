import streamlit as st

st.set_page_config(page_title="Limpar Arquivo TXT", layout="centered")

st.title("🧹 Limpar Linhas do TXT")
st.write("Remove linhas que começam com `|C100|1|0||55|02|001|`")

uploaded_file = st.file_uploader("Faça upload do seu arquivo .txt", type=["txt"])

if uploaded_file is not None:
    linhas = uploaded_file.read().decode("utf-8").splitlines()

    # Filtrar as linhas
    linhas_filtradas = [
        linha for linha in linhas
        if not linha.startswith("|C100|1|0||55|02|001|")
    ]

    # Transformar de volta em texto
    resultado = "\n".join(linhas_filtradas)

    # Mostrar prévia
    st.subheader("✅ Linhas filtradas (prévia):")
    st.text("\n".join(linhas_filtradas[:10]))  # mostra só as 10 primeiras linhas

    # Botão para download
    st.download_button(
        label="📥 Baixar arquivo limpo",
        data=resultado,
        file_name="arquivo_limpo.txt",
        mime="text/plain"
    )
