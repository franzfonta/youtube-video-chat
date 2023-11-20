from urllib.parse import ParseResult, urlparse


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
