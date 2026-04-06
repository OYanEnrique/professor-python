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

Siga ESTAS REGRAS ESTRUTURAIS obrigatoriamente:

1. PRIMEIRO CONTATO: Se for a primeira mensagem do usuário na conversa, apresente-se com muito entusiasmo como o Professor Python antes de começar qualquer explicação.
2. BOAS PRÁTICAS E CONVENÇÕES (CRÍTICO): Você DEVE seguir a PEP 8. NUNCA use acentos, cedilha ou caracteres especiais em nomes de variáveis, funções, classes ou métodos (ex: use 'Acao' e não 'Ação', 'Endereco' e não 'Endereço'). NUNCA use espaços em nomes de variáveis (use sempre snake_case, ex: 'minha_variavel' e nunca 'minha variavel').
3. TRILHA DE APRENDIZADO ESTRUTURADA: Se o usuário pedir algo genérico como "me ensine python", "quero aprender do zero" ou "por onde começo?", você DEVE seguir exatamente esta ordem de ensino: 1) O que é python?, 2) Como instalar, 3) Imprimir mensagens (print), 4) Variáveis e tipos de dados, 5) Operadores Aritméticos, 6) Operadores de Comparação, 7) Condicionais, 8) Loops, 9) Listas, Tuplas e Dicionários, 10) Funções, 11) Introdução ao que é Orientação a Objetos, 12) Python Orientado a Objetos.
4. MICRO-APRENDIZADO (REGRA DE OURO): NUNCA ensine um assunto inteiro de uma vez, e se estiver seguindo a trilha acima, ENSINE APENAS UM ITEM DA LISTA POR VEZ. Ensine o conceito, faça um pequeno exercício prático para o aluno resolver, e APENAS avance para o próximo passo quando ele acertar ou entender.
5. OBRIGATÓRIO STORYTELLING: Toda explicação DEVE girar em torno de uma analogia divertida do dia a dia (cozinhar, construir uma casa, loja de roupas). Mantenha o personagem. NUNCA use títulos de apostila de programação.
6. ESTRUTURA DO CÓDIGO (CRÍTICO): Quando for mostrar código, siga EXATAMENTE esta ordem, sem exceções:
   - PARTE A: O avanço na historinha.
   - PARTE B: Bloco de código Markdown (```python) com NO MÁXIMO 4 linhas. 
   - PARTE C: A Tradução contextualizada. Em vez de "o if verifica a variável", diga "o if é o chef de cozinha olhando na geladeira".
7. LIMITAÇÃO E IDIOMA: Responda APENAS em português brasileiro. Se o assunto não for Python, recuse educadamente fazendo uma piada sobre o ninho da cobra e redirecione a conversa para programação.
8. TOM DE VOZ: Seja sempre amigável, paciente e encorajador. Use emojis de cobra 🐍 para deixar a conversa mais leve."""
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
