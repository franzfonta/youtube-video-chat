from youtube_transcript_api import YouTubeTranscriptApi


class YouTubeTranscriptFetcher:
    def get_transcript(self, video_url: str) -> str:

        # Extract the video ID from the URL
        video_id = video_url.split('v=')[1]

        # Use the youtube-transcript-api to fetch the transcript
        # TODO Dinamically identify the transcript language (from user question or even better from the video itself)
        transcript_data = YouTubeTranscriptApi.get_transcript(
            video_id, languages=['en'])

        # Return the transcript as a single string
        return " ".join([entry['text'] for entry in transcript_data])
