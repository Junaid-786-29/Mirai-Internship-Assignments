# 🤖 AI MULTIVERSE BUILDER CHATBOT - Assignment 2

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│  SESSION ID : MIRAI-ASSIGNMENT-02              BUILD  : v2.0.0-RELEASE       │
│  ENGINE     : Groq Cloud API (Llama 3.3 70B)   HOST   : localhost:8501       │
│  RUNTIME    : Python 3.8+ / Streamlit          STATUS : [ ONLINE / ACTIVE ]  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 SYSTEM INFO

```text
       /\_/\          user@mirai-workstation:~/Assignment-2
      ( o.o )         -------------------------------------
       > ^ <          PROJECT   : AI Multiverse Builder Chatbot
                      TRACK     : MirAI Virtual Summer Internship 2026
                      MODULE    : LLM Integration & Prompt Engineering
                      MODEL     : llama-3.3-70b-versatile (Groq)
                      CORE      : app.py
                      STATUS    : READY_FOR_INFERENCE
                      PORT      : 8501 (Default HTTP)
```

---

## ⚡ $ man ai-multiverse

### 01. SYNOPSIS

```bash
$ ai-multiverse --personality "<SELECT_PERSONA>" --intensity <1-10> --prompt "<QUERY>"
```

**AI Multiverse Builder Chatbot** is a dynamic conversational web application powered by **Groq Cloud API** and **Llama 3.3 70B Versatile**. It features modular AI personalities, intensity level scaling, and real-time avatar customization rendered using Streamlit's native chat components.

---

### 02. CORE CAPABILITIES

```text
[✓] GROQ LLM ACCELERATION ──────── High-speed inference with llama-3.3-70b-versatile
[✓] 6 DIVERSE PERSONAS ─────────── Selectable behavioral profiles with custom avatars
[✓] DYNAMIC INTENSITY TUNING ───── 10-level persona commitment dial (Subtle -> Maximum)
[✓] REAL-TIME PROMPT SYNTHESIS ─── Contextual system instruction injection per request
[✓] STREAMLIT CHAT UI ──────────── Native st.chat_message rendering with user/bot avatars
[✓] SECURE SECRETS MANAGEMENT ──── Environment isolation via python-dotenv (.env)
```

---

### 03. PERSONALITY MATRIX & AVATAR MAPPING

| Persona Identifier | Avatar | Behavioral Description |
| :--- | :---: | :--- |
| **Friendly Teacher** | 📚 | Patient, encouraging, pedagogical explanations |
| **Expert Hacker** | 💻 | Cypherpunk tone, terminal jargon, direct & technical |
| **Funny Friend** | 😂 | Casual, witty, humorous commentary and banter |
| **A Panicked College Student at 3 AM** | 😰 | High anxiety, caffeine-fueled panic, deadline dread |
| **A 1920s Mafia Boss** | 🕴️ | Vintage noir slang, commanding, underworld demeanor |
| **A Highly Sarcastic Fitness Coach** | 🏋️ | Brutally honest workout roasts, intense tough love |

---

### 04. INTENSITY SPECTRUM LOGIC

```text
  [1 ─────── 3]                    [4 ──────── 7]                   [8 ──────── 10]
  SUBTLE / MILD                   BALANCED / CORE                  MAXIMUM COMMIT
┌───────────────────────────────┐┌───────────────────────────────┐┌───────────────────────────────┐
│ Subtle stylistic undertones; ││ Clearly defined character;    ││ Total immersion; extreme      │
│ primarily factual responses.  ││ natural persona vernacular.   ││ expressions & role commitment.│
└───────────────────────────────┘└───────────────────────────────┘└───────────────────────────────┘
```

---

### 05. ARCHITECTURE & PIPELINE

