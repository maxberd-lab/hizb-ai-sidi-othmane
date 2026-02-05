import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="AI Sidi Othmane", page_icon="🇲🇦")

st.title("🤖 Assistant Digital - Sidi Othmane")

# --- 1. GESTION DE LA CLÉ API ---
if "GROQ_API_KEY" in st.secrets:
    api_key = st.secrets["GROQ_API_KEY"]
else:
    api_key = st.sidebar.text_input("Clé API Groq", type="password")

if not api_key:
    st.info("💡 Veuillez configurer la clé API dans les Secrets Streamlit.")
    st.stop()

# --- 2. CHARGEMENT DES DONNÉES ---
try:
    with open("data.txt", "r", encoding="utf-8") as f:
        context = f.read()
except FileNotFoundError:
    st.error("Fichier data.txt introuvable.")
    st.stop()

# --- 3. INITIALISATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des anciens messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 4. INTERACTION ---
if prompt := st.chat_input("Votre question..."):
    # Affichage message utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Appel Groq avec le nouveau modèle
    try:
        llm = ChatGroq(
            temperature=0, 
            groq_api_key=api_key, 
            model_name="llama-3.3-70b-versatile"
        )
        
        system_instructions = f"Tu es l'assistant du parti à Sidi Othmane. Utilise ces infos : {context}"
        
        with st.chat_message("assistant"):
            response = llm.invoke([
                SystemMessage(content=system_instructions),
                HumanMessage(content=prompt)
            ])
            full_response = response.content
            st.markdown(full_response)
            
            # Sauvegarder dans l'historique
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
    except Exception as e:
        st.error(f"Erreur : {e}")