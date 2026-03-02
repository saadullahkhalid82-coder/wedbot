from typing import Any, Dict, List
import streamlit as st
from api import get_conversation


def history_ui() -> None:
    token = st.session_state.get("token")

    if not token:
        st.error("Session expired. Please login again.")
        st.session_state.clear()
        st.rerun()

    st.header("Conversation History")

    if st.button("Load Conversation"):
        try:
            with st.spinner("Fetching conversation..."):
                response: Dict[str, Any] = get_conversation(token)

            messages: List[Dict[str, Any]] = response.get("messages", [])

            if not messages:
                st.info("No conversation history found.")
                return

            for msg in messages:
                role: str = msg.get("role", "unknown")
                content: str = msg.get("content", "")

                if role == "user":
                    st.markdown(f"**You:** {content}")
                else:
                    st.markdown(f"**Assistant:** {content}")

        except Exception as exc:
            if "Session expired" in str(exc):
                st.session_state.clear()
                st.rerun()
            else:
                st.error(f"Failed to load conversation: {exc}")