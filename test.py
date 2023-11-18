import logging
import sys
import os

from openai import OpenAI
from dotenv import load_dotenv
from mock_openai_client import MockOpenaiClient
from youtube_thread import YouTubeThread

from youtube_assistant import YouTubeAssistant
from youtube_transcript_fetcher import YouTubeTranscriptFetcher


# TODO convert to unittest framework

load_dotenv()
logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

api_key = os.getenv('OPENAI_API_KEY')
client = MockOpenaiClient()
transcript_fetcher = YouTubeTranscriptFetcher()
assistant = YouTubeAssistant(client, transcript_fetcher)
thread = assistant.create_thread("https://www.youtube.com/watch?v=qSAVIDivILk")
answer = assistant.ask_question(thread, "What is the video about? Write short bullet points.")
print(answer)
