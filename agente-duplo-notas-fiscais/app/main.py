import streamlit as st
import zipfile
import pandas as pd
import os
from workflow import responder_pergunta

st.set_page_config(page_title="IAGents - Análise de Notas Fiscais Públicas")
st.title("🧾 IAGents - Análise de Notas Fiscais Públicas")

# Escolha do modelo
modelo = st.selectbox(
    "Escolha o modelo de IA:",
    ["deepseek-custom", "custom"],
    index=0
)

# Para modelo custom, o usuário fornece a chave e URL
api_key = None
api_url = None

if modelo == "custom":
    api_key = st.text_input("Sua chave de API:", type="password")
    api_url = st.text_input(
        "URL da API:", placeholder="https://sua-api.com/v1")
else:
    # URLs padrões para os modelos que usam secrets
    default_urls = {
        "deepseek-custom": "https://api.deepseek.com/v1"
    }
    api_url = default_urls[modelo]

# Upload do ZIP
uploaded_file = st.file_uploader(
    "Envie o arquivo .zip contendo os CSVs", type="zip")

if uploaded_file:
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall("data_temp")

    try:
        df_header = pd.read_csv("data_temp/202401_NFs_Cabecalho.csv")
        df_items = pd.read_csv("data_temp/202401_NFs_Itens.csv")
    except Exception as e:
        st.error(f"Erro ao ler os arquivos CSV: {e}")
        df_header, df_items = None, None

    pergunta = st.text_area("Digite sua pergunta sobre os dados:")

    if st.button("🔍 Analisar") and pergunta and df_header is not None and df_items is not None:
        resposta = responder_pergunta(
            pergunta, df_header, df_items, modelo, api_url, api_key
        )
        st.markdown(f"💬 **Resposta:**\n\n{resposta}")

    # Limpeza opcional
    if os.path.exists("data_temp"):
        for file in os.listdir("data_temp"):
            os.remove(f"data_temp/{file}")
        os.rmdir("data_temp")
