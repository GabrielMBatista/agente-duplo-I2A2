const fs = require('fs');
const path = require('path');

// Nome esperado da pasta do projeto
const expectedDirName = 'agente-duplo-notas-fiscais';
const currentDir = path.basename(process.cwd());

// Define o diretório base (cria apenas se necessário)
const baseDir = currentDir === expectedDirName
    ? process.cwd()
    : path.join(process.cwd(), expectedDirName);

// Subpastas necessárias
const subdirs = ['data', '.streamlit'];

// Arquivos com conteúdo
const files = {
    'requirements.txt': `pandas
streamlit
langchain
python-dotenv`,

    '.env.example': `OPENAI_API_KEY=coloque_sua_chave_aqui`,

    '.streamlit/secrets.toml': `OPENAI_API_KEY = "coloque_sua_chave_aqui"`,

    'README.md': `# Agente Duplo – IAGents

Sistema para análise de notas fiscais públicas com IA Generativa e visualização interativa via Streamlit.

## 🚀 Como rodar o projeto

1. Instale as dependências:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

2. Configure sua chave da API no .env ou diretamente na interface

3. Rode localmente:
\`\`\`bash
streamlit run main.py
\`\`\`
`,

    'agent.py': `import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

def responder_pergunta(pergunta, df_header, df_items, modelo, url, chave):
    contexto = "Você é um assistente especializado em dados de notas fiscais públicas."
    prompt = f"{contexto}\\nPergunta: {pergunta}\\nResponda com base nos dados CSV disponíveis."

    llm = ChatOpenAI(
        model=modelo,
        openai_api_base=url,
        openai_api_key=chave
    )

    resposta = llm([HumanMessage(content=prompt)])
    return resposta.content
`,

    'main.py': `import streamlit as st
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
`
};

// Criação da estrutura
function createStructure() {
    console.log("🚀 Iniciando criação de estrutura em:", baseDir);

    if (!fs.existsSync(baseDir)) {
        fs.mkdirSync(baseDir);
        console.log(`📁 Pasta criada: ${baseDir}`);
    }

    subdirs.forEach(sub => {
        const fullPath = path.join(baseDir, sub);
        if (!fs.existsSync(fullPath)) {
            fs.mkdirSync(fullPath, { recursive: true });
            console.log(`📂 Subpasta criada: ${fullPath}`);
        }
    });

    for (const [filename, content] of Object.entries(files)) {
        const fullPath = path.join(baseDir, filename);
        fs.writeFileSync(fullPath, content, 'utf-8');
        console.log(`✅ Arquivo criado: ${filename}`);
    }

    console.log("🎉 Projeto configurado com sucesso!");
}

createStructure();
