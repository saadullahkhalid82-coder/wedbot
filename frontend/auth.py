import streamlit as st
from supabase import create_client, Client


SUPABASE_URL: str = "https://agglgrfstvugdzoqyepv.supabase.co"
SUPABASE_ANON_KEY: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFnZ2xncmZzdHZ1Z2R6b3F5ZXB2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAxNzgyNjQsImV4cCI6MjA4NTc1NDI2NH0.Ss85AqU6w8oSdRwANXoi1X5e5uKYZ8IVjeLXkdeOFIk"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)


def login_page() -> None:
    st.title("User Login")

    email: str = st.text_input("Email")
    password: str = st.text_input("Password", type="password")

    if st.button("Login"):
        if not email or not password:
            st.warning("Please enter email and password.")
            return

        try:
            with st.spinner("Authenticating..."):
                response = supabase.auth.sign_in_with_password(
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