import streamlit as st
import pandas as pd
import zipfile
import os
import tempfile
from agent import responder_pergunta

st.set_page_config(page_title="IAGents", layout="wide")
st.title("🧾 IAGents - Análise de Notas Fiscais Públicas")

llm_opcoes = {
    "DeepSeek": {
        "modelo": "deepseek-chat",
        "url": "https://api.deepseek.com/v1"
    },
    "OpenAI (GPT-3.5)": {
        "modelo": "gpt-3.5-turbo",
        "url": "https://api.openai.com/v1"
    },
    "OpenRouter (Mistral)": {
        "modelo": "mistral",
        "url": "https://openrouter.ai/api/v1"
    }
}

opcao = st.selectbox("Escolha o modelo de IA:", list(llm_opcoes.keys()))
api_key = st.text_input("Sua chave de API:", type="password")

zip_file = st.file_uploader("Envie o arquivo .zip contendo os CSVs", type="zip")

if zip_file and api_key:
    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(tmpdir)

        csv1 = os.path.join(tmpdir, "202401_NFs_Cabecalho.csv")
        csv2 = os.path.join(tmpdir, "202401_NFs_Itens.csv")

        if os.path.exists(csv1) and os.path.exists(csv2):
            df_header = pd.read_csv(csv1)
            df_items = pd.read_csv(csv2)

            pergunta = st.text_input("Digite sua pergunta sobre os dados:")

            if pergunta:
                modelo = llm_opcoes[opcao]["modelo"]
                url = llm_opcoes[opcao]["url"]
                resposta = responder_pergunta(pergunta, df_header, df_items, modelo, url, api_key)
                st.write("📊 Resposta:")
                st.success(resposta)
        else:
            st.error("Arquivos CSV esperados não encontrados no ZIP.")
