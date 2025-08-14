import streamlit as st
import requests
import tempfile
import os

st.set_page_config(page_title="Limpar TXT sem alterar estrutura", layout="centered")
st.title("🧹 Limpar Arquivo TXT por Link")
st.write("Remove apenas as linhas `|C100|1|0||55|02|001|`, mantendo tudo igual ao original")

# Inputs do usuário
url = st.text_input("📎 Link direto do arquivo (.txt):")
nome_original = st.text_input("📝 Nome original do arquivo (ex: sped.txt):")

if url and nome_original:
    try:
        st.info("📡 Baixando arquivo...")

        # Faz o download
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Nome do arquivo temporário de saída
        with tempfile.NamedTemporaryFile(delete=False, mode="w", encoding="utf-8") as output_file:
            count_total = 0
            count_removidas = 0

            for linha_bytes in response.iter_lines():
                linha = linha_bytes.decode("utf-8", errors="ignore")  # mantém codificação segura
                count_total += 1

                if not linha.startswith("|C100|1|0||55|02|001|"):
                    output_file.write(linha + "\n")
                else:
                    count_removidas += 1

            caminho_saida = output_file.name

        st.success(f"✅ Arquivo processado com sucesso!")
        st.write(f"🔹 Total de linhas: {count_total}")
        st.write(f"🗑️ Linhas removidas: {count_removidas}")

        # Botão de download com mesmo nome original
        with open(caminho_saida, "rb") as f:
            st.download_button(
                label="📥 Baixar arquivo limpo",
                data=f,
                file_name=nome_original,
                mime="text/plain"
            )

    except Exception as e:
        st.error(f"❌ Erro ao processar: {e}")
