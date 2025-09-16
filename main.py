import streamlit as st
import wikipedia
import streamlit_authenticator as stauth

# --------------------------
# HASHED PASSWORDS
# --------------------------
hashed_passwords = stauth.Hasher(["admin123", "user123"]).generate()
credentials = {
    "usernames": {
        "admin": {
            "name": "Administrator",
            "password": hashed_passwords[0]   # Correct: get the first hashed password string
        },
        "bhavya": {
            "name": "Bhavya",
            "password": hashed_passwords[1]   # Correct: second hashed password string
        }
    }
}


# --------------------------
# AUTHENTICATOR
# --------------------------
authenticator = stauth.Authenticate(
    credentials,
    "threat_app",   # cookie name
    "abcdef",       # key
    cookie_expiry_days=1
)
# --------------------------
# LOGIN PAGE TITLE
# --------------------------
st.image("img.jpg", width=100)
st.title("Sentinel-Auth")

# --------------------------
# LOGIN FORM
# --------------------------
name, authentication_status, username = authenticator.login(fields={"form_name": "Login"}, location="main")

if authentication_status:
    st.sidebar.success(f"✅ Welcome {name}")
    authenticator.logout("Logout", "sidebar")
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
            # NOTE: Use results not results!
            summary = wikipedia.summary(results, sentences=2, auto_suggest=False, redirect=True)
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
elif authentication_status == False:
    st.error("❌ Username/password is incorrect")
elif authentication_status == None:
    st.warning("ℹ️ Please enter your username and password")
