from dataclasses import dataclass, field
from typing import Any


@dataclass
class YouTubeThread:
    """
    Represents a YouTube thread for video chat.

    Attributes:
        video_url (str): The URL of the YouTube video.
        transcript (str): The transcript of the video.
        openai_thread (Any): The OpenAI thread object.
        messages (list): The list of messages in the thread.
    """

    video_url: str
    transcript: str
    openai_thread: Any
    messages: list = field(default_factory=list)
