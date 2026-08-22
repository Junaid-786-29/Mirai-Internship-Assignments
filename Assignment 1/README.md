# 📟 THE IDENTITY ECHO INTERFACE - Assignment 1


```text
┌──────────────────────────────────────────────────────────────────────────────┐
│  SESSION ID : MIRAI-ASSIGNMENT-01              BUILD  : v1.0.0-RELEASE       │
│  AUTHOR     : Junaid Khan                      HOST   : localhost:8501       │
│  RUNTIME    : Python 3.8+ / Streamlit          STATUS : [ ONLINE / ACTIVE ]  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 💻 SYSTEM INFO

```text
       /\_/\          user@mirai-workstation:~/Assignment-1
      ( o.o )         -------------------------------------
       > ^ <          PROJECT   : The Identity Echo Interface
                      TRACK     : MirAI Virtual Summer Internship 2026
                      MODULE    : Streamlit UI & Interactive State
                      CORE      : app.py
                      STATUS    : READY_FOR_TRANSMISSION
                      PORT      : 8501 (Default HTTP)
```

---

## ⚡ $ man identity-echo

### 01. SYNOPSIS

```bash
$ identity-echo --name "<USER_NAME>" --message "<TRANSMISSION_PAYLOAD>"
```

**The Identity Echo Interface** is a responsive Streamlit web application designed to capture user credentials (Name) and payload data (Message), validate input integrity via real-time alerting triggers, and render a personalized confirmation echo.

---

### 02. CORE CAPABILITIES

```text
[✓] INTERACTIVE STREAMLIT GUI ───── Clean user input interface via web runtime
[✓] DUAL-STAGE VALIDATION ──────── Conditional logic filter before submission
[✓] DYNAMIC STATUS ALERTS ──────── Visual feedback stream (Error / Warning / Success)
[✓] PERSONALIZED ECHO RENDER ───── Python formatted string transmission dispatch
```

---

### 03. LOGIC & VALIDATION PIPELINE

```text
                       ┌─────────────────────────┐
                       │  User Clicks Transmit   │
                       └────────────┬────────────┘
                                    │
                                    ▼
                      /───────────────────────────\
                     <   Is 'Name' field empty?    >
                      \───────────────────────────/
                               /         \
                       YES    /           \   NO
                             ▼             ▼
                 ┌─────────────────┐  /───────────────────────────\
                 │ st.error(...)   │ <  Is 'Message' field empty?  >
                 │ "Provide name." │  \───────────────────────────/
                 └─────────────────┘           /         \
                                       YES    /           \   NO
                                             ▼             ▼
                                 ┌──────────────────┐  ┌───────────────────┐
                                 │ st.warning(...)  │  │ st.success(...)   │
                                 │ "Type a message."│  │ Personalized echo │
                                 └──────────────────┘  └───────────────────┘
```

#### Validation Matrix

| Priority | Condition | UI Alert Method | Output Message |
| :--- | :--- | :--- | :--- |
| `01` | `not user_name` | `st.error()` | 🚨 *Please provide your name.* |
| `02` | `not user_message` | `st.warning()` | ⚠️ *Please type a message to transmit* |
| `03` | `else` *(Valid)* | `st.success()` | ✅ *Transmission successful! Greetings, {user_name}. We received your message: {user_message}* |

---

### 04. EXECUTION & SETUP GUIDE

```bash
# [Step 1] Navigate to Assignment 1 directory
cd "Assignment 1"

# [Step 2] Initialize and activate virtual environment
# Windows (PowerShell):
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# [Step 3] Install package dependencies
pip install -r requirements.txt

# [Step 4] Launch the Streamlit application
streamlit run app.py
```

```text
  You can now view your Streamlit app in your browser.

  Local URL:    http://localhost:8501
  Network URL:  http://192.168.x.x:8501
```

---

### 05. DIRECTORY STRUCTURE

```text
Assignment 1/
├── 📄 app.py              # Main Streamlit application logic & controls
├── 📄 requirements.txt    # Project dependencies (streamlit, etc.)
├── 📄 .gitignore          # Git exclusion rules (venv/, __pycache__/)
└── 📄 README.md           # Terminal style project documentation
```

---

### 06. SYSTEM SOURCE OVERVIEW


```python
import streamlit as st

st.title("The Identity Echo Interface")

st.write("Enter your name and a message, then click Transmit.")

user_name = st.text_input("Name")

user_message = st.text_input("Message")

if st.button("Transmit"):

    if not user_name:
        st.error("Please provide your name.")
    elif not user_message:
        st.warning("Please type a message to transmit")
    else:
        st.success(f"Transmission successful! Greetings, {user_name}. We received your message: {user_message}")
```

---

### 07. TELEMETRY & LEARNING OUTCOMES

```text
[OK] st.title()        : Webpage heading setup
[OK] st.write()        : User prompt & instruction rendering
[OK] st.text_input()   : Capturing string variables (`user_name`, `user_message`)
[OK] st.button()       : Event listener & submission trigger
[OK] if / elif / else  : Branching control validation flow
[OK] st.error/warning  : Conditional alerting system
[OK] st.success()      : String interpolation & transmission feedback
```

```text
────────────────────────────────────────────────────────────────────────────────
[ TRANSMISSION PROTOCOL COMPLETE — MIRAI SCHOOL OF TECHNOLOGY SUMMER 2026 ]
────────────────────────────────────────────────────────────────────────────────
```
