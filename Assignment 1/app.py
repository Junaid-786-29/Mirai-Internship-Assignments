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