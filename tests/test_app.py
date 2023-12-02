import logging
import os
import sys

from dotenv import load_dotenv

from tests.mock_openai_client import MockOpenaiClient
from youtube_video_chat.helpers import fetch_youtube_transcript
from youtube_video_chat.youtube_assistant import YouTubeAssistant

# TODO convert to unittest framework

load_dotenv()
logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

api_key = os.getenv('OPENAI_API_KEY')
client = MockOpenaiClient()
assistant = YouTubeAssistant(
    client, "stub_assistant", fetch_youtube_transcript)
thread = assistant.create_thread("https://www.youtube.com/watch?v=qSAVIDivILk")
answer = assistant.ask_question(
    thread, "What is the video about? Write short bullet points.")
print(answer)
