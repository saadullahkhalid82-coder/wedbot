import streamlit as st
from components.chat import chat_ui
from components.tasks import tasks_ui
from components.budget import budget_ui
from components.profile import profile_ui
from components.history import history_ui


def dashboard() -> None:
    st.sidebar.title("Dashboard")

    menu = st.sidebar.radio(
        "Navigation",
        [
            "AI Chat",
            "Generate Checklist",
            "View Tasks",
            "Create Budget",
            "View Budgets",
            "Profile",
            "Conversation History",
            "Logout",
        ],
    )

    if menu == "AI Chat":
        chat_ui()

    elif menu == "Generate Checklist":
        tasks_ui(generate=True)

    elif menu == "View Tasks":
        tasks_ui(generate=False)

    elif menu == "Create Budget":
        budget_ui(create=True)

    elif menu == "View Budgets":
        budget_ui(create=False)

    elif menu == "Profile":
        profile_ui()

    elif menu == "Conversation History":
        history_ui()

    elif menu == "Logout":
        st.session_state.clear()
        st.rerun()