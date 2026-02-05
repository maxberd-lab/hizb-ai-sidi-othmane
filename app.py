import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

st.set_page_config(page_title="AI Sidi Othmane", page_icon="🇲🇦")

# --- TITRE ET STYLE ---
st.title("🤖 Assistant Hizb - Sidi Othmane")

# Lecture de tes connaissances
with open("data.txt", "r", encoding="utf-8") as f:
    context = f.read()

# Configuration de la clé API (Tu peux la cacher dans les secrets de Streamlit plus tard)
api_key = st.sidebar.text_input("Entrez votre clé Groq API", type="password")

if api_key:
    llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name="llama3-8b-8192")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)
        
        # Le prompt qui force l'IA à utiliser tes données
        system_prompt = f"Tu es l'assistant officiel du parti à Sidi Othmane. Utilise ces infos pour répondre exclusivement : {context}"
        
        response = llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=prompt)
        ])
        
        msg_content = response.content
        st.session_state.messages.append({"role": "assistant", "content": msg_content})
        st.chat_message("assistant").write(msg_content)
else:
    st.info("Veuillez entrer votre clé API Groq pour commencer. (Gratuit sur console.groq.com)")