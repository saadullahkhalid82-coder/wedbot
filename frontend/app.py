import streamlit as st
from auth import login_page
from dashboard import dashboard


def main() -> None:
    st.set_page_config(
        page_title="AI Planner",
        layout="wide",
    )

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        dashboard()
    else:
        login_page()


if __name__ == "__main__":
    main()