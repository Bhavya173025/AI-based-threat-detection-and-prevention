import streamlit as st
import wikipedia
import streamlit_authenticator as stauth

# --------------------------
# USER CREDENTIALS (hashed passwords, required in >=0.3.1)
# --------------------------
# To generate new hashes:
#   import streamlit_authenticator as stauth
#   stauth.Hasher(["admin123", "user123"]).generate()
credentials = {
    "usernames": {
        "admin": {
            "email": "admin@example.com",  # required
            "name": "Administrator",
            "password": "$2b$12$gA.0RhPaK0jvNhbbFoj7XOi7NUjN8IkYz3XzMmwFhtdl10EZw0rEy",  # hash for admin123
            "role": "admin"
        },
        "bhavya": {
            "email": "bhavya@example.com",  # required
            "name": "Bhavya",
            "password": "$2b$12$sBj86ZqT6CM3KrHmkWAwKe/xMfRhCA7A5FKsoMRsYyPLAVBbk8AxC",  # hash for user123
            "role": "user"
        }
    }
}

# --------------------------
# AUTHENTICATOR
# --------------------------
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name="threat_app",  # Cookie name
    key="abcdef",              # Key for encryption
    cookie_expiry_days=1
)

# --------------------------
# LOGIN FORM
# --------------------------
name, authentication_status, username = authenticator.login("Login", location="sidebar")

if authentication_status:
    role = credentials["usernames"][username]["role"]

    st.sidebar.success(f"✅ Welcome {name} ({role})")
    authenticator.logout("Logout", location="sidebar")

    # --------------------------
    # MAIN FEATURE: Wikipedia Chatbot
    # --------------------------
    st.title("📚 Wikipedia Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    def get_wikipedia_summary(query):
        try:
            results = wikipedia.search(query)
            if not results:
                return "Sorry, I couldn't find anything on that topic."
            summary = wikipedia.summary(results[0], sentences=2, auto_suggest=False, redirect=True)
            return summary
        except wikipedia.DisambiguationError as e:
            return f"Your query is ambiguous, did you mean: {', '.join(e.options[:5])}?"
        except wikipedia.PageError:
            return "Sorry, I couldn't find a page matching your query."
        except Exception:
            return "Oops, something went wrong."

    user_input = st.text_input("Ask me anything:")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        bot_response = get_wikipedia_summary(user_input)
        st.session_state.messages.append({"role": "bot", "content": bot_response})

    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Bot:** {msg['content']}")

    # --------------------------
    # ADMIN PANEL (only visible for admin role)
    # --------------------------
    if role == "admin":
        st.markdown("---")
        st.subheader("🔐 Admin Panel")
        st.info("Admin-only area: logs, user management, retrain model, etc.")

elif authentication_status is False:
    st.error("❌ Username/password is incorrect")

elif authentication_status is None:
    st.warning("ℹ️ Please enter your username and password")
