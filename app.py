import streamlit as st

from rag import GitAssistant


assistant = GitAssistant()


st.title("💬 Git Assistant")
st.caption("🚀 Ask AI assistant with knowledge of Pro Git Book")
st.link_button("Pro Git Book", "https://git-scm.com/book/en/v2")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Let me help you with git! What is your question?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="👨‍💻").write(prompt)
    answer = assistant.answer(prompt)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.chat_message("assistant", avatar="🤖").write(answer)
