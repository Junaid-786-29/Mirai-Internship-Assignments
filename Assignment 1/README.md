# Assignment 1 – The Identity Echo Interface

> **MirAI School of Technology – Virtual Summer Internship 2026**

## 📌 Overview

**The Identity Echo Interface** is a Streamlit web application designed to collect user input (Name and Message), validate the entries with visual status alerts, and generate a personalized echo/transmission confirmation message.

---

## ✨ Features

- **Interactive Streamlit UI**: Simple interface with input fields and visual indicators.
- **Input Fields**:
  - Name input (`st.text_input`)
  - Message input (`st.text_input`)
  - Transmit button (`st.button`)
- **Input Validation & Dynamic Alerts**:
  - 🚨 **Error (`st.error`)**: Displayed if the name field is empty.
  - ⚠️ **Warning (`st.warning`)**: Displayed if the message field is empty.
  - ✅ **Success (`st.success`)**: Displays a personalized response using Python f-strings upon valid input.

---

## 🛠️ Tech Stack & Requirements

- **Language**: Python 3.8+
- **Framework**: [Streamlit](https://streamlit.io/)
- **Dependencies**: Detailed in [requirements.txt](file:///c:/Users/Junaid%20Khan/Desktop/Mirai%20Internship%20Assignments/Assignment%201/requirements.txt)

---

## 🚀 Installation & Running

### 1. Navigate to the Assignment 1 Directory

```bash
cd "Assignment 1"
```

### 2. Set Up a Virtual Environment (Recommended)

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application

```bash
streamlit run app.py
```

Once executed, Streamlit will launch the application in your default web browser (typically at `http://localhost:8501`).

---

## 📁 File Structure

```text
Assignment 1/
├── app.py              # Main Streamlit application logic
├── requirements.txt    # Required Python packages
├── .gitignore          # Ignored files (virtual environments, cache)
└── README.md           # Documentation for Assignment 1
```

---

## 📚 Learning Outcomes

- Initializing a Streamlit project and configuring app title (`st.title`).
- Capturing user inputs using `st.text_input`.
- Processing form submission triggers with `st.button`.
- Utilizing control flow logic (`if`, `elif`, `else`) for input validation.
- Presenting user feedback using `st.error`, `st.warning`, and `st.success`.
