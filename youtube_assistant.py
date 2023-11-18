import logging
import time
from youtube_thread import YouTubeThread

from youtube_transcript_fetcher import YouTubeTranscriptFetcher


class YouTubeAssistant:

    def __init__(self, client, transcript_fetcher: YouTubeTranscriptFetcher):
        self.client = client

        self.transcript_fetcher = transcript_fetcher

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

    def create_thread(self, video_url: str) -> YouTubeThread:
        openai_thread = self.client.beta.threads.create()
        transcript = self.transcript_fetcher.get_transcript(video_url)
        return YouTubeThread(video_url, transcript, openai_thread)

    def __retrieve_run(self, thread_id: str, run_id: str, max_retries: int = 5, base_delay: int = 2):
        # Poll the run until it is completed
        retries = 0
        while retries < max_retries:
            logging.info(f"Attempt {retries + 1}")
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id, run_id=run_id)
            if run.status == "completed":
                return run
            else:
                retries += 1
                delay = (base_delay * 2 ** retries)
                logging.info(f"Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
        raise Exception("Max retries reached, operation failed.")

    def ask_question(self, thread: YouTubeThread, prompt: str) -> str:

        # Add user message to thread
        thread.messages.append({"role": "user", "content": prompt})

        try:

            # Create a new message in the thread
            query = f"I have a question about this YouTube video transcript: \n\"{thread.transcript}\".\n My question is: {prompt}"
            message = self.client.beta.threads.messages.create(
                thread_id=thread.openai_thread.id,
                role="user",
                content=query
            )

            # Create a new run
            run = self.client.beta.threads.runs.create(
                thread_id=thread.openai_thread.id,
                assistant_id=self.assistant.id
            )

            # Wait for the run to complete
            run = self.__retrieve_run(thread.openai_thread.id, run.id)

            # Retrieve the last message in the thread
            messages = self.client.beta.threads.messages.list(
                thread_id=thread.openai_thread.id)
            response = messages.data[0].content[0].text.value

            # Add assistant response to chat history
            thread.messages.append({"role": "assistant", "content": response})

            return response

        except Exception as e:
            logging.error(e)
