from dataclasses import dataclass
from typing import Any


@dataclass
class YouTubeThread:
    
    video_url: str
    transcript: str
    openai_thread: Any
    messages = []
