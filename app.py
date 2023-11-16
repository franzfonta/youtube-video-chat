# TODO choose only one logging library
import logging
import os
import sys

import streamlit as st
from dependency_injector import containers, providers
from dotenv import load_dotenv
from icecream import ic
from openai import OpenAI

from helpers import is_valid_url
from mock_openai_client import MockOpenaiClient
from thread import Thread
from youtube_assistant import YouTubeAssistant
from youtube_transcript_fetcher import YouTubeTranscriptFetcher

# TODO introduce dependency injection

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

    # TODO inject dependency
    transcript_fetcher = YouTubeTranscriptFetcher()

    # Retrieve or create the Assistant TODO
    st.session_state.assistant = YouTubeAssistant(client, transcript_fetcher)

if 'threads' not in st.session_state:
    # Initialize threads
    st.session_state.threads = []

# Set title and description
st.title('YouTube Smart Assistant')
st.write('Ask me something about a YouTube video and I will answer you!')

with st.sidebar:

    with st.form(key='my_form'):

        st.markdown('## Let\'s start a new conversation!')

        # The URL of the YouTube video the user is interested in
        video_url = st.text_input("YouTube video")

        # True when the user pushes the Ask button
        wanna_chat = st.form_submit_button("Analyse it!")
        if wanna_chat:
            if is_valid_url(video_url):
                st.session_state.current_thread = st.session_state.assistant.create_thread(video_url)
                st.session_state.threads.append(
                    st.session_state.current_thread)
            else:
                st.error("Please enter a valid YouTube URL")

    # Display chat messages from history on app rerun
    for thread in st.session_state.threads:
        callback = lambda thread: st.session_state.__setitem__("current_thread", thread)
        st.button(
            f"Thread {thread.id}",
            on_click=callback(thread),
            type = "primary" if thread == st.session_state.current_thread else "secondary"
        )

# Display chat messages from history on app rerun
if "current_thread" in st.session_state:
    for message in st.session_state.current_thread.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# React to user input
if prompt := st.chat_input(f"Your question..."):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # TODO check if the transcript is available and user has asked a question
    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner():
            response = st.session_state.assistant.ask_question(
                st.session_state.current_thread, prompt)
            st.markdown(response)
