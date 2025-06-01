import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel


def get_llm(modelo: str, api_key: str | None, base_url: str) -> BaseChatModel:
    if modelo == "deepseek-custom":
        api_key = st.secrets["deepseek"]["api_key"]
        return ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model="deepseek-chat"
        )

    elif modelo == "custom":
        return ChatOpenAI(
            api_key=api_key,
            base_url=base_url,
            model="gpt-3.5-turbo"
        )

    else:
        raise ValueError(f"Modelo não suportado: {modelo}")
