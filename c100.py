import streamlit as st
import zipfile
import tempfile
import os

st.set_page_config(page_title="Limpar TXT e gerar auditoria", layout="centered")
st.title("📦 Limpar TXT de ZIP + Gerar Auditoria")

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
            nome_txt = arquivos_txt[0]
            caminho_txt = os.path.join(temp_dir, nome_txt)
            caminho_corrigido = os.path.join(temp_dir, nome_txt)
            nome_auditoria = nome_txt.replace(".txt", "_removidas.txt")
            caminho_auditoria = os.path.join(temp_dir, nome_auditoria)

            count_total = 0
            count_removidas = 0

            with open(caminho_txt, "r", encoding="utf-8", errors="ignore") as original, \
                 open(caminho_corrigido, "w", encoding="utf-8") as saida_corrigido, \
                 open(caminho_auditoria, "w", encoding="utf-8") as saida_auditoria:

                for linha in original:
                    count_total += 1
                    if not linha.startswith("|C100|1|0||55|02|001|"):
                        saida_corrigido.write(linha)
                    else:
                        saida_auditoria.write(linha)
                        count_removidas += 1

            st.success(f"✅ Arquivo `{nome_txt}` processado com sucesso!")
            st.write(f"🔹 Total de linhas: {count_total}")
            st.write(f"🗑️ Linhas removidas: {count_removidas}")

            # Botão para baixar o arquivo corrigido
            with open(caminho_corrigido, "rb") as f_corrigido:
                st.download_button(
                    label="📥 Baixar arquivo corrigido",
                    data=f_corrigido,
                    file_name=nome_txt,
                    mime="text/plain"
                )

            # Botão para baixar o arquivo de auditoria
            with open(caminho_auditoria, "rb") as f_auditoria:
                st.download_button(
                    label="📋 Baixar arquivo de auditoria (linhas removidas)",
                    data=f_auditoria,
                    file_name=nome_auditoria,
                    mime="text/plain"
                )
