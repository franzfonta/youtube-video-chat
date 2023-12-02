from urllib.parse import ParseResult, urlparse

from youtube_transcript_api import YouTubeTranscriptApi


def is_valid_url(url: str) -> bool:
    """
    Check if a URL is valid.

    Args:
        url (str): The URL to be checked.

    Returns:
        bool: True if the URL is valid, False otherwise.
    """
    try:
        result: ParseResult = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def fetch_youtube_transcript(video_url: str) -> str:
    """
    Fetch the transcript of a YouTube video.

    Args:
        video_url (str): The URL of the YouTube video.

    Returns:
        str: The video transcript.
    """

    # Extract the video ID from the URL
    # TODO use urllib.parse to avoid string manipulation
    video_id = video_url.split('v=')[1]

    # Use the youtube-transcript-api to fetch the transcript
    # TODO Check if the video has a transcript for the user language
    # TODO make it async
    transcript = YouTubeTranscriptApi.get_transcript(
        video_id, languages=['en'])

    # TODO Check if the transcript is empty
    # Return the transcript as a single string
    return " ".join([entry['text'] for entry in transcript])