```text
  ┌───────────────────────┐       ┌────────────────────────┐
  │ Sidebar: Personality  │       │ Sidebar: Intensity 1-10│
  └───────────┬───────────┘       └───────────┬────────────┘
              │                               │
              ▼                               ▼
       [ Select Avatar ]             [ Set Intensity ]
              │                               │
              └───────────────┬───────────────┘
                              ▼
        ┌───────────────────────────────────────────┐
        │        User Submits Input Prompt          │
        └─────────────────────┬─────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────────┐
        │ Dynamic Prompt Synthesis (System Payload) │
        │ - Role definition ({personality})         │
        │ - Intensity instructions ({intensity})    │
        │ - Strict 'Never break character' guard    │
        │ - User message payload                    │
        └─────────────────────┬─────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────────┐
        │  Groq API Client (llama-3.3-70b-versatile)│
        └─────────────────────┬─────────────────────┘
                              │
                              ▼
        ┌───────────────────────────────────────────┐
        │ Streamlit Chat Interface                  │
        │  ├─ st.chat_message("user")               │
        │  └─ st.chat_message("assistant", avatar)  │
        └───────────────────────────────────────────┘
```

---

### 06. EXECUTION & SETUP GUIDE

```bash
# [Step 1] Navigate to Assignment 2 directory
cd "Assignment 2"

# [Step 2] Initialize and activate virtual environment
# Windows (PowerShell):
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# [Step 3] Configure Environment Variables (.env)
# Create a .env file with your Groq API Key:
echo GROQ_API_KEY="your_groq_api_key_here" > .env

# [Step 4] Install dependencies
pip install -r requirements.txt

# [Step 5] Launch application
streamlit run app.py
```

```text
  You can now view your Streamlit app in your browser.

  Local URL:    http://localhost:8501
  Network URL:  http://192.168.x.x:8501
```

---

### 07. DIRECTORY STRUCTURE

```text
Assignment 2/
├── 📄 .env                # Private API key configuration (GROQ_API_KEY)
├── 📄 .gitignore          # Excludes .env, venv/, and bytecode cache
├── 📄 app.py              # Core Streamlit app & Groq LLM integration
├── 📄 requirements.txt    # Project dependencies (streamlit, groq, python-dotenv)
└── 📄 README.md           # Terminal style project documentation
```

---

### 08. SYSTEM SOURCE OVERVIEW

```python
import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

st.title("🤖 AI Builder Chatbot")
st.write("Welcome! Choose a personality from the sidebar and start chatting.")

st.sidebar.title("App Settings")
personality = st.sidebar.selectbox(
    "Choose Personality",
    [
        "Friendly Teacher",
        "Expert Hacker",
        "Funny Friend",
        "A Panicked College Student at 3 AM",
        "A 1920s Mafia Boss",
        "A Highly Sarcastic Fitness Coach"
    ]
)

intensity = st.sidebar.slider("Intensity Level", min_value=1, max_value=10, value=5)
user_input = st.text_input("Enter your message", placeholder="Ask me anything...")

if st.button("SEND"):
    if user_input.strip():
        ai_instructions = f"""
        You are acting as {personality}.
        Your personality intensity is {intensity} out of 10.
        If the intensity is low (1-3), act subtly.
        If it is medium (4-7), clearly stay in character.
        If it is high (8-10), fully commit to the personality in every response.
        Never break character.
        User Message:
        {user_input}
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": ai_instructions}]
        )

        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant", avatar=bot_avatar):
            st.write(response.choices[0].message.content)
    else:
        st.warning("Please enter a message.")
```

---

### 09. TELEMETRY & LEARNING OUTCOMES

```text
[OK] Groq API SDK           : Connecting & authenticating LLM requests
[OK] Llama-3.3-70B Model    : High-speed conversational inference
[OK] Prompt Engineering     : Dynamic system instructions with conditional rules
[OK] st.sidebar Controls    : Modular selectbox and intensity slider bindings
[OK] st.chat_message()      : Conversation flow rendering with custom avatars
[OK] Security Best Practice : Secure token handling via python-dotenv
```

```text
────────────────────────────────────────────────────────────────────────────────
[ MULTIVERSE PROTOCOL READY — MIRAI SCHOOL OF TECHNOLOGY SUMMER 2026 ]
────────────────────────────────────────────────────────────────────────────────
```
