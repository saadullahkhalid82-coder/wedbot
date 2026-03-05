from typing import Dict, Any
import streamlit as st
from supabase import create_client, Client


SUPABASE_URL: str = "https://agglgrfstvugdzoqyepv.supabase.co"
SUPABASE_ANON_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFnZ2xncmZzdHZ1Z2R6b3F5ZXB2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAxNzgyNjQsImV4cCI6MjA4NTc1NDI2NH0.Ss85AqU6w8oSdRwANXoi1X5e5uKYZ8IVjeLXkdeOFIk"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def login_page() -> None:
    st.title("Authentication")

    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    with tab1:
        st.subheader("User Login")

        email: str = st.text_input("Email", key="login_email")
        password: str = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button("Login"):
            if not email or not password:
                st.warning("Please enter email and password.")
                return

            try:
                with st.spinner("Authenticating..."):
                    response: Any = supabase.auth.sign_in_with_password(
                        {
                            "email": email,
                            "password": password,
                        }
                    )

                if not response.session:
                    st.error("Invalid login response.")
                    return

                token: str = response.session.access_token

                st.session_state["token"] = token
                st.session_state["authenticated"] = True
                st.session_state["user"] = response.user.email

                st.success("Login successful.")
                st.rerun()

            except Exception as exc:
                st.error(f"Login failed: {exc}")

    with tab2:
        st.subheader("Create Account")

        signup_email: str = st.text_input(
            "Email",
            key="signup_email"
        )

        signup_password: str = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        confirm_password: str = st.text_input(
            "Confirm Password",
            type="password",
            key="signup_confirm_password"
        )

        if st.button("Create Account"):
            if not signup_email or not signup_password:
                st.warning("Please fill all fields.")
                return

            if signup_password != confirm_password:
                st.warning("Passwords do not match.")
                return

            try:
                with st.spinner("Creating account..."):
                    response: Dict[str, Any] = supabase.auth.sign_up(
                        {
                            "email": signup_email,
                            "password": signup_password
                        }
                    )

                if response.user is None:
                    st.error("Signup failed.")
                    return

                st.success(
                    "Account created successfully. Please login."
                )

            except Exception as exc:
                st.error(f"Signup failed: {exc}")