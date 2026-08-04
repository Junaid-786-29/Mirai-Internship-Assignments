import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

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

if personality == "Friendly Teacher":
    bot_avatar = "📚"

elif personality == "Expert Hacker":
    bot_avatar = "💻"

elif personality == "Funny Friend":
    bot_avatar = "😂"

elif personality == "A Panicked College Student at 3 AM":
    bot_avatar = "😰"

elif personality == "A 1920s Mafia Boss":
    bot_avatar = "🕴️"

elif personality == "A Highly Sarcastic Fitness Coach":
    bot_avatar = "🏋️"

else:
    bot_avatar = "🤖"

intensity = st.sidebar.slider(
    "Intensity Level",
    min_value=1,
    max_value=10,
    value=5
)

user_input = st.text_input(
    "Enter your message",
    placeholder="Ask me anything..."
)

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
        messages=[
            {
                "role": "user",
                "content": ai_instructions
            }
        ]
    )
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant",avatar=bot_avatar):
            st.write(response.choices[0].message.content)
    else:
        st.warning("Please enter a message.")