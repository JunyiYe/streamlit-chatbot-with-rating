import streamlit as st
import random
import time
from datetime import datetime
import pandas as pd
from streamlit_star_rating import st_star_rating


# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)


st.title("Simple chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("How can I assit you?"):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    chat_df = pd.DataFrame([{"timestamp": current_time, "role": "user", "content": prompt}])
    chat_df.to_csv("chat_history.csv", index=False, mode="a")  # Append mode


    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator())

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    stars = st_star_rating("Please rate you experience", maxValue=5, defaultValue=3, key="rating")
    print(stars)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat_df = pd.DataFrame([{"timestamp": current_time, "role": "assistant", "content": response, "rating": stars}])
    chat_df.to_csv("chat_history.csv", index=False, mode="a")  # Append mode

