import streamlit as st
import json
import openai
import os
import random

# ------------------------------ Configuração ------------------------------
JSON_PATH = "furia_completa.json"  # arquivo com todos os dados da equipe
MODEL_NAME = "gpt-4o-mini"          # ajuste conforme seu plano
DATA_CUTOFF = "abril de 2025"       # até quando as estatísticas estão atualizadas

# ------------------------- Camada de Conhecimento -------------------------
class BaseDeDadosFuria:
    """Carrega o JSON da FURIA e gera fatos estruturados."""

    def __init__(self, dados_time: dict):
        self.dados_time = dados_time
        self.fatos = self._preparar_fatos()

    # ---------------------------------------------------------------------
    # Geração de fatos
    # ---------------------------------------------------------------------
    def _preparar_fatos(self) -> list[str]:
        fatos: list[str] = []
        t = self.dados_time

        loc = t.get("location", "Brasil")
        year = t.get("founded", "2017")
        fatos.append(
            f"A FURIA é uma organização brasileira de e‑sports sediada em {loc}, fundada em {year}."
        )

        # data‑cutoff explícita para transparência
        fatos.append(f"Dados atualizados até {DATA_CUTOFF}.")

        fatos.append("Jogadores ativos:")
        for p in t.get("active_roster", []):
            pid = p.get("id", "?")
            nome = p.get("name", "?")
            role = p.get("role")
            fatos.append(f"- {nome} ({pid}{', ' + role if role else ''})")

        if coach := t.get("coach"):
            fatos.append(f"Coach: {coach.get('name')} ({coach.get('id')})")

        if matches := t.get("recent_matches"):
            fatos.append("Últimas 50 partidas:")
            for m in matches[:50]:
                data = m.get("date")
                torneio = m.get("tournament")
                opp = m.get("opponent")
                score = m.get("score")
                fatos.append(f"- {data}: {torneio} vs {opp} resultado {score}")

        return fatos

    # ---------------------------------------------------------------------
    # Recuperação de contexto
    # ---------------------------------------------------------------------
    def obter_contexto_para_consulta(self, consulta: str) -> str:
        contexto: list[str] = []

        if "Jogadores ativos:" in self.fatos:
            i = self.fatos.index("Jogadores ativos:")
            contexto.extend(self.fatos[i : i + 1])
            for linha in self.fatos[i + 1 :]:
                if linha.startswith("-"):
                    contexto.append(linha)
                else:
                    break

        if "Últimas 50 partidas:" in self.fatos:
            j = self.fatos.index("Últimas 50 partidas:")
            contexto.extend(self.fatos[j : j + 1 + 50])

        palavras = consulta.lower().split()
        relevantes = [
            f for f in self.fatos
            if any(p in f.lower() for p in palavras) and f not in contexto
        ][:20]

        return "\n".join(contexto + relevantes)

# ------------------------------ Utilidades ------------------------------

def carregar_dados() -> dict:
    with open(JSON_PATH, "r", encoding="utf-8") as fp:
        return json.load(fp)["team"]

@st.cache_resource(show_spinner=False)
def inicializar_base():
    return BaseDeDadosFuria(carregar_dados())

CHEERS = [
    "🔥 Bora FURIA!",
    "💥 É nóis na tela!",
    "🐆 Rooooar Pantera!",
    "🚀 Partiu highlight!",
    "🎉 Vamo que vamo!",
    "🏆 Rumo ao topo!",
    "⚡ Energia lá em cima!",
]


def obter_resposta_openai(pergunta: str, contexto: str) -> str:
    sistema = (
        "Você é um torcedor apaixonado da FURIA CS2 e assistente técnico. "
        "O corte de dados é " + DATA_CUTOFF + ". "
        "Responda com entusiasmo, emojis e expressões variadas de torcida (sem repetir a mesma na resposta). "
        "Se a pergunta for mera saudação, cumprimente de forma animada e breve. "
        "Use somente o CONTEXTO fornecido; se faltar informação específica, diga 'Não encontrei essa info agora 😅'."
    )

    mensagens = [
        {"role": "system", "content": sistema},
        {"role": "system", "content": f"Contexto:\n{contexto}"},
        {"role": "user", "content": pergunta},
    ]

    resposta = openai.chat.completions.create(
        model=MODEL_NAME,
        messages=mensagens,
        temperature=0.7,
        max_tokens=1024,
    ).choices[0].message.content.strip()

    return resposta

# ------------------------------ Interface ------------------------------

st.set_page_config(page_title="FURIA Chatbot", page_icon="🔥")
st.title("🔥 Chatbot FURIA CS2 — Torcida Online")
st.caption(f"Dados até {DATA_CUTOFF}. Pergunte estatísticas, histórico, escalação ou só grite pela Pantera!")

if not os.getenv("OPENAI_API_KEY"):
    st.error("Defina a variável de ambiente OPENAI_API_KEY antes de usar o app.")
    st.stop()

if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

base_dados = inicializar_base()

for mensagem in st.session_state.mensagens:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])

pergunta = st.chat_input("Manda tua pergunta aí, FURIOSO! 🐆")
if pergunta:
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    with st.spinner(random.choice(CHEERS)):
        contexto = base_dados.obter_contexto_para_consulta(pergunta)
        resposta = obter_resposta_openai(pergunta, contexto)

    st.session_state.mensagens.append({"role": "assistant", "content": resposta})
    with st.chat_message("assistant"):
        st.markdown(resposta)
