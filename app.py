import streamlit as st
from groq import Groq

# 1. Configuração visual da página
st.set_page_config(page_title="Professor Python", page_icon="professor.png", layout="centered")
col1, col2 = st.columns([1, 5]) # A coluna 2 é 5 vezes mais larga que a 1

with col1:
    # Mostra a imagem com uma largura de 80 pixels (você pode ajustar esse número)
    st.image("professor.png", width=80)

with col2:
    # O título agora fica na coluna ao lado, sem o emoji
    st.title("Professor Python")
st.write("Tire suas dúvidas de programação! Explico tudo com exemplos do dia a dia.")
st.caption("Desenvolvido por **Yan Enrique** © 2026")


# 2. Conexão com o cérebro da IA (Usando a chave de segurança do Streamlit)
cliente = Groq(api_key=st.secrets["GROQ_API_KEY"])
modelo_escolhido = "llama-3.1-8b-instant" # Um modelo super inteligente e rápido disponível no Groq

# 3. Regra de Ouro (System Prompt)
prompt_do_sistema = {
    "role": "system", 
    "content": """Você é o Professor Python, um tutor extremamente didático, animado e paciente. Sua missão é ensinar Python para iniciantes absolutos.

Siga ESTAS REGRAS ESTRUTURAIS obrigatoriamente, independentemente do tamanho da conversa:

1. PRIMEIRO CONTATO: Na primeira mensagem do usuário, apresente-se com muito entusiasmo como o Professor Python.
2. PROIBIÇÃO ABSOLUTA DE ACENTOS NO CÓDIGO (CRÍTICO): É ESTRITAMENTE PROIBIDO o uso de qualquer acento (á, é, í, ó, ú, ã, õ, ç, etc) ou apóstrofo (') DENTRO do bloco de código ```python. NUNCA escreva 'é_de_autor', escreva 'e_de_autor'. O código deve seguir a PEP 8 rigorosamente. Identificadores só podem ter letras sem acento, números e underlines.
3. TRILHA ESTRUTURADA: Se o usuário pedir "me ensine python", siga a ordem: 1) O que é python?, 2) Como instalar, 3) Imprimir (print), 4) Variáveis/Tipos, 5) Operadores Aritméticos, 6) Operadores de Comparação, 7) Condicionais, 8) Loops, 9) Listas/Tuplas/Dicionários, 10) Funções, 11) Introdução a POO, 12) POO em Python.
4. MICRO-APRENDIZADO E A REGRA DO ÚNICO BLOCO (CRÍTICO): Você DEVE entregar o conhecimento em migalhas. Para garantir isso, É ESTRITAMENTE PROIBIDO gerar mais de UM (1) único bloco de código Markdown (```python) por resposta. O bloco deve ter NO MÁXIMO 4 linhas. Entregue um conceito, um bloco curto, e PARE. Faça uma pergunta e espere o aluno responder.
5. OBRIGATÓRIO STORYTELLING: Toda explicação DEVE usar uma analogia divertida do dia a dia.
6. ESTRUTURA DA RESPOSTA:
   - Primeiro: O avanço na historinha/analogia.
   - Segundo: O ÚNICO bloco de código (max 4 linhas).
   - Terceiro: Tradução contextualizada (ex: "o if é o chef olhando a geladeira").
   - Quarto: Uma pergunta ou pequeno desafio para o aluno digitar antes de você avançar.
7. LIMITAÇÃO E IDIOMA: Responda APENAS em português brasileiro. Se não for Python, faça uma piada de cobra e mude de assunto.
8. TOM DE VOZ: Amigável e encorajador. Use emojis 🐍."""
}

# 4. Memória da conversa
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [prompt_do_sistema]

# 5. Mostra o histórico na tela (ignorando a regra do sistema para não aparecer pro usuário)
for msg in st.session_state.mensagens:
    if msg["role"] != "system":
        icone = "professor.png" if msg["role"] == "assistant" else "👤"
        with st.chat_message(msg["role"], avatar=icone):
            st.markdown(msg["content"])

# 6. Caixa de texto para o usuário digitar
pergunta = st.chat_input("Ex: Me ensine Python")

if pergunta:
    # Mostra a pergunta na tela e salva na memória
    with st.chat_message("user", avatar="👤"):
        st.markdown(pergunta)
    st.session_state.mensagens.append({"role": "user", "content": pergunta})

    # Chama a API do Groq para gerar a resposta
    with st.chat_message("assistant", avatar="professor.png"):
        resposta_placeholder = st.empty()
        
        try:
            # Envia o histórico completo para a IA
            resposta_ia = cliente.chat.completions.create(
                model=modelo_escolhido,
                messages=st.session_state.mensagens,
                temperature=0.7 # Controla a criatividade (0 a 1)
            )
            
            texto_final = resposta_ia.choices[0].message.content
            resposta_placeholder.markdown(texto_final)
            
            # Salva a resposta na memória
            st.session_state.mensagens.append({"role": "assistant", "content": texto_final})
            
        except Exception as e:
            # Se a Groq bloquear por excesso de requisições, mostra o aviso amigável
            mensagem_erro = "Poxa, muita gente da turma perguntando ao mesmo tempo! O professor aqui retorna em 1 minuto."
            resposta_placeholder.error(mensagem_erro)
