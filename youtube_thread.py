from dataclasses import dataclass, field
from typing import Any


@dataclass
class YouTubeThread:
    
    video_url: str
    transcript: str
    openai_thread: Any
    messages: list = field(default_factory=list)
