import streamlit as st
import requests
import tempfile

st.set_page_config(page_title="Limpar TXT por Link", layout="centered")
st.title("🧹 Limpar Arquivo TXT por Link")
st.write("Remove linhas que começam com `|C100|1|0||55|02|001|` e gera o mesmo arquivo original")

# Entrada do link e nome do arquivo original
url = st.text_input("📎 Cole o link direto do arquivo (.txt):")
nome_original = st.text_input("📝 Nome original do arquivo (ex: meu_arquivo.txt):")

if url and nome_original:
    try:
        st.info("📡 Baixando arquivo...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Cria arquivo temporário e processa linha por linha
        with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8") as output_file:
            count_total = 0
            count_removidas = 0

            for linha in response.iter_lines():
                linha_decodificada = linha.decode("utf-8")
                count_total += 1

                if not linha_decodificada.startswith("|C100|1|0||55|02|001|"):
                    output_file.write(linha_decodificada + "\n")
                else:
                    count_removidas += 1

            caminho_saida = output_file.name

        st.success(f"✅ Arquivo processado com sucesso!")
        st.write(f"🔹 Total de linhas: {count_total}")
        st.write(f"🗑️ Linhas removidas: {count_removidas}")

        # Botão de download com o mesmo nome original
        with open(caminho_saida, "rb") as f:
            st.download_button(
                label="📥 Baixar arquivo limpo",
                data=f,
                file_name=nome_original,
                mime="text/plain"
            )

    except Exception as e:
        st.error(f"❌ Erro: {e}")
