import streamlit as st
import uuid
import time


from rag import GitAssistant
from db import (
    save_conversation,
    save_feedback,
    get_feedback_stats,
)

def print_log(message):
    print(message, flush=True)



st.title("💬 Git Assistant")
st.caption("🚀 Ask AI assistant with knowledge of Pro Git Book")
st.link_button("Pro Git Book", "https://git-scm.com/book/en/v2")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Let me help you with git! What is your question?"}
    ]
    # Session state initialization
    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
        print_log(
            f"New conversation started with ID: {st.session_state.conversation_id}"
        )
    if "count" not in st.session_state:
        st.session_state.count = 0
        print_log("Feedback count initialized to 0")

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user", avatar="👨‍💻").write(prompt)
    
    start_time = time.time()
    response = GitAssistant().response(prompt)
    end_time = time.time()

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant", avatar="🤖").write(response)

    save_conversation(
        st.session_state.conversation_id, prompt, response
    )


    st.session_state.conversation_id = str(uuid.uuid4())

    # Feedback buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("+1"):
            st.session_state.count += 1
            print_log(
                f"Positive feedback received. New count: {st.session_state.count}"
            )
            save_feedback(st.session_state.conversation_id, 1)
            print_log("Positive feedback saved to database")
    with col2:
        if st.button("-1"):
            st.session_state.count -= 1
            print_log(
                f"Negative feedback received. New count: {st.session_state.count}"
            )
            save_feedback(st.session_state.conversation_id, -1)
            print_log("Negative feedback saved to database")

    st.write(f"Current count: {st.session_state.count}")

    # Display feedback stats
    feedback_stats = get_feedback_stats()
    st.subheader("Feedback Statistics")
    st.write(f"Thumbs up: {feedback_stats['thumbs_up']}")
    st.write(f"Thumbs down: {feedback_stats['thumbs_down']}")