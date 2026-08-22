# 🧠 THE MEMORY VAULT (STATEFUL CHATBOT) - Assignment 3

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│  SESSION ID : MIRAI-ASSIGNMENT-03              BUILD  : v3.0.0-RELEASE       │
│  ENGINE     : Groq Cloud API (Llama 3.3 70B)   HOST   : localhost:8501       │
│  STATE TYPE : Stateful (st.session_state)      STATUS : [ ONLINE / ACTIVE ]  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 SYSTEM INFO

```text
       /\_/\          user@mirai-workstation:~/Assignment-3
      ( o.o )         -------------------------------------
       > ^ <          PROJECT   : The Memory Vault (Stateful Chatbot)
                      TRACK     : MirAI Virtual Summer Internship 2026
                      MODULE    : Streamlit Session State & Multi-Turn Chat
                      MODEL     : llama-3.3-70b-versatile (Groq)
                      CORE      : app.py
                      STATUS    : PERSISTENT_MEMORY_READY
                      PORT      : 8501 (Default HTTP)
```

---

## ⚡ $ man memory-vault

### 01. SYNOPSIS

```bash
$ memory-vault --personality "<SELECT_PERSONA>" --intensity <1-10> --persist-state true
```

**The Memory Vault** upgrades the conversational assistant from a stateless single-turn system into a full stateful chat application. Powered by **Groq Cloud API (Llama 3.3 70B)** and Streamlit's native `st.session_state`, it persists multi-turn dialogue history across full-page reruns, dynamic sidebar personality updates, and intensity adjustments.

---

### 02. CORE CAPABILITIES

```text
[✓] PERSISTENT SESSION MEMORY ──── Message buffer retention via st.session_state
[✓] NATIVE STREAMLIT CHAT UI ───── Modern input experience with st.chat_input()
[✓] MULTI-TURN RE-RENDERING ────── Preserves message bubbles across script reruns
[✓] ADAPTIVE PERSONALITY ENGINE ── 6 behavioral profiles with live avatar switching
[✓] INTENSITY SPECTRUM (1-10) ──── Dynamic prompt injection controlling role immersion
[✓] SECURE GROQ CLOUD PIPELINE ─── Environment-isolated API keys via python-dotenv
```

---

### 03. PERSONALITY MATRIX & AVATAR MAPPING

| Persona Identifier | Avatar | Behavioral Role |
| :--- | :---: | :--- |
| **Friendly Teacher** | 📚 | Encouraging mentor offering step-by-step guidance |
| **Expert Hacker** | 💻 | Terminal-savvy cypherpunk offering direct technical answers |
| **Funny Friend** | 😂 | Lighthearted comedic pal delivering witty banter |
| **A Panicked College Student at 3 AM** | 😰 | Overwhelmed, sleepless student battling looming deadlines |
| **A 1920s Mafia Boss** | 🕴️ | Vintage mobster demeanor with underworld authority |
| **A Highly Sarcastic Fitness Coach** | 🏋️ | Relentless roaster serving aggressive tough love |

---

### 04. STATE LIFECYCLE & MEMORY PIPELINE

```text
               ┌──────────────────────────────────────────────┐
               │         Browser Session Initialized          │
               └──────────────────────┬───────────────────────┘
                                      │
                                      ▼
                      /───────────────────────────────\
                     <   'messages' in session_state?  >
                      \───────────────────────────────/
                                /           \
                        NO     /             \   YES
                              ▼               ▼
                 ┌──────────────────┐  ┌──────────────────────────────┐
                 │ Initialize Buffer│  │ Load Prior History Buffer    │
                 │ messages = []    │  │ [ {role, content, avatar} ]  │
                 └────────────┬─────┘  └──────────────┬───────────────┘
                              │                       │
                              └───────────┬───────────┘
                                          ▼
                      ┌───────────────────────────────────────┐
                      │ Render All Past Chat Bubbles to Screen│
                      │ (st.chat_message for user & assistant)│
                      └───────────────────┬───────────────────┘
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │ Listen for User Prompt via            │
                      │ st.chat_input("Ask me anything...")   │
                      └───────────────────┬───────────────────┘
                                          │
                                          ▼
                      ┌───────────────────────────────────────┐
                      │ 1. Append User Message to State       │
                      │ 2. Synthesize Persona System Prompt   │
                      │ 3. Dispatch to Groq (Llama 3.3 70B)   │
                      │ 4. Append AI Response to State        │
                      │ 5. Render Streamlit Chat Message      │
                      └───────────────────────────────────────┘
```

---

### 05. EXECUTION & SETUP GUIDE

```bash
# [Step 1] Navigate to Assignment 3 directory
cd "Assignment 3"

# [Step 2] Initialize and activate virtual environment
# Windows (PowerShell):
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# [Step 3] Configure Environment Secrets
# Create a .env file with your Groq API Key:
echo GROQ_API_KEY="your_groq_api_key_here" > .env

# [Step 4] Install package dependencies
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

### 06. DIRECTORY STRUCTURE

```text
Assignment 3/
├── 📄 .env                # Private API key configuration (GROQ_API_KEY)
├── 📄 .gitignore          # Excludes .env, venv/, and cache files
├── 📄 app.py              # Stateful Streamlit application logic & session state
├── 📄 requirements.txt    # Project dependencies (streamlit, groq, python-dotenv)
└── 📄 README.md           # Terminal style project documentation
```

---

### 07. SYSTEM SOURCE OVERVIEW

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

### 08. TELEMETRY & LEARNING OUTCOMES

```text
[OK] st.session_state       : Retaining multi-turn conversation memory across reruns
[OK] Groq API SDK           : Streaming and querying llama-3.3-70b-versatile
[OK] Prompt Engineering     : Ingesting persona definitions + dynamic intensity
[OK] st.chat_message()      : Preserving and rendering message containers
[OK] State Management       : Preventing message loss during sidebar setting changes
[OK] Environment Security   : Isolating credentials using python-dotenv
```

```text
────────────────────────────────────────────────────────────────────────────────
[ MEMORY VAULT PROTOCOL COMPLETE — MIRAI SCHOOL OF TECHNOLOGY SUMMER 2026 ]
────────────────────────────────────────────────────────────────────────────────
```
