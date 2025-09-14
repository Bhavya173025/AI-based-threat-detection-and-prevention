import streamlit as st
import wikipedia
import streamlit_authenticator as stauth

# --------------------------
# USER CREDENTIALS (hashed passwords)
# --------------------------
credentials = {
    "usernames": {
        "admin": {
            "name": "Administrator",
            # hash for "admin123"
            "password": "$2b$12$gA.0RhPaK0jvNhbbFoj7XOi7NUjN8IkYz3XzMmwFhtdl10EZw0rEy",
            "role": "admin"
        },
        "bhavya": {
            "name": "Bhavya",
            # hash for "user123"
            "password": "$2b$12$sBj86ZqT6CM3KrHmkWAwKe/xMfRhCA7A5FKsoMRsYyPLAVBbk8AxC",
            "role": "user"
        }
    }
}

# Create authenticator
authenticator = stauth.Authenticate(
    credentials,
    "threat_app",   # Cookie name
    "abcdef",       # Key for cookie
    cookie_expiry_days=1
)

# --------------------------
# LOGIN (rendered in sidebar)
# --------------------------
name, authentication_status, username = authenticator.login("Login", location=st.sidebar)

if authentication_status:
    role = credentials["usernames"][username]["role"]

    st.sidebar.success(f"Welcome {name} ({role})")
    authenticator.logout("Logout", "sidebar")

    # --------------------------
    # COMMON FEATURE: Chatbot
    # --------------------------
    st.title("📚 Wikipedia Chatbot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    def get_wikipedia_summary(query):
        try:
            results = wikipedia.search(query)
            if not results:
                return "Sorry, I couldn't find anything on that topic."
            summary = wikipedia.summary(
                results[0], sentences=2, auto_suggest=False, redirect=True
            )
            return summary
        except wikipedia.DisambiguationError as e:
            return f"Your query is ambiguous, did you mean: {', '.join(e.options[:5])}?"
        except wikipedia.PageError:
            return "Sorry, I couldn't find a page matching your query."
        except Exception:
            return "Oops, something went wrong."

    # User input
    user_input = st.text_input("Ask me anything:")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        bot_response = get_wikipedia_summary(user_input)
        st.session_state.messages.append({"role": "bot", "content": bot_response})

    # Display chat history
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f"**You:** {msg['content']}")
        else:
            st.markdown(f"**Bot:** {msg['content']}")

    # --------------------------
    # EXTRA: Admin-only Section
    # --------------------------
    if role == "admin":
        st.markdown("---")
        st.subheader("🔐 Admin Panel")
        st.info("Here you can add features like viewing logs, managing users, etc.")

elif authentication_status is False:
    st.error("❌ Username/password is incorrect")

elif authentication_status is None:
    st.warning("Please enter your username and password")
