from llm_selector import get_llm
from langchain.schema.messages import HumanMessage


def responder_pergunta(pergunta, df_header, df_items, modelo, url, api_key):
    try:
        # Seleciona uma amostra razoável para o modelo entender o conteúdo sem estourar o limite de tokens
        header_sample = df_header.head(100).to_markdown(index=False)
        items_sample = df_items.head(100).to_markdown(index=False)

        prompt = f"""
Você é um agente de IA especializado em análise de dados públicos, com foco em notas fiscais brasileiras.

Sua tarefa é responder perguntas com base nas tabelas fornecidas abaixo. Os dados foram extraídos de sistemas públicos e representam notas fiscais emitidas em janeiro de 2024.

---

📄 Tabela: Cabeçalho das Notas Fiscais (amostra)
{header_sample}

📄 Tabela: Itens das Notas Fiscais (amostra)
{items_sample}

---

❗ Observações:
- Os dados exibidos são apenas uma amostra (10 linhas de cada tabela).
- Utilize seu raciocínio para interpretar os nomes das colunas e o significado dos dados.
- Se necessário, relacione as duas tabelas com base em colunas em comum (como número da nota, CNPJ, etc.).
- Caso a amostra não seja suficiente para uma resposta precisa, avise o usuário.

---

💬 Pergunta do usuário:
{pergunta}

🎯 Regras para resposta:
- Escreva em português.
- Seja direto e profissional.
- Destaque valores monetários com separador de milhar e vírgula decimal (ex: R$ 12.345,67).
- Se não houver dados suficientes, diga claramente que não é possível responder com precisão.
"""

        llm = get_llm(modelo, api_key, url)
        resposta = llm.invoke([HumanMessage(content=prompt)])
        return resposta.content

    except Exception as e:
        return f"❌ Erro no processamento: {str(e)}"
