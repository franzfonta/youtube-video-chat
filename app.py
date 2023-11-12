import logging
import sys
import os
import time

from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi


def retrieve_run(thread_id, run_id, max_retries=5, base_delay=2):
    """
    Polls a run until it is completed or until the maximum number of retries is reached.

    Args:
        thread_id (str): The ID of the thread containing the run.
        run_id (str): The ID of the run to poll.
        max_retries (int, optional): The maximum number of times to retry polling the run. Defaults to 5.
        base_delay (int, optional): The base delay (in seconds) between retries. Defaults to 2.

    Returns:
        dict: The completed run object.

    Raises:
        Exception: If the maximum number of retries is reached and the run is still not completed.
    """
    # Poll the run until it is completed
    retries = 0
    while retries < max_retries:
        logging.info(f"Attempt {retries + 1}")
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id, run_id=run_id)
        logging.info(run.status)
        if run.status == "completed":
            return run
        else:
            retries += 1
            delay = (base_delay * 2 ** retries)
            logging.info(f"Retrying in {delay:.2f} seconds...")
            time.sleep(delay)
    raise Exception("Max retries reached, operation failed.")


load_dotenv()
logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# initialize openai
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

# Initialize the assistant and the thread
if 'assistant' not in st.session_state:
    # Retrieve or create the Assistant
    # TODO instead of creating a new assistant every time, retrieve the existing one
    # client.beta.assistants.list()
    st.session_state.assistant = client.beta.assistants.retrieve(
        "asst_LPQPZEeSHTUPxsap2htGVGYa")
    if not st.session_state.assistant:
        st.session_state.assistant = client.beta.assistants.create(
            name="YouTube Transcript Assistant",
            instructions="You are a news feed. Use video transcripts to best respond customer queries.",
            tools=[],
            model="gpt-4-1106-preview"
        )
    # Create a new thread
    st.session_state.thread = client.beta.threads.create()

# Set title and description
st.title('YouTube Smart Assistant')
st.write('Ask me something about a YouTube video and I will answer you!')

# Display question and choices
col1, col2 = st.columns(2)

with col1:
    # The URL of the YouTube video the user is interested in
    # TODO validate URL
    video_url = st.text_input("Enter the URL")
    # The user question
    user_question = st.text_input(f"Your question")
    # True when the user pushes the Ask button
    is_asking = st.button("Ask")

with col2:

    # If the user entered a URL and a question and clicked on the Ask button
    if is_asking and video_url and user_question:

        try:
            # Extract the video ID from the URL
            video_id = video_url.split('v=')[1]

            # Use the youtube-transcript-api to fetch the transcript
            # TODO Dinamically identify the transcript language (from user question or even better from the video itself)
            transcript_data = YouTubeTranscriptApi.get_transcript(
                video_id, languages=['en'])
            full_transcript = " ".join([entry['text']
                                       for entry in transcript_data])

            # Create a new message in the thread
            query = f"I have a question about this YouTube video transcript: \n\"{full_transcript}\".\n My question is: {user_question}"
            message = client.beta.threads.messages.create(
                thread_id=st.session_state.thread.id,
                role="user",
                content=query
            )

            # Create a new run
            run = client.beta.threads.runs.create(
                thread_id=st.session_state.thread.id,
                assistant_id=st.session_state.assistant.id
            )

            # Wait for the run to complete
            run = retrieve_run(st.session_state.thread.id, run.id)

            # Retrieve the last message in the thread
            messages = client.beta.threads.messages.list(
                thread_id=st.session_state.thread.id
            )
            last_message = messages[0].data 

            # Display the answer
            st.write(last_message.content[0].text.data)

        except Exception as e:
            logging.error(e)
            st.write(f"No transcript available")
