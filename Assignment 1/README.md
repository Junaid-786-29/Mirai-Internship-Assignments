# MirAI Internship Assignment 1
## The Identity Echo Interface

A simple Streamlit web application developed as part of the **MirAI School of Technology – Virtual Summer Internship 2026**.

## 📌 Objective

The application collects a user's name and message through a simple interface, validates the inputs, and displays an appropriate response based on the submitted data.

---

## ✨ Features

- User-friendly Streamlit interface
- Input field for user's name
- Input field for user's message
- "Transmit" button to submit data
- Input validation
  - Error if the name is empty
  - Warning if the message is empty
- Personalized success message using Python f-strings
- Bonus: Token Cost Estimator (approximate token usage based on message length)

---

## 🛠️ Technologies Used

- Python 3
- Streamlit

---

## 📂 Project Structure

```
Assignment 1/
│── app.py
│── requirements.txt
│── README.md
│── .gitignore
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Navigate to the project folder

```bash
cd <repository-folder>
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

---

## 📸 Preview

![alt text](dashboard.png)

---

## 📖 Learning Outcomes

Through this assignment, I learned:

- Creating a Streamlit application
- Using `st.title()` and `st.write()`
- Collecting user input with `st.text_input()`
- Creating buttons using `st.button()`
- Implementing conditional logic (`if`, `elif`, `else`)
- Displaying feedback using:
  - `st.error()`
  - `st.warning()`
  - `st.success()`
  - `st.info()`
- Using Python f-strings for formatted output
- Estimating token usage based on character count

---

## 📄 License

This project was created for educational purposes as part of the **MirAI School of Technology Virtual Summer Internship 2026**.