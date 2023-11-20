from typing import Optional

from youtube_transcript_api import YouTubeTranscriptApi


class YouTubeTranscriptFetcher:
    """
    A class for fetching the transcript of a YouTube video.
    """

    def get_transcript(self, video_url: str) -> Optional[str]:
        """
        Fetches the transcript of a YouTube video.

        Args:
            video_url (str): The URL of the YouTube video.

        Returns:
            Optional[str]: The transcript of the video as a single string, or None if the transcript is not available.
        """

        # Extract the video ID from the URL
        # TODO use urllib.parse to avoid string manipulation
        video_id = video_url.split('v=')[1]

        # Use the youtube-transcript-api to fetch the transcript
        # TODO Check if the video has a transcript for the user language
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id, languages=['en'])

        # Return the transcript as a single string
        return " ".join([entry['text'] for entry in transcript])
