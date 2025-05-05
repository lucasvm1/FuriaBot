# 🔥 Chatbot FURIA CS2 — Torcida Online

Chatbot interativo para fãs da FURIA, desenvolvido com Streamlit e OpenAI. Responde perguntas sobre escalação, histórico de partidas e curiosidades da equipe com linguagem descontraída e tom de torcedor animado.

## 📦 Funcionalidades

- Consulta dinâmica sobre:
  - Escalação atual
  - Histórico recente de partidas
  - Informações da organização
- Respostas animadas com emojis e linguagem de torcida
- Foco exclusivo em informações do JSON de base
- Interface via Streamlit com chat interativo
- Atualizado até: **abril de 2025**

## 🧠 Tecnologias

- [Streamlit](https://streamlit.io/)
- [OpenAI API](https://platform.openai.com/)
- Python 3.10+

## 🗂️ Estrutura

```
.
├── app.py                # Código principal
├── furia_completa.json  # Base de dados da equipe
├── .venv/                # Ambiente virtual (recomendado)
└── README.md             # Este arquivo
```

## ⚙️ Como rodar

1. Crie um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Defina sua chave da API OpenAI:
   ```bash
   export OPENAI_API_KEY='sua-chave-aqui'  # Linux/macOS
   set OPENAI_API_KEY=sua-chave-aqui       # Windows
   ```

4. Inicie o app:
   ```bash
   streamlit run app.py
   ```

## 📁 Base de Dados

O chatbot usa o arquivo `furia_completa.json`, com a seguinte estrutura (exemplo simplificado):

```json
{
  "team": {
    "full_name": "FURIA Esports",
    "location": "Brasil",
    "founded": "2017",
    "active_roster": [...],
    "coach": {...},
    "recent_matches": [...]
  }
}
```

## 💬 Exemplos de Perguntas

- "Quem está na line-up atual?"
- "Qual foi o resultado contra a NAVI?"
- "Quem é o coach da FURIA?"
- "Quais foram as últimas partidas?"

## 🛡️ Limitações

- Usa apenas o conteúdo do JSON como base de conhecimento
- Se faltar informação, o bot avisa com transparência
- Necessário conexão com a OpenAI API


