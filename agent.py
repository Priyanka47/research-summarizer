from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Stores full conversation — questions AND answers
conversation_history = []
research_topics = []


def initialize_agent():
    """Set up the agent's personality and instructions at the start."""
    conversation_history.append({
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

            2. If the user asks a FOLLOW-UP QUESTION about something already 
               discussed (e.g. "explain key point 3", "tell me more about that", 
               "how does this relate to healthcare"), answer naturally and 
               conversationally using the full conversation context.

            3. Always be clear, accurate, and beginner-friendly.
            4. Never forget anything said earlier in the conversation.
        """}]
    })
    conversation_history.append({
        "role": "model",
        "parts": [{"text": "Understood! I'm your AI research assistant. Give me any topic to research, or ask me follow-up questions about anything we've discussed. I'll remember our entire conversation!"}]
    })


def chat(user_message):
    """Send a message and get a response, maintaining full conversation history."""
    
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    # Send ENTIRE conversation history to the model
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation_history
    )

    assistant_reply = response.text

    # Add agent's reply to history
    conversation_history.append({
        "role": "model",
        "parts": [{"text": assistant_reply}]
    })

    return assistant_reply


def show_history():
    """Show stats about the current session."""
    # Filter only real user messages (skip the system prompt)
    user_messages = [
        m for m in conversation_history
        if m["role"] == "user"
    ][1:]  # Skip the first one (system prompt)

    if not user_messages:
        print("\n📭 No topics researched yet in this session.\n")
    else:
        print(f"\n📋 Session Stats:")
        print(f"   Messages sent: {len(user_messages)}")
        print(f"   Topics explored: {len(research_topics)}")
        if research_topics:
            print(f"\n Topics covered:")
            for i, topic in enumerate(research_topics,1):
                print(f"  {i}. {topic}")
        print()


def main():
    print("\n🔍 AI Research Summarizer Agent")
    print("=" * 40)
    print("Commands:")
    print("  • Type any topic to research it")
    print("  • Ask follow-up questions naturally!")
    print("  • Type 'history' to see session stats")
    print("  • Type 'clear' to start a fresh session")
    print("  • Type 'quit' to exit")
    print("=" * 40)

    # Initialize the agent with its instructions
    initialize_agent()

    while True:
        user_input = input("\n💬 You: ").strip()

        if not user_input:
            print("⚠️  Please enter a topic or question.")
            continue

        if user_input.lower() == "quit":
            print("\n👋 Goodbye! Happy researching!\n")
            break

        elif user_input.lower() == "history":
            show_history()

        elif user_input.lower() == "clear":
            conversation_history.clear()
            initialize_agent()  # Re-initialize with instructions
            print("\n🗑️  Conversation cleared! Starting fresh.\n")

        else:
            print(f"\n⏳ Thinking...\n")
            result = chat(user_input)
            print(f"🤖 Agent: {result}")
            
            # If response contains OVERVIEW it was a research topic
            if "OVERVIEW" in result:
                research_topics.append(user_input)


if __name__ == "__main__":
    main()