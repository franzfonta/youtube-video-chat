from tests.mock_openai_client import MockOpenaiClient
from youtube_video_chat.youtube_assistant import YouTubeAssistant


def test_assistant_answers():
    client = MockOpenaiClient()
    assistant = YouTubeAssistant(
        client, "stub_assistant", lambda x: x)
    thread = assistant.create_thread(
        "https://www.youtube.com/watch?v=qSAVIDivILk")
    answer = assistant.ask_question(
        thread, "What is the video about? Write short bullet points.")
    assert answer == "I'm the assistant, here is my answer"
