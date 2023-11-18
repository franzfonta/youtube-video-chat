from urllib.parse import ParseResult, urlparse


def is_valid_url(url: str) -> bool:
    try:
        result: ParseResult = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False
