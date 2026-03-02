from typing import Any, Dict, List
import streamlit as st
from api import export_checklist, get_tasks, mark_complete


def tasks_ui(generate: bool = False) -> None:
    token = st.session_state.get("token")

    if not token:
        st.session_state.clear()
        st.rerun()

    if generate:
        st.header("Export Checklist")

        if st.button("Export Checklist"):
            try:
                with st.spinner("Fetching checklist..."):
                    pdf_bytes: bytes = export_checklist(token)

                st.download_button(
                    label="Download Checklist PDF",
                    data=pdf_bytes,
                    file_name="checklist.pdf",
                    mime="application/pdf",
                )

            except Exception as exc:
                st.error(f"Failed to export checklist: {exc}")

    
    else:
        st.header("Your Tasks")

        if st.button("Refresh Tasks"):
            try:
                with st.spinner("Fetching tasks..."):
                    response: Any = get_tasks(token)

                if isinstance(response, list):
                    tasks: List[Dict[str, Any]] = response
                else:
                    tasks = response.get("tasks", [])

                if not tasks:
                    st.info("No tasks found.")
                    return

                for task in tasks:
                    st.write(task.get("title"))
                    col1, col2 = st.columns([4, 1])

                with col1:
                    if task.get("completed"):
                        st.markdown(f"~~{task.get('title')}~~ ✅")
                    else:
                        st.write(task.get("title"))

                with col2:
                    if not task.get("completed"):
                        if st.button(
                            "Mark Complete",
                            key=f"complete_{task['id']}"
                        ):
                            mark_complete(token, task["title"])
                            st.rerun()

            except Exception as exc:
                st.error(f"Failed to fetch tasks: {exc}")