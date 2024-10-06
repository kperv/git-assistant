import streamlit as st
from rag import GitAssistant


st.title("💬 Git Assistant")
st.caption("🚀 Pro-Git enhanced with AI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "How to commit changes in a file?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="👨‍💻").write(prompt)
    response = GitAssistant().response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant", avatar="🤖").write(msg)
