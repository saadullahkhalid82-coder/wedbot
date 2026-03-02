from typing import Any, Dict
import streamlit as st
from api import update_profile, get_profile


def profile_ui() -> None:
    token = st.session_state.get("token")

    if not token:
        st.session_state.clear()
        st.rerun()

    st.header("Profile")

    try:
        with st.spinner("Loading profile..."):
            profile: Dict[str, Any] = get_profile(token)
    except Exception as exc:
        st.error(f"Failed to load profile: {exc}")
        return

    st.text_input("Email", value=profile.get("email", ""), disabled=True)

    name: str = st.text_input("Name", value=profile.get("name", ""))
    phone: str = st.text_input("Phone", value=profile.get("phone", ""))
    city: str = st.text_input("City", value=profile.get("city", ""))

    if st.button("Update Profile"):
        try:
            with st.spinner("Updating profile..."):
                update_profile(
                    token,
                    {
                        "name": name,
                        "phone": phone,
                        "city": city,
                    },
                )

            st.success("Profile updated successfully.")
            st.rerun()

        except Exception as exc:
            st.error(f"Failed to update profile: {exc}")