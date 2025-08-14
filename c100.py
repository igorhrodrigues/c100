import streamlit as st
import requests
import tempfile

st.set_page_config(page_title="Limpar TXT via Link", layout="centered")
st.title("📥 Limpar Arquivo TXT por Link")
st.write("Baixa o arquivo direto do Google Drive e remove linhas que começam com `|C100|1|0||55|02|001|`")

url = st.text_input("Cole aqui o link de download direto (ex: Google Drive):")

if url:
    try:
        # Faz download do arquivo
        st.info("📡 Baixando arquivo...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Cria arquivo temporário para salvar o conteúdo
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

            caminho_arquivo_limpo = output_file.name

        st.success(f"✅ Arquivo processado com sucesso!")
        st.write(f"🔹 Linhas totais: {count_total}")
        st.write(f"🗑️ Linhas removidas: {count_removidas}")

        # Botão de download
        with open(caminho_arquivo_limpo, "rb") as f:
            st.download_button(
                label="📥 Baixar arquivo limpo",
                data=f,
                file_name="arquivo_limpo.txt",
                mime="text/plain"
            )

    except Exception as e:
        st.error(f"❌ Erro ao baixar ou processar o arquivo: {e}")
