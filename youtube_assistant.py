import logging
import time

from youtube_transcript_api import YouTubeTranscriptApi


class YouTubeAssistant:

    def __init__(self, client):
        self.client = client

        self.assistant = client.beta.assistants.retrieve(
            "asst_LPQPZEeSHTUPxsap2htGVGYa")
        # TODO instead of creating a new assistant every time, retrieve the existing one
        """
        client.beta.assistants.list()
        if not st.session_state.assistant:
            st.session_state.assistant = client.beta.assistants.create(
                name="YouTube Transcript Assistant",
                instructions="You are a news feed. Use video transcripts to best respond customer queries.",
                tools=[],
                model="gpt-4-1106-preview"
            )
        """

        self.thread = None

    def start_new_thread(self, video_url):

        self.thread = self.client.beta.threads.create()

        # Extract the video ID from the URL
        video_id = video_url.split('v=')[1]

        # Use the youtube-transcript-api to fetch the transcript
        # TODO Dinamically identify the transcript language (from user question or even better from the video itself)
        # TODO Refactor this into a separate function
        transcript_data = YouTubeTranscriptApi.get_transcript(
            video_id, languages=['en'])
        self.full_transcript = " ".join([entry['text'] for entry in transcript_data])

        return self.thread

    def __retrieve_run(self, thread_id, run_id, max_retries=5, base_delay=2):
        # Poll the run until it is completed
        retries = 0
        while retries < max_retries:
            logging.info(f"Attempt {retries + 1}")
            run = self.client.beta.threads.runs.retrieve(
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

    def ask_question(self, user_question):

        if self.thread is None or self.full_transcript is None:
            raise Exception("Thread not created")

        try:

            # Create a new message in the thread
            query = f"I have a question about this YouTube video transcript: \n\"{self.full_transcript}\".\n My question is: {user_question}"
            message = self.client.beta.threads.messages.create(
                thread_id=self.thread.id,
                role="user",
                content=query
            )

            # Create a new run
            run = self.client.beta.threads.runs.create(
                thread_id=self.thread.id,
                assistant_id=self.assistant.id
            )

            # Wait for the run to complete
            run = self.__retrieve_run(self.thread.id, run.id)

            # Retrieve the last message in the thread
            messages = self.client.beta.threads.messages.list(
                thread_id=self.thread.id
            )
            last_message = messages.data[0].content[0].text.value

            # Display the answer
            return last_message.content[0].text.data

        except Exception as e:
            logging.error(e)
            return f"No transcript available"
