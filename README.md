# MirAI Internship Assignments

## MirAI School of Technology – Virtual Summer Internship 2026

This repository contains the assignments completed as part of the **MirAI School of Technology – Virtual Summer Internship 2026**. Each assignment focuses on building practical AI-powered applications using Python and Streamlit while learning prompt engineering, API integration, and modern UI development.

---

# 📁 Assignments

## Assignment 1 – The Identity Echo Interface

### 📌 Objective

Build a simple Streamlit application that collects a user's name and message, validates the inputs, and displays personalized feedback.

### ✨ Features

* User-friendly Streamlit interface
* Input field for user's name
* Input field for user's message
* **Transmit** button
* Input validation

  * Error if the name is empty
  * Warning if the message is empty
* Personalized success message using Python f-strings
* Bonus: Token Cost Estimator (approximate token usage based on message length)

### 📚 Learning Outcomes

* Creating a Streamlit application
* Using `st.title()` and `st.write()`
* Collecting user input with `st.text_input()`
* Creating buttons using `st.button()`
* Implementing conditional logic (`if`, `elif`, `else`)
* Displaying feedback using:

  * `st.error()`
  * `st.warning()`
  * `st.success()`
  * `st.info()`
* Using Python f-strings
* Estimating token usage

---

# Assignment 2 – Upgrading the AI Multiverse

### 📌 Objective

Upgrade a basic AI chatbot into a modern conversational web application by integrating AI personalities, prompt engineering, sidebar controls, and a chat-based interface.

### ✨ Features

* AI-powered chatbot built with **Streamlit**
* AI model integration using the **Groq API**
* Multiple AI personalities:

  * Friendly Teacher
  * Expert Hacker
  * Funny Friend
  * A Panicked College Student at 3 AM
  * A 1920s Mafia Boss
  * A Highly Sarcastic Fitness Coach
* Sidebar-based application settings
* Adjustable **Intensity Level (1–10)** to control personality behavior
* Prompt engineering using Python f-strings
* Modern chat interface using `st.chat_message()`
* Dynamic emoji avatars based on the selected personality
* Clean and interactive user interface

### 📚 Learning Outcomes

* Integrating an AI API into a Streamlit application
* Loading API keys securely using `.env`
* Prompt engineering
* Working with sidebar components
* Using `st.sidebar.selectbox()`
* Using `st.sidebar.slider()`
* Using `st.chat_message()` for chat interfaces
* Applying Python control flow (`if`, `elif`, `else`)
* Creating dynamic UI elements
* Building interactive AI-powered applications

---

# 🛠️ Technologies Used

* Python 3
* Streamlit
* Groq API
* python-dotenv

---

# 📂 Project Structure

```text
Assignments/
│
├── Assignment 1/
│   ├── app.py
│   ├── requirements.txt
│   ├── README.md
│   └── .gitignore
│
├── Assignment 2/
│   ├── app.py
│   ├── requirements.txt
│   ├── README.md
│   ├── .env (not included)
│   └── .gitignore
│
├── screenshots/
│   └── dashboard.png
│
└── README.md

```

---

# 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Junaid-786-29/Mirai-Internship-Assignments.git
```

### 2. Navigate to the project

```bash
cd Mirai-Internship-Assignments
```

### 3. Install the required packages

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

```env
GROQ_API_KEY=your_api_key_here
```

### 5. Run the application

```bash
streamlit run app.py
```

---

# 📸 Preview

### Assignment 1

![alt text](screenshots/image.png)

### Assignment 2

![alt text](screenshots/image-1.png)

---

# 🎯 Skills Demonstrated

* Python Programming
* Streamlit Development
* AI API Integration
* Prompt Engineering
* Environment Variable Management
* User Interface Design
* Chatbot Development
* Conditional Logic
* Python f-strings
* Dynamic User Interfaces

---

# 📄 License

This repository was created for educational purposes as part of the **MirAI School of Technology – Virtual Summer Internship 2026**.
