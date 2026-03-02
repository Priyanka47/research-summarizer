import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

#client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ── Page Config ──────────────────────────────────────────
st.set_page_config(
    page_title="AI Research Summarizer",
    page_icon="🔍",
    layout="wide"
)

# ── Initialize Session State ──────────────────────────────
# Streamlit reruns the whole script on every interaction
# so we use st.session_state to persist data between reruns
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
    st.session_state.research_topics = []
    st.session_state.messages_display = []  # for showing chat on screen
    initialize_needed = True
else:
    initialize_needed = False

# ── Agent Functions ───────────────────────────────────────
def initialize_agent():
    st.session_state.conversation_history.append({
        "role": "user",
        "parts": [{"text": """
            You are an expert AI research assistant with knowledge across all domains.

            Follow these rules in every response:

            1. If the user gives you a TOPIC TO RESEARCH (e.g. "machine learning",
               "climate change"), respond with a full structured summary using
               EXACTLY this format:

                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                📌 OVERVIEW
                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                3-4 sentences introducing the topic clearly.

                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                🔑 KEY POINTS
                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                Exactly 5 key insights, each 2-3 sentences long.
                • Point 1
                • Point 2
                • Point 3
                • Point 4
                • Point 5

                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                🌍 REAL WORLD APPLICATIONS
                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                3 concrete real-world examples with specific names or companies.

                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                📚 EXPLORE FURTHER
                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                3 subtopics to explore next, each with a one sentence explanation.

                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                💡 TL;DR
                ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                One powerful sentence capturing the essence of the topic.

            2. If the user asks a FOLLOW-UP QUESTION answer naturally and
               conversationally using the full conversation context.

            3. Always be clear, accurate, and beginner-friendly.
            4. Never forget anything said earlier in the conversation.
        """}]
    })
    st.session_state.conversation_history.append({
        "role": "model",
        "parts": [{"text": "Understood! I'm ready to research any topic or answer follow-up questions."}]
    })


def chat(user_message, client):
    st.session_state.conversation_history.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=st.session_state.conversation_history
    )

    assistant_reply = response.text

    st.session_state.conversation_history.append({
        "role": "model",
        "parts": [{"text": assistant_reply}]
    })

    # Track research topics
    if "OVERVIEW" in assistant_reply:
        st.session_state.research_topics.append(user_message)

    return assistant_reply


# ── Initialize on first load ──────────────────────────────
if initialize_needed:
    initialize_agent()

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.title("🔑 API Configuration")
    
    user_api_key = st.text_input(
        "Enter your Gemini API Key",
        type="password",        # hides the key like a password field
        placeholder="AIzaSy..."
    )
    
    st.caption("Get your free API key at [aistudio.google.com](https://aistudio.google.com)")
    st.divider()

    # Stop here if no API key provided
    if not user_api_key:
        st.warning("⚠️ Please enter your Gemini API key to get started.")
        st.stop()  # stops the rest of the app from rendering

    # Create client with user's key
    client = genai.Client(api_key=user_api_key)
 
    st.title("📊 Session Stats")
    st.metric("Messages Sent", len(st.session_state.messages_display))
    st.metric("Topics Researched", len(st.session_state.research_topics))

    if st.session_state.research_topics:
        st.subheader("📚 Topics Covered")
        for i, topic in enumerate(st.session_state.research_topics, 1):
            st.write(f"{i}. {topic}")

    if st.button("🗑️ Clear Conversation"):
        st.session_state.conversation_history = []
        st.session_state.research_topics = []
        st.session_state.messages_display = []
        initialize_agent()
        st.rerun()

# ── Main UI ───────────────────────────────────────────────
st.title("🔍 AI Research Summarizer")
st.caption("Type any topic to get a structured research summary. Ask follow-up questions naturally!")

# Display chat history
for message in st.session_state.messages_display:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input at the bottom
if user_input := st.chat_input("Enter a topic or ask a follow-up question..."):

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages_display.append({
        "role": "user",
        "content": user_input
    })

    # Get and show agent response
    with st.chat_message("assistant"):
        with st.spinner("Researching..."):
            result = chat(user_input, client)
        st.markdown(result)

    st.session_state.messages_display.append({
        "role": "assistant",
        "content": result
    })
