import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage

def responder_pergunta(pergunta, df_header, df_items, modelo, url, chave):
    contexto = "Você é um assistente especializado em dados de notas fiscais públicas."
    prompt = f"{contexto}\nPergunta: {pergunta}\nResponda com base nos dados CSV disponíveis."

    llm = ChatOpenAI(
        model=modelo,
        openai_api_base=url,
        openai_api_key=chave
    )

    resposta = llm([HumanMessage(content=prompt)])
    return resposta.content
