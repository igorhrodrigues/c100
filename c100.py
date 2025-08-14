import streamlit as st
import tempfile

st.set_page_config(page_title="Limpar Arquivo TXT Grande", layout="centered")
st.title("🧹 Limpar Linhas do TXT (Arquivo Grande)")
st.write("Remove linhas que começam com `|C100|1|0||55|02|001|` sem travar a memória 😎")

uploaded_file = st.file_uploader("Faça upload do seu arquivo .txt", type=["txt"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8") as output_file:
        count_total = 0
        count_removidas = 0

        for linha in uploaded_file:
            linha_decodificada = linha.decode("utf-8")
            count_total += 1

            if not linha_decodificada.startswith("|C100|1|0||55|02|001|"):
                output_file.write(linha_decodificada)
            else:
                count_removidas += 1

        output_file_path = output_file.name

    st.success(f"Processado com sucesso! 🔍\n\nTotal de linhas: {count_total}\nLinhas removidas: {count_removidas}")

    # Para baixar
    with open(output_file_path, "rb") as f:
        st.download_button(
            label="📥 Baixar arquivo limpo",
            data=f,
            file_name="arquivo_limpo.txt",
            mime="text/plain"
        )
