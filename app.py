import logging
import sys
import os

from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

from youtube_assistant import YouTubeAssistant

load_dotenv()
logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# initialize openai
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# Initialize the assistant
if 'assistant' not in st.session_state:
    # Retrieve or create the Assistant TODO
    # st.session_state.assistant = YouTubeAssistant(client)
    st.session_state.assistant = None

# Set title and description
st.title('YouTube Smart Assistant')
st.write('Ask me something about a YouTube video and I will answer you!')

# The URL of the YouTube video the user is interested in
# TODO validate URL
video_url = st.text_input("Enter the URL")
# True when the user pushes the Ask button
wanna_chat = st.button("Chat about this video")
if wanna_chat:
    st.session_state.assistant.start_new_thread(video_url)

# Display question and answers in two columns
col1, col2 = st.columns(2)

# The question the user wants to ask
with col1:
    user_question = st.text_input(f"Your question")
    send_message = st.button("💬")

# The answer from the assistant
with col2:
    if video_url and wanna_chat and user_question:
        with st.spinner():
            response = st.session_state.assistant.ask_question(user_question)
            st.write(response)
