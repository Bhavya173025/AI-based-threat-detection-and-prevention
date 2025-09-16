import streamlit as st
import wikipedia
import streamlit_authenticator as stauth
import requests

# Debug: Show loaded secrets for verification (remove in production)
st.write("Secrets loaded:", st.secrets)

# --------------------------
# HASHED PASSWORDS
# --------------------------
hashed_passwords = stauth.Hasher(["admin123", "user123"]).generate()
credentials = {
    "usernames": {
        "admin": {"name": "Administrator", "password": hashed_passwords[0]},
        "bhavya": {"name": "Bhavya", "password": hashed_passwords[1]},
    }
}

# --------------------------
# AUTHENTICATOR
# --------------------------
authenticator = stauth.Authenticate(
    credentials,
    "threat_app",
    "abcdef",
    cookie_expiry_days=1
)

# --------------------------
# LOGIN PAGE TITLE
# --------------------------
st.title("Sentinel-Auth")

# --------------------------
# LOGIN FORM
# --------------------------
name, authentication_status, username = authenticator.login(fields={"form_name": "Login"}, location="main")

if authentication_status:
    st.sidebar.success(f"✅ Welcome {name}")
    authenticator.logout("Logout", "sidebar")

    section = st.sidebar.radio("Select Section", ["Wikipedia Chatbot", "Security Tools"])

    if section == "Wikipedia Chatbot":
        st.title("📚 Wikipedia Chatbot")

        if "messages" not in st.session_state:
            st.session_state.messages = []

        def get_wikipedia_summary(query):
            try:
                results = wikipedia.search(query)
                if not results:
                    return "Sorry, I couldn't find anything on that topic."
                summary = wikipedia.summary(results[0],
