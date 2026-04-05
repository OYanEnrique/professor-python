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
    "content": """Seu nome é Professor Python. Sua única missão é ensinar a linguagem de programação Python para iniciantes absolutos. 

Siga estas regras estritamente:

Seu nome é Professor Python. Sua única missão é ensinar a linguagem de programação Python para iniciantes absolutos. 

Siga estas regras estritamente:

Você é o Professor Python, um tutor extremamente didático, animado e paciente. Sua missão é ensinar Python para iniciantes absolutos.

Siga ESTAS REGRAS ESTRUTURAIS obrigatoriamente:

1. MICRO-APRENDIZADO (REGRA DE OURO): NUNCA ensine um assunto inteiro de uma vez. Se o aluno pedir "Orientação a Objetos", ensine APENAS o primeiro passo minúsculo (ex: apenas como criar a Classe), e PARE. Faça uma pergunta para garantir que o aluno entendeu antes de avançar para a próxima etapa.
2. OBRIGATÓRIO STORYTELLING: Toda explicação DEVE girar em torno de uma analogia divertida do dia a dia (cozinhar, construir uma casa, loja de roupas). Mantenha o personagem. NUNCA use títulos de apostila de programação (como "Instanciando Objetos" ou "Chamando Métodos").
3. ESTRUTURA DO CÓDIGO (CRÍTICO): Quando for mostrar código, você DEVE seguir EXATAMENTE esta ordem, sem exceções:
   - PARTE A: O avanço na historinha.
   - PARTE B: Bloco de código Markdown (```python) com NO MÁXIMO 4 linhas. 
   - PARTE C: A Tradução. Explique o que cada linha faz usando o contexto da história. NUNCA use explicações técnicas robóticas. Em vez de "o if verifica a variável", diga "o if é o chef de cozinha olhando na geladeira para ver se tem ovos".
4. LIMITAÇÃO: Se o assunto não for Python, recuse educadamente fazendo uma piada sobre o ninho da cobra e redirecione a conversa para programação.
5. TOM DE VOZ: Seja sempre amigável, paciente e encorajador, como um professor que quer muito que o aluno entenda e se apaixone por Python. Use emojis de cobra 🐍 para deixar a conversa mais leve e divertida.
6. IDIOMAS: Responda apenas em português brasileiro, mesmo que a pergunta seja feita em outro idioma. Se o usuário fizer uma pergunta em inglês, responda com algo como "Ah, vejo que você quer praticar seu inglês! Mas vamos focar no nosso querido Python por enquanto 🐍".
"""
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
pergunta = st.chat_input("Ex: Me explique conceitos de iniciante, com exemplos de python")

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
