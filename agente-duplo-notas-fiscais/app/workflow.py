from llm_selector import get_llm
from langchain.schema.messages import HumanMessage


def resumir_df_header(df):
    return {
        "total_notas": len(df),
        "valor_total": df["valorTotal"].sum(),
        "media_valor": df["valorTotal"].mean(),
        "fornecedor_mais_frequente": df["nomeFornecedor"].mode()[0] if not df["nomeFornecedor"].mode().empty else "N/A",
    }


def resumir_df_items(df):
    return {
        "total_itens": len(df),
        "item_mais_frequente": df["descricaoItem"].mode()[0] if not df["descricaoItem"].mode().empty else "N/A",
        "maior_quantidade": df["quantidadeItem"].max(),
        "item_maior_valor_unitario": df.sort_values(by="valorUnitarioItem", ascending=False)["descricaoItem"].iloc[0]
        if not df.empty else "N/A",
    }


def responder_pergunta(pergunta, df_header, df_items, modelo, url, api_key):
    try:
        resumo_header = resumir_df_header(df_header)
        resumo_items = resumir_df_items(df_items)

        prompt = f"""
Você é um agente de IA especializado em análise de dados públicos, com foco em notas fiscais brasileiras.

Sua tarefa é responder perguntas com base nas informações abaixo. Os dados foram extraídos de sistemas públicos e representam notas fiscais emitidas em janeiro de 2024.

---

📊 **Resumo: Cabeçalho das Notas Fiscais**
- Total de notas fiscais: {resumo_header['total_notas']}
- Valor total: R$ {resumo_header['valor_total']:,.2f}
- Valor médio: R$ {resumo_header['media_valor']:,.2f}
- Fornecedor mais frequente: {resumo_header['fornecedor_mais_frequente']}

📊 **Resumo: Itens das Notas Fiscais**
- Total de itens: {resumo_items['total_itens']}
- Item mais frequente: {resumo_items['item_mais_frequente']}
- Maior quantidade em um item: {resumo_items['maior_quantidade']}
- Item com maior valor unitário: {resumo_items['item_maior_valor_unitario']}

---

❗ Observações:
- Este é um resumo dos dados completos, focado em estatísticas relevantes.
- Utilize seu raciocínio para interpretar nomes de colunas e dados relacionados.
- Relacione, quando necessário, as duas tabelas com base em colunas comuns (ex: número da nota, CNPJ, etc.).
- Caso o resumo não seja suficiente para uma resposta precisa, avise o usuário.

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
