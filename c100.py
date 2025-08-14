import streamlit as st
import zipfile
import tempfile
import os

st.set_page_config(page_title="Limpar TXT de ZIP", layout="centered")
st.title("📦 Limpar TXT de ZIP automaticamente")

uploaded_zip = st.file_uploader("📂 Faça upload de um arquivo .zip contendo um .txt", type=["zip"])

if uploaded_zip is not None:
    with tempfile.TemporaryDirectory() as temp_dir:
        # Salva o zip no diretório temporário
        zip_path = os.path.join(temp_dir, "arquivo.zip")
        with open(zip_path, "wb") as f:
            f.write(uploaded_zip.read())

        # Extrai o ZIP
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)
            arquivos_txt = [f for f in zip_ref.namelist() if f.endswith(".txt")]

        if not arquivos_txt:
            st.error("❌ Nenhum arquivo .txt encontrado no ZIP.")
        else:
            # Pega o primeiro .txt encontrado
            nome_txt = arquivos_txt[0]
            caminho_txt = os.path.join(temp_dir, nome_txt)
            caminho_corrigido = os.path.join(temp_dir, nome_txt)

            count_total = 0
            count_removidas = 0

            # Lê e processa o arquivo (sobrescreve o original)
            with open(caminho_txt, "r", encoding="utf-8", errors="ignore") as original:
                linhas = original.readlines()

            with open(caminho_corrigido, "w", encoding="utf-8") as saida:
                for linha in linhas:
                    count_total += 1
                    if not linha.startswith("|C100|1|0||55|02|001|"):
                        saida.write(linha)
                    else:
                        count_removidas += 1

            st.success(f"✅ Processado com sucesso!")
            st.write(f"📄 Arquivo: `{nome_txt}`")
            st.write(f"🔹 Total de linhas: {count_total}")
            st.write(f"🗑️ Linhas removidas: {count_removidas}")

            # Cria botão de download imediatamente
            with open(caminho_corrigido, "rb") as f:
                st.download_button(
                    label="📥 Baixar arquivo corrigido",
                    data=f,
                    file_name=nome_txt,
                    mime="text/plain"
                )
