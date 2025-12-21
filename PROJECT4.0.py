import streamlit as st
from dotenv import load_dotenv
import os
import base64
from datetime import datetime


from utils.gemini_init_function import init_gemini_client
from utils.gemini_init_function import init_connection_mongo
from tools.mongodb_rag import load_embedding_model
from tools.mongodb_rag import retrieve_context
from tools.scrapping_tool import scrape_horario
from utils.chat_history import get_gemini_history
from utils.langfuse_function import generate_response_with_tools_and_langfuse


#Data Base of numbers and passwords
dic={st.secrets["user1"]: st.secrets["pass1"], st.secrets["user2"]: st.secrets['pass2']}


#*PARTE DO DESIGN DO CHATBOT*
#FUNDO
image_path = os.path.join(os.path.dirname(__file__), "fundo verde com simbolo branco.png")

with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
    </style>
""", unsafe_allow_html=True)


#DESIGN GERAL
st.markdown("""
    <style>
        /* --- ESPECÍFICO PARA A TOOLBAR COM TEXTO BRANCO --- */
        
        /* 1. Container principal da toolbar */
        header[data-testid="stHeader"] {
            background-color: #111111 !important;
        }
        
        /* 2. TODO o texto na toolbar fica BRANCO */
        header[data-testid="stHeader"] * {
            color: #ffffff !important;
        }
        
        /* 3. Status de arquivo alterado */
        div[data-testid="stStatusWidget"] {
            color: #ffffff !important;
            font-weight: bold;
        }
        
        /* 4. Texto "File change." */
        .st-emotion-cache-1r4qj8v p,
        .st-emotion-cache-1r4qj8v span {
            color: #ffffff !important;
            background-color: transparent !important;
        }
        
        /* 5. Botão "Rerun" */
        button[kind="secondary"],
        .st-emotion-cache-1erivf3 {
            background-color: #00ff88 !important;
            color: #000000 !important !important; /* Texto preto no botão */
            border: none;
            border-radius: 5px;
            padding: 5px 15px;
            font-weight: bold;
        }
        
        button[kind="secondary"]:hover,
        .st-emotion-cache-1erivf3:hover {
            background-color: #00cc66 !important;
        }
        
        /* 6. Checkbox "Always rerun" */
        .stCheckbox label {
            color: #ffffff !important;
        }
        
        /* 7. Ícones na toolbar */
        header svg {
            fill: #ffffff !important;
        }
        
        /* 8. Override para garantir que tudo fique branco */
        .stApp > header,
        .stApp > header *,
        .stApp > header div,
        .stApp > header span,
        .stApp > header p {
            color: #ffffff !important;
        }
        
        /* 9. Se precisar de uma solução mais radical */
        .stApp > header {
            filter: invert(0) hue-rotate(0deg) brightness(1) !important;
        }
    </style>
""", unsafe_allow_html=True)


st.markdown("""
    <style>
        
        
        
        /* --- TÍTULOS --- */
        h1, h2, h3, h4, h5, h6 {
            color: #000000 !important; /* Preto */
            font-weight: bold;
        }
        
        
        
        
        /* --- TEXTOS DAS LABELS (antes dos inputs) --- */
        label {
            color: #000000 !important; /* Preto */
            font-weight: 600; /* ligeiramente mais forte para destacar */
        }
        
        /* --- INPUTS DE TEXTO --- */
        .stTextInput > div > div > input {
            background-color: rgba(0, 0, 0, 0);
            color: #ffffff !important; /* Texto do input preto */
            border: None;
            border-radius: 10px;
            padding: 10px;
        }
        
        .stTextInput > label {
            color: #000000 !important; /* Label do input preto */
            font-weight: bold;
        }
        
        /* --- BOTÕES --- */
        .stButton > button {
            background-color: #00ff88;
            color: #000000 !important; /* Texto do botão preto */
            border-radius: 10px;
            font-weight: bold;
            border: 2px solid #000000;
            padding: 10px 20px;
            margin-top: 10px;
        }
        
        .stButton > button:hover {
            background-color: #00cc66;
            transform: scale(1.02);
        }
        
        /* --- CHAT MESSAGES - PARTE CRÍTICA --- */
        /* Reset completo das mensagens do chat */
        .stChatMessage {
            color: #000000 !important;
        }
        
        /* Conteúdo das mensagens do chat */
        .stChatMessage div[data-testid="stChatMessageContent"] {
            color: #000000 !important;
            background-color: transparent !important;
        }
        
        /* Texto dentro das mensagens do chat */
        .stChatMessage p,
        .stChatMessage div,
        .stChatMessage span,
        .stChatMessage li,
        .stChatMessage ul,
        .stChatMessage ol {
            color: #000000 !important;
            font-size: 16px;
            line-height: 1.6;
        }
        
        /* --- CHAT INPUT --- */
        .stChatInput > div > div > textarea {
            color: #000000 !important;
            background-color: rgba(0, 0, 0, 0.05);
            border: 2px solid #00ff88;
            border-radius: 10px;
        }
        
        /* --- CONTAINERS DE MENSAGENS ESPECÍFICOS --- */
        /* Mensagens do assistente (respostas do chatbot) */
        div[data-testid="stChatMessage"][aria-label="Chat message from assistant"] {
            color: #000000 !important;
        }
        
        div[data-testid="stChatMessage"][aria-label="Chat message from assistant"] * {
            color: #000000 !important;
        }
        
        /* Mensagens do usuário */
        div[data-testid="stChatMessage"][aria-label="Chat message from user"] {
            color: #000000 !important;
        }
        
        div[data-testid="stChatMessage"][aria-label="Chat message from user"] * {
            color: #000000 !important;
        }
        
        /* --- MARKDOWN DENTRO DO CHAT --- */
        .stMarkdown {
            color: #000000 !important;
        }
        
        .stMarkdown p {
            color: #000000 !important;
        }
        
        .stMarkdown ul, .stMarkdown ol {
            color: #000000 !important;
        }
        
        .stMarkdown li {
            color: #000000 !important;
        }
        
        /* --- TEXTO EM NEGRITO E ITÁLICO --- */
        strong, b {
            color: #000000 !important;
            font-weight: bold;
        }
        
        em, i {
            color: #000000 !important;
            font-style: italic;
        }
        
        /* --- POSITION DO LOGO --- */
        .logo {
            position: absolute;
            top: 5px;
            right: 55px;
            width: 180px;
            opacity: 0.95;
        }
        
        /* --- SIDEBAR --- */
        section[data-testid="stSidebar"] {
            background-color: #111111;
        }
        
        /* Texto dentro da sidebar */
        section[data-testid="stSidebar"] * {
            color: #000000 !important; /* Branco para contraste na sidebar escura */
        }
        
        /* --- EXPANDER --- */
        section[data-testid="stSidebar"] details {
            border: 1px solid #00ff88;
            border-radius: 10px;
            padding: 5px;
            margin-bottom: 8px;
        }
        
        /* Texto dentro do expander */
        section[data-testid="stSidebar"] details * {
            color: #ffffff !important;
        }
        
        /* --- GARANTIR QUE NÃO HAJA TEXTO BRANCO --- */
        /* Override específico para qualquer texto branco */
        .stChatMessage *:not(.stMarkdown) {
            color: #000000 !important;
        }
        
        /* Garantia máxima para o conteúdo do chat */
        [class*="chat"], [class*="Chat"], [class*="message"], [class*="Message"] {
            color: #000000 !important;
        }
        
        [class*="chat"] *, [class*="Chat"] *, [class*="message"] *, [class*="Message"] * {
            color: #000000 !important;
        }
        
        /* --- BACKGROUND DO CHAT PARA CONTRASTE --- */
        /* Se quiser fundo claro para o chat */
        .stChatMessage {
            background-color: #f8f9fa !important; /* Cinza muito claro */
            padding: 10px;
            border-radius: 10px;
            margin: 5px 0;
        }
        
        /* Mensagens do assistente com fundo diferente */
        div[data-testid="stChatMessage"][aria-label="Chat message from assistant"] {
            background-color: #e9ecef !important; /* Cinza claro */
        }
        
        /* Mensagens do usuário com fundo diferente */
        div[data-testid="stChatMessage"][aria-label="Chat message from user"] {
            background-color: #d4edda !important; /* Verde muito claro */
        }
        
        /* --- SCROLLBAR PERSONALIZADA --- */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb {
            background: #00ff88;
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: #00cc66;
        }
        
        
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    /* 1. Estilizar a "caixa" da mensagem inteira */
    div[data-testid="stChatMessage"] {
        background-color: #00ff88 !important; /* Fundo preto puro */
        border-radius: 20px !important;       /* Cantos bem arredondados */
        padding: 1.5rem !important;           /* Espaço interno para não ficar colado */
        margin-bottom: 1rem !important;       /* Espaço entre mensagens */
        border: 1px solid #333333 !important; /* Opcional: borda subtil */
        box-shadow: 0 2px 5px rgba(0,0,0,0.2); /* Sombra leve para destacar */
    }

    /* 3. Ajustar o fundo do ícone para não ficar estranho */
    div[data-testid="stChatMessageAvatarContainer"] {
        background-color: transparent !important;
    }
    
    /* 4. (Opcional) Cor dos ícones SVGs se necessário */
    div[data-testid="stChatMessage"] svg {
        fill: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)



#*DEFINIR CAIXA DE MENSAGENS E PREDEFINIR O IDIOMA EM INGLES*

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "language" not in st.session_state:
    st.session_state["language"] = "en"  




#DESIGN DO LOGO DA IMS
logo_path = os.path.join(os.path.dirname(__file__), "unnamed-removebg-preview.png")

with open(logo_path, "rb") as f:
    logo_base64 = base64.b64encode(f.read()).decode()
st.markdown(
    f"""
    <img class="logo" src="data:image/png;base64,{logo_base64}" alt="NOVA IMS logo">
    """,
    unsafe_allow_html=True
)



#TÍTULO
st.set_page_config(page_title="AIms - Nova IMS Chatbot", page_icon="💬", layout= "centered")




#BOTÃO DE TROCAR DE LINGUA
with st.sidebar.expander("🌍 Choose the Chatbot Language / Escolher Idioma", expanded=False):
    language = st.radio(
        "Select the language / Selecionar Idioma:",
        ["English", "Português"]
    )




#TRADUÇÕES
#Definir textos que aparecem no chatbot, e a sua versão em português e inglês

if language == "English":
    st.session_state.language = "en"
    st.session_state.system_instruction = "You are a helpful assistant. You assist with academic queries, career guidance, and general support."
    texts = {
        "title": "AIms",
        "subtitle": "Nova IMS Virtual Assistant",
        "name": "Enter your name:",
        "number": "Enter your student number:",
        "question": "Write your question:",
        "submit": "Submit",
        "clear_chat": "🗑 Clear Chat",
        "clear_toast": "Chat successfully cleared!",
        "response": "Response:",
        "warning": "⚠ Write something before submitting.",
        "api_error": "❌ API Key not found! Set the GOOGLE_API_KEY variable.",
        "spinner": "Generating response...",
        "personality_title": "🤖 Choose the Bot Personality",
        "current_personality": "Current Bot Personality",
        "info_title": "🔍 More Information",
        "netpa": "[🔗 **NetPA**](https://netpa.novaims.unl.pt)",
        "email": "[📧 **Nova IMS Email**](https://outlook.office.com/mail/)",
        "password": "Enter your NetPA password:",
        "erro": "Waiting for user to enter a valid number and password..."
        
    }
else:
    st.session_state.language = "pt"
    st.session_state.system_instruction = "Você é um assistente acadêmico. Você ajuda com dúvidas acadêmicas, orientação de carreira e suporte geral."
    texts = {
        "title": "AIms",
        "subtitle": "Assistente Virtual da Nova IMS",
        "name": "Escreve o teu nome:",
        "number": "Escreve o teu número de aluno:",
        "question": "Escreve a tua pergunta:",
        "submit": "Enviar",
        "clear_chat": "🗑 Limpar Conversa",
        "clear_toast": "Conversa limpa com sucesso!",
        "response": "Resposta:",
        "warning": "⚠ Escreve algo antes de enviar.",
        "api_error": "❌ Chave da API não encontrada! Define a variável GOOGLE_API_KEY.",
        "spinner": "A gerar resposta...",
        "personality_title": "🤖 Escolhe a Personalidade do Bot",
        "current_personality": "Personalidade Atual do Bot",
        "info_title": "🔍 Mais Informações",
        "netpa": "[🔗 **NetPA**](https://netpa.novaims.unl.pt)",
        "email": "[📧 **Email Nova IMS**](https://outlook.office.com/mail/)",
        "password": "Escreve a tua password do NetPA:",
        "erro": "Aguardando usuário inserir um número e password válido..."
        
    }




#titulo
st.markdown("""
    <style>
        /* Importa a fonte do Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&display=swap');
        font-family: 'Playfair Display', serif;

        /* Aplica ao título */
        h1 {
            font-family: 'Poppins', sans-serif !important;
            color: #000000 !important;
            font-size: 3rem;
            font-weight: 700;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

st.title(texts['title'])
st.subheader(texts["subtitle"])



#Botão onde se vê os links necessários (netpa, email)
with st.sidebar.expander(texts['info_title'], expanded=False):
    st.markdown(texts['netpa'])
    st.markdown(texts['email'])




#BOTÃO PARA DEFINIR A PERSONALIDADE DO CHATBOT

with st.sidebar.expander(texts['personality_title'], expanded=False):
    system_instruction = st.selectbox(
        "Choose tha Bot's Personality:" if st.session_state.language == 'en' else 'Escolha a Personalidade do Bot:',
        ["Academic Advisor" if st.session_state.language == 'en' else 'Orientador Académico', "Career Coach" if st.session_state.language == 'en' else 'Orientador de Carreira', "Administrative Assistant" if st.session_state.language == 'en' else 'Assistente Administrativo', "Buddy Mode" if st.session_state.language == 'en' else 'Modo Amigo']
    )

    if system_instruction == "Academic Advisor" or system_instruction == 'Orientador Académico':
        st.session_state.system_instruction = (
            "You are an academic advisor at Nova IMS. You help students with courses, ECTS, and academic plans."
            if st.session_state.language == "en" else
            "Você é um assistente acadêmico. Você ajuda com cursos, ECTS e planos acadêmicos."
        )
    elif system_instruction == "Career Coach" or system_instruction == 'Orientador de Carreira':
        st.session_state.system_instruction = (
            "You are a career coach. You provide guidance on internships, LinkedIn, and professional development."
            if st.session_state.language == "en" else
            "Você é um coach de carreira. Você fornece orientações sobre estágios, LinkedIn e desenvolvimento profissional."
        )
    elif system_instruction == "Administrative Assistant" or system_instruction == 'Assistente Administrativo':
        st.session_state.system_instruction = (
            "You are an administrative assistant. You provide information on deadlines, fees, timetables, and rooms."
            if st.session_state.language == "en" else
            "Você é um assistente administrativo. Você fornece informações sobre prazos, taxas, horários e salas."
        )
    elif system_instruction == "Buddy Mode" or system_instruction == 'Modo Amigo':
        st.session_state.system_instruction = (
            "You are a friendly buddy. You chat informally, sharing tips and stories about student life at Nova IMS."
            if st.session_state.language == "en" else
            "Você é um amigo simpático. Você conversa de forma informal, compartilhando dicas e histórias sobre a vida estudantil na Nova IMS."
        )



# Botão para limpar o chat (fora do expander de histórico)
if st.sidebar.button(texts['clear_chat']):
    st.session_state["messages"] = []  
    st.session_state["user_input"] = ""  
    st.toast(texts['clear_toast'])




#VARIABLES
name = st.text_input(texts['name'])
number= st.text_input(texts['number'])
password = st.text_input(texts['password'], type="password")
if password=='1234':
    password=st.secrets['pass2']
elif password=='5678':
    password=st.secrets['pass1']



load_dotenv()

######################################## GEMINI API CONNECTION ####################################
api_key= st.secrets["GOOGLE_API_KEY"]
gemini_client=init_gemini_client()



######################################## MONGO DB CONECTION #######################################

mongo_client= init_connection_mongo()
if number and str(number) in dic.keys() and password == dic[str(number)]:
    collection = mongo_client["Projeto_curso"][str(number)]
else:
    collection = mongo_client["Projeto_curso"]["temp"]


embedding_model= load_embedding_model()



def mongdb(user_query:str):
    """
    Pesquisa informações especificas sobre notas, ECTS, coisas em especificas sobre a universidade presente na base de dados MongoDB
    Utiliza esta ferramenta sempre que o utilizador fizer perguntas sobre conteúdos especificos, regras ou dados.
    Quando a pergunta é referente a horários não utilzes esta tool.
    Deves usar esta tool caso a pergunta envolva algo como, pagamentos, propinas ou dividas.

    Args: 
        user_query (str): A pergunta do utilizador.
    """
    return retrieve_context(user_query, embedding_model, collection)



############################################### SCRAPPING TOOL ###############################################


def get_horario_atualizado_tool():
    """
    Acede ao site da faculdade (NetPA) em tempo real para consultar o horário pessoal do aluno.
    Usa esta ferramenta para responder a perguntas sobre:
    - Próximas aulas
    - Salas de aula
    - Horas de inicio e fim
    - Calendário académico
    ATENÇÂO: TODAS AS PERGUNTAS QUE ENVOLVEREM DAR OS DIAS DA SEMANA DEVES DÁ-LOS POR ORDEM.
    A ordem é a seguinte [Segunda-feira, Terça-feira, Quarta-feira, Quinta-feira, Sexta-feira] ou [Monday, Tuesday, Wednesday, Thursday, Friday]
    Segue sempre ista ordem para qualquer pergunta em que a resposta envolva mais do que um dia, esta informação deve ser prioritária à organizçaõ por hora
    """
    return scrape_horario(number, password)


########################################## LANGFUSE ################################################
langfuse_secret_key = st.secrets['langfuse_secret_key']
langfuse_public_key = st.secrets['langfuse_public_key']
langfuse_host = st.secrets['langfuse_host']

my_tools=[mongdb, get_horario_atualizado_tool]


#RESPONSE

if "messages" not in st.session_state:
    st.session_state["messages"]=[]
if not api_key:
    st.error(texts['api_error'])
else:
    client=init_gemini_client()
    model = "gemini-2.5-flash-lite"

    if name and number and password and str(number) in dic.keys() and password == dic[str(number)]:
        st.markdown(f"<div style='color:#000000; font-weight:bold; font-size:18px; margin:15px 0;'>"
            f"{'Hello' if st.session_state.language == 'en' else 'Olá'}, {name} 👋"
            f"</div>", 
            unsafe_allow_html=True)
        user_input = st.text_input(texts['question'], key="user_input")
        if st.button(texts['submit']):
            if user_input:
                with st.spinner(texts['spinner']):
                    try:
                        history_for_gemini=get_gemini_history()
                    
                        prompt_sistema = f"""
                        És um assistente da NOVA IMS. Tens acesso a ferramentas para consultar a documentação do projeto.
                        Usa a ferramenta 'retrieve_context' sempre que a pergunta exigir conhecimento específico sobre cursos, a universidade, notas, créditos, cadeiras, dividas, propinas e pagamentos.
                        Quando a pergunta é referente a horários utiliza a ferramenta 'get_horario_atualizado_tool'.
                        ATENÇÂO: Se não encontrares informação disponivel  em nenhuma das outras tools usa responde, mas apenas para perguntas relacionadas com universidade, mesmo que sejam outars funcionaliadades ou outras universidades.
                        ATENÇÂO: Para perguntas relacionadas com algo relacionada a universidade faz uma pesquisa detalhada.
                        Se a pergunta for genérica (ex: "Olá"), não uses a ferramenta.
                        Pergunta: {user_input}
                        Idioma da resposta: {language}
                        Contexto temporal: 
                        - Data e hora atual: {datetime.now().strftime("%A, %d/%m/%Y às %H:%M")}
                        - Usa esta informação para perguntas que precisem de contexto temporal como como "hoje", "amanhã", "esta semana" ou "já passou o prazo?".
                        ATENÇÂO: TODAS AS PERGUNTAS QUE ENVOLVEREM DAR OS DIAS DA SEMANA DEVES DÁ-LOS POR ORDEM.
                        A ordem é a seguinte [Segunda-feira, Terça-feira, Quarta-feira, Quinta-feira, Sexta-feira] ou [Monday, Tuesday, Wednesday, Thursday, Friday]
                        Segue sempre ista ordem para qualquer pergunta em que a resposta envolva mais do que um dia, esta informação deve ser prioritária à organizçaõ por hora.
                        ATENÇÂO: Quando a pergunta envolver ECTS feitos, deves responder com os ECTS que estão aprovados. Se a pergunta for ECTS inscritos deves responder todos os ECTS que a pessoa está inscrita.
                        """
                        system_intstructions_final= f"{st.session_state.system_instruction}\n\n---\n\n{prompt_sistema}"
                        
                        response_text = generate_response_with_tools_and_langfuse(
                            user_input=user_input,
                            model_name=model,
                            system_instr=system_intstructions_final,
                            user_name=name if name else "anonymous",
                            api_key=api_key,
                            chat_history=history_for_gemini,
                            my_tools=my_tools
                        )
                        st.session_state["messages"].append(
                            {"role": "user", "content": user_input}
                        )
                        st.session_state["messages"].append(
                            {"role": "assistant", "content": response_text}
                        )
                        st.write(response_text)
                        if langfuse_public_key:
                            with st.expander("🔍 Trace Info"):
                                st.success("✅ This interaction has been traced!")
                                st.info(f"View in [Langfuse Dashboard]({langfuse_host})")
                            
                    except Exception as e:
                        st.error(f"Error generating response: {e}")
            else:
                st.warning(texts['warning'])
    else:
        st.warning(texts['erro'])
st.markdown("---")
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.write(message["content"])