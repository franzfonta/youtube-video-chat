# TODO choose only one logging library
import logging
from icecream import ic
import sys
import os

from dependency_injector import containers, providers
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
from helpers import is_valid_url

from mock_openai_client import MockOpenaiClient
from youtube_assistant import YouTubeAssistant
from youtube_transcript_fetcher import YouTubeTranscriptFetcher

load_dotenv()
logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize the assistant
if 'assistant' not in st.session_state:

    # initialize OpenAI client
    api_key = os.getenv('OPENAI_API_KEY')
    # TODO move implementation choice to a dependency injector
    # client = OpenAI(api_key=api_key)
    client = MockOpenaiClient()

    # TODO convert to function
    transcript_fetcher = YouTubeTranscriptFetcher()

    # Retrieve or create the Assistant TODO
    st.session_state.assistant = YouTubeAssistant(client, transcript_fetcher)

# Set title and description
st.title('YouTube Smart Assistant')
st.write('Ask me something about a YouTube video and I will answer you!')

# The URL of the YouTube video the user is interested in
video_url = st.text_input("Enter the URL")

# True when the user pushes the Ask button
wanna_chat = st.button("Chat about this video")
if wanna_chat:
    if is_valid_url(video_url):
        st.session_state.assistant.start_new_thread(video_url)
    else:
        st.error("Please enter a valid YouTube URL")

# Display question and answers in two columns
col1, col2 = st.columns(2)

# The question the user wants to ask
with col1:
    user_question = st.text_input(f"Your question")
    send_message = st.button("💬")

# The answer from the assistant
with col2:
    if wanna_chat and send_message:
        with st.spinner():
            response = st.session_state.assistant.ask_question(user_question)
            st.write(response)

