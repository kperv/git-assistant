import streamlit as st

# with st.sidebar:

st.title("💬 Git Assistant")
st.caption("🚀 Pro-Git enhanced with AI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How to commit changes in a file?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)