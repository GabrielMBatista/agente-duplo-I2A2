# 🧾 IAGents - Análise de Notas Fiscais Públicas

Este projeto permite ao usuário consultar dados públicos de notas fiscais (CSV) com uma interface de IA generativa.

## 🚀 Executar localmente

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app/main.py
```

## 🌐 Modelos suportados
- ✅ deepseek-chat (padrão)
- OpenAI, Mistral, OpenRouter...

## 🔐 .env (exemplo)
```
MODEL=deepseek-chat
API_KEY=sua-chave-aqui
API_URL=https://api.deepseek.com/v1
```
