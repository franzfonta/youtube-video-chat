import logging
import os
import sys

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from helpers import is_valid_url
from mock_openai_client import MockOpenaiClient
from youtube_assistant import YouTubeAssistant
from youtube_thread import YouTubeThread
from youtube_transcript_fetcher import YouTubeTranscriptFetcher

load_dotenv()
logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize the assistant
if 'assistant' not in st.session_state:

    # Initialize the OpenAI client. Use the mock client when developing.
    environment = os.getenv('ENVIRONMENT')
    api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI(
        api_key=api_key) if environment == "prod" else MockOpenaiClient()

    transcript_fetcher = YouTubeTranscriptFetcher()

    st.session_state.assistant = YouTubeAssistant(client, transcript_fetcher)

# Initialize threads
if 'threads' not in st.session_state:
    st.session_state.threads: list[YouTubeThread] = []

# Set title and description
st.title('YouTube Smart Assistant')
st.write('Ask me something about a YouTube video and I will answer you!')

# Display the sidebar with the form to start a new conversation and the previous conversations
with st.sidebar:

    # Display the form to fetch a transcript and start a new conversation
    with st.form(key='my_form'):

        st.markdown('## Let\'s start a new conversation!')

        # The URL of the YouTube video the user is interested in
        video_url = st.text_input("YouTube video link")

        # True when the user pushes the Ask button
        if st.form_submit_button("Analyze it!"):
            if is_valid_url(video_url):
                st.session_state.current_thread = st.session_state.assistant.create_thread(
                    video_url)
                st.session_state.threads.append(
                    st.session_state.current_thread)
            else:
                st.error("Please enter a valid YouTube URL")

    # Display the video thumbnail and a button to select the thread for all previous conversations
    for thread in st.session_state.threads:
        def callback(thread): return st.session_state.__setitem__(
            "current_thread", thread)
        # TODO refactor this
        st.image(f"https://img.youtube.com/vi/{thread.video_url.split('v=')[1]}/maxresdefault.jpg")
        st.button(
            f"Thread {thread.openai_thread.id}",
            on_click=lambda thread=thread: callback(thread),
            type="primary" if thread == st.session_state.current_thread else "secondary"
        )
        st.divider()

# Display chat messages from history
if "current_thread" in st.session_state:
    for message in st.session_state.current_thread.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input
if prompt := st.chat_input(f"Your question..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner():
            if not "current_thread" in st.session_state:
                st.markdown("Please select a YouTube video.")
            elif st.session_state.current_thread.transcript is None:
                st.warning("Please select a YouTube video.")
            else:
                if response := st.session_state.assistant.ask_question(st.session_state.current_thread, prompt):
                    st.markdown(response)
                else:
                    st.error("Something went wrong. Please try again.")

