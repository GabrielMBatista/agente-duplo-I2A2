
from llm_selector import get_llm
from langchain.schema.messages import HumanMessage


def resumo_cabecalho(df):
    return {
        "total_notas": len(df),
        "valor_total": df["VALOR NOTA FISCAL"].sum(),
        "valor_médio": df["VALOR NOTA FISCAL"].mean(),
        "valor_máximo": df["VALOR NOTA FISCAL"].max(),
        "valor_mínimo": df["VALOR NOTA FISCAL"].min(),
        "nota_maior_valor": df.loc[df["VALOR NOTA FISCAL"].idxmax()].to_dict(),
        "uf_emitente_mais_comum": df["UF EMITENTE"].mode()[0],
        "destino_mais_comum": df["DESTINO DA OPERAÇÃO"].mode()[0],
        "presença_comprador_mais_comum": df["PRESENÇA DO COMPRADOR"].mode()[0],
        "total_emitentes_distintos": df["RAZÃO SOCIAL EMITENTE"].nunique(),
        "destinatário_mais_comum": df["NOME DESTINATÁRIO"].mode()[0],
    }


def resumo_itens(df):
    return {
        "total_itens": len(df),
        "quantidade_total": df["QUANTIDADE"].sum(),
        "quantidade_média": df["QUANTIDADE"].mean(),
        "valor_unitário_médio": df["VALOR UNITÁRIO"].mean(),
        "valor_total_geral": df["VALOR TOTAL"].sum(),
        "item_mais_comum": df["DESCRIÇÃO DO PRODUTO/SERVIÇO"].mode()[0],
        "item_maior_valor_unitario": df.loc[df["VALOR UNITÁRIO"].idxmax()].to_dict(),
        "item_maior_valor_total": df.loc[df["VALOR TOTAL"].idxmax()].to_dict(),
        "tipo_produto_mais_comum": df["NCM/SH (TIPO DE PRODUTO)"].mode()[0],
        "unidade_mais_utilizada": df["UNIDADE"].mode()[0],
        "nota_com_mais_itens": df["CHAVE DE ACESSO"].value_counts().idxmax(),
    }


def responder_pergunta(pergunta, df_header, df_items, modelo, url, api_key):
    try:
        resumo_header = resumo_cabecalho(df_header)
        resumo_items = resumo_itens(df_items)

        prompt = f"""
Você é um agente de IA especializado em análise de dados públicos, com foco em notas fiscais brasileiras.

Sua tarefa é responder perguntas com base nas informações abaixo. Os dados foram extraídos de sistemas públicos e representam notas fiscais emitidas em janeiro de 2024.

---

📊 **Resumo: Cabeçalho das Notas Fiscais**
- Total de notas fiscais: {resumo_header['total_notas']}
- Valor total: R$ {resumo_header['valor_total']:,.2f}
- Valor médio: R$ {resumo_header['valor_médio']:,.2f}
- Valor máximo: R$ {resumo_header['valor_máximo']:,.2f}
- Valor mínimo: R$ {resumo_header['valor_mínimo']:,.2f}
- UF emitente mais comum: {resumo_header['uf_emitente_mais_comum']}
- Destino mais comum: {resumo_header['destino_mais_comum']}
- Presença do comprador mais comum: {resumo_header['presença_comprador_mais_comum']}
- Total de emitentes distintos: {resumo_header['total_emitentes_distintos']}
- Destinatário mais comum: {resumo_header['destinatário_mais_comum']}

📄 **Nota com maior valor:**
{resumo_header['nota_maior_valor']}

---

📦 **Resumo: Itens das Notas Fiscais**
- Total de itens: {resumo_items['total_itens']}
- Quantidade total: {resumo_items['quantidade_total']}
- Quantidade média por item: {resumo_items['quantidade_média']:.2f}
- Valor unitário médio: R$ {resumo_items['valor_unitário_médio']:,.2f}
- Valor total geral: R$ {resumo_items['valor_total_geral']:,.2f}
- Item mais comum: {resumo_items['item_mais_comum']}
- Tipo de produto mais comum (NCM): {resumo_items['tipo_produto_mais_comum']}
- Unidade mais utilizada: {resumo_items['unidade_mais_utilizada']}
- Nota com maior número de itens: {resumo_items['nota_com_mais_itens']}

📄 **Item com maior valor unitário:**
{resumo_items['item_maior_valor_unitario']}

📄 **Item com maior valor total:**
{resumo_items['item_maior_valor_total']}

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
