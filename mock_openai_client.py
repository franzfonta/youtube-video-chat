from unittest.mock import MagicMock
import random


class MockOpenaiClient:
    def __init__(self):
        self.beta = MagicMock()
        self.beta.threads.create = lambda **kwargs: MagicMock(id=str(random.randint(0, 1000)))
        self.beta.threads.runs.retrieve.return_value = MagicMock(status="completed")
        messages = MagicMock()
        messages.data[0].content[0].text.value = "I'm the assistant, here is my answer"
        self.beta.threads.messages.list.return_value = messages
        