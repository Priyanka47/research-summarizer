# 🔍 AI Research Summarizer Agent

An AI-powered research assistant that generates structured, comprehensive summaries on any topic. Built with Python, Google Gemini API, and Streamlit.

## 🌟 Features

- **Instant Research Summaries** — Get structured summaries on any topic in seconds
- **Conversation Memory** — Ask follow-up questions and the agent remembers full context
- **Structured Output** — Every summary includes Overview, Key Points, Real World Applications, Further Reading and TL;DR
- **Session History** — Track all topics researched in current session
- **Secure** — Users provide their own Gemini API key, no keys stored server-side
- **Clean UI** — Chat-style interface built with Streamlit

## 🎥 Demo

> Type any topic → Get a structured research summary → Ask follow-up questions naturally

![Demo](demo.gif)

## 🛠️ Tech Stack

- **Python 3.11+**
- **Google Gemini API** (gemini-2.5-flash)
- **Streamlit** — Web UI
- **python-dotenv** — Environment variable management

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or higher
- A free Gemini API key from [aistudio.google.com](https://aistudio.google.com)

### Installation

1. Clone the repository
```bash
git clone https://github.com/Priyanka47/research-summarizer.git
cd research-summarizer
```

2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Run the app
```bash
streamlit run app.py
```

5. Enter your Gemini API key in the sidebar and start researching!

## 💡 How to Use

1. Get a free API key from [aistudio.google.com](https://aistudio.google.com)
2. Enter your API key in the sidebar
3. Type any topic in the chat box
4. Get a full structured research summary
5. Ask follow-up questions naturally — the agent remembers context!

## 📁 Project Structure
```
research-summarizer/
├── app.py              # Main Streamlit app with UI and agent logic
├── agent.py            # Standalone agent logic (terminal version)
├── requirements.txt    # Python dependencies
└── .gitignore          # Files excluded from version control
```

## 🧠 Key Concepts Used

- **LLM API Integration** — Connecting to Google Gemini API
- **Conversation Memory** — Managing message history for context
- **Prompt Engineering** — Structured prompts for consistent output
- **Context Window Management** — Passing full history on every request
- **Streamlit Session State** — Persisting data across app reruns

## 🔮 Future Improvements

- [ ] Export summaries as PDF
- [ ] Support multiple AI providers (OpenAI, Anthropic)
- [ ] Save research history across sessions
- [ ] Add web search for real-time information
- [ ] Support for multiple languages

## 👨‍💻 Author

**Priyanka Kumari**
- GitHub: [@Priyanka47](https://github.com/Priyanka47)
- LinkedIn: [priyankaa47](https://www.linkedin.com/in/priyankaa47/)


