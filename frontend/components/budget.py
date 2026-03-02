from typing import Any
import streamlit as st
from api import create_budget, export_budget


def budget_ui(create: bool = False) -> None:
    token = st.session_state.get("token")

    if not token:
        st.error("Session expired. Please login again.")
        st.session_state.clear()
        st.rerun()

    st.header("Budget Management")

    st.subheader("Create Budget Breakdown")

    total_budget: float = st.number_input(
        "Enter Total Budget",
        min_value=0.0,
        step=1000.0,
    )

    if st.button("Create Budget"):
        try:
            with st.spinner("Creating budget breakdown..."):
                response: Any = create_budget(token, total_budget)

            st.success("Budget breakdown created successfully.")

        except Exception as exc:
            st.error(f"Failed to create budget: {exc}")

    st.subheader("Export Budget PDF")

    if st.button("Export Budget"):
        try:
            with st.spinner("Generating budget PDF..."):
                pdf_bytes: bytes = export_budget(token)

            st.success("Budget ready for download.")

            st.download_button(
                label="Download Budget PDF",
                data=pdf_bytes,
                file_name="budget.pdf",
                mime="application/pdf",
            )

        except Exception as exc:
            st.error(f"Failed to export budget: {exc}")