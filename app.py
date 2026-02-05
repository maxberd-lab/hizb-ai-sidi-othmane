import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="Hizb Sidi Othmane AI", 
    page_icon="🇲🇦", 
    layout="centered"
)

# --- STYLE PERSONNALISÉ (Optionnel pour faire "Pro") ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; border: none; }
    </style>
    """, unsafe_allow_request_usage=True)

st.title("🤖 Assistant Digital - Sidi Othmane")
st.subheader("Programme Électoral & Citoyenneté")

# --- 1. GESTION DE LA CLÉ API ---
# On vérifie d'abord les Secrets Streamlit, sinon on demande une saisie manuelle
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = st.sidebar.text_input("Clé API Groq (Optionnel si Secrets configurés)", type="password")

if not api_key:
    st.info("💡 En attente de la configuration de la clé API...")
    st.stop()

# --- 2. CHARGEMENT DES DONNÉES DE CONNAISSANCE ---
try:
    with open("data.txt", "r", encoding="utf-8") as f:
        connaissances_locales = f.read()
except FileNotFoundError:
    st.error("❌ Erreur : Le fichier 'data.txt' est introuvable sur votre GitHub.")
    st.stop()

# --- 3. INITIALISATION DU MODÈLE ET DE L'HISTORIQUE ---
# Utilisation de Llama 3.3 70B (Modèle actuel le plus performant sur Groq)
llm = ChatGroq(
    temperature=0.3, 
    groq_api_key=api_key, 
    model_name="llama-3.3-70b-versatile"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages de la discussion
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. INTERACTION UTILISATEUR ---
if prompt := st.chat_input("Posez votre question sur Sidi Othmane..."):
    # Ajouter le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Préparation du message système (Instructions)
    instruction_politique = f"""
    Tu es l'expert digital du parti pour l'arrondissement de Sidi Othmane. 
    Tes réponses doivent être basées EXCLUSIVEMENT sur ces informations : {connaissances_locales}.
    Si l'utilisateur pose une question hors sujet, réponds poliment que tu es là pour parler du programme local.
    Réponds en Darija si l'utilisateur t'écrit en Darija. Sois encourageant et patriotique.
    """

    # Génération de la réponse
    with st.chat_message("assistant"):
        try:
            with st.spinner("Réflexion en cours..."):
                full_prompt = [
                    SystemMessage(content=instruction_politique),
                    HumanMessage(content=prompt)
                ]
                response = llm.invoke(full_prompt)
                full_response = response.content
                st.markdown(full_response)
                
                # Sauvegarder la réponse dans l'historique
                st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Désolé, une erreur technique est survenue : {e}")