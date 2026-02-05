import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

st.set_page_config(page_title="AI Sidi Othmane", page_icon="🇲🇦")
st.title("🤖 Assistant Hizb - Sidi Othmane")

# 1. Vérification sécurisée de la clé API
if "GROQ_API_KEY" not in st.secrets:
    st.error("⚠️ La clé 'GROQ_API_KEY' manque dans vos Secrets Streamlit.")
    st.stop()

api_key = st.secrets["GROQ_API_KEY"]

# 2. Chargement propre des connaissances
try:
    with open("data.txt", "r", encoding="utf-8") as f:
        context = f.read()
except Exception:
    context = "Infos indisponibles pour le moment."

# 3. Initialisation de l'historique
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage des messages passés
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# 4. Traitement du message utilisateur
if prompt := st.chat_input("Dites 'Bonjour' pour commencer..."):
    # On affiche immédiatement le message de l'utilisateur
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    try:
        # Initialisation précise du modèle pour éviter les erreurs de requête
        llm = ChatGroq(
            temperature=0.2, 
            groq_api_key=api_key, 
            model_name="llama3-8b-8192"
        )
        
        # On s'assure que le contenu n'est pas vide
        if prompt.strip():
            system_instructions = f"Tu es l'assistant officiel de Sidi Othmane. Réponds en te basant sur ceci : {context}"
            
            with st.spinner("L'IA réfléchit..."):
                response = llm.invoke([
                    SystemMessage(content=system_instructions),
                    HumanMessage(content=prompt)
                ])
                
                # Sauvegarde et affichage de la réponse
                answer = response.content
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.chat_message("assistant").write(answer)
        
    except Exception as e:
        # Affichage clair de l'erreur pour le débogage
        st.error(f"Erreur technique Groq : {str(e)}")