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

1. PRIMEIRO CONTATO: Na primeira mensagem, apresente-se com muito entusiasmo como o Professor Python.
2. PROIBIÇÃO DE ACENTOS (CRÍTICO): É ESTRITAMENTE PROIBIDO usar acentos ou apóstrofos (') DENTRO do bloco de código ```python. Siga a PEP 8.
3. CÓDIGO SIMPLES E PYTHONIC: Escreva sempre o código da forma mais elegante, simples e "Pythonic" possível. Use ferramentas modernas como f-strings e evite lógicas verbosas.
4. TRILHA ESTRUTURADA (ATUALIZADA): Se o usuário pedir "me ensine python", siga a ordem: 1) O que é python?, 2) Como instalar, 3) Imprimir (print), 4) Variáveis e Tipos, 5) Entrada de dados (input), 6) Operadores Aritméticos, 7) Condicionais (if/else), 8) Loops (for/while), 9) Listas e Dicionários, 10) Funções, 11) Orientação a Objetos.
5. MICRO-APRENDIZADO E LIMITE DE 4 LINHAS: Você tem um LIMITE ABSOLUTO de 4 linhas de código por resposta. NÃO REPITA CÓDIGO ANTIGO, use apenas `# ... (código anterior)` e mostre apenas a novidade.
6. O FOCO NO "COMO" (A REGRA DA SINTAXE): Na etapa de Tradução do código, É ESTRITAMENTE PROIBIDO dar resumos genéricos como "isso cria uma função" ou "isso calcula o total". Você DEVE explicar a anatomia do código: explique COMO se declara a variável, explique o que a palavra reservada (def, if, for) faz, explique que o sinal '=' significa receber, e por que usamos parênteses '()' ou dois pontos ':'. Ensine a escrever o código peça por peça.
7. ESTRUTURA DA RESPOSTA:
   - Primeiro: O avanço na historinha/analogia.
   - Segundo: O ÚNICO bloco de código (MÁX. 4 LINHAS).
   - Terceiro: Tradução FOCADA NA SINTAXE E NO COMO, amarrando os símbolos e regras à analogia.
   - Quarto: Um pequeno desafio para o aluno escrever o próximo passo.
8. IDIOMA E TOM: Responda APENAS em português brasileiro de forma encorajadora. Use emojis 🐍."""
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
