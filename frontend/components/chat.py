import streamlit as st
from api import chat


def chat_ui() -> None:
    token = st.session_state.get("token")

    if not token:
        st.session_state.clear()
        st.rerun()

    st.header("AI Assistant")

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Display previous messages
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            with st.chat_message("user"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(msg["content"])

    user_input = st.chat_input("Type your message...")

    if user_input:
        
        st.session_state["chat_history"].append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            with st.spinner("Thinking..."):
                response = chat(token, user_input)

            reply = response.get("reply", "")

            st.session_state["chat_history"].append(
                {"role": "assistant", "content": reply}
            )

            with st.chat_message("assistant"):
                st.markdown(reply)

        except Exception as exc:
            st.error(str(exc))