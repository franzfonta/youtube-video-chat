from youtube_transcript_api import YouTubeTranscriptApi
from typing import Optional


class YouTubeTranscriptFetcher:
    def get_transcript(self, video_url: str) -> Optional[str]:

        # Extract the video ID from the URL
        # TODO use urllib.parse to avoid string manipulation
        video_id = video_url.split('v=')[1]

        # Use the youtube-transcript-api to fetch the transcript
        # TODO Check if the video has a transcript for the user language
        # TODO We don't like implicit dependencies
        transcript_data = YouTubeTranscriptApi.get_transcript(
            video_id, languages=['en'])

        # Return the transcript as a single string
        return " ".join([entry['text'] for entry in transcript_data])
