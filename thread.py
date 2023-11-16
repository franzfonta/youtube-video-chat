class Thread:
    def __init__(self, video_url: str, full_transcript: str, thread):
        self.video_url = video_url
        self.full_transcript = full_transcript
        self.openai_thread = thread
        self.id = thread.id
        # TODO create another constructor to use when the thread already exists
        self.messages = []
