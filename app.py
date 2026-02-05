import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# Récupération automatique de la clé depuis les "Secrets"
api_key = st.secrets["GROQ_API_KEY"]

st.set_page_config(page_title="AI Sidi Othmane", page_icon="🇲🇦")
st.title("🤖 Assistant Hizb - Sidi Othmane")

with open("data.txt", "r", encoding="utf-8") as f:
    context = f.read()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Posez votre question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    
    llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name="llama3-8b-8192")
    
    system_prompt = f"Tu es l'assistant officiel du parti à Sidi Othmane. Réponds en utilisant ces infos : {context}"
    
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt)
    ])
    
    st.session_state.messages.append({"role": "assistant", "content": response.content})
    st.chat_message("assistant").write(response.content)