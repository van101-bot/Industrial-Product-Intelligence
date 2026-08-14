from dataclasses import dataclass
from typing import Optional

import requests
from bs4 import BeautifulSoup


@dataclass
class RetrievedDocument:
    url: str
    title: str
    text: str
    status_code: int
    success: bool
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "title": self.title,
            "text": self.text,
            "status_code": self.status_code,
            "success": self.success,
            "error": self.error,
        }


def retrieve_page(url: str, timeout: int = 15) -> RetrievedDocument:
    """
    Retrieve a webpage and convert its HTML into clean text.
    """

    try:
        response = requests.get(
            url,
            timeout=timeout,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 "
                    "(KHTML, like Gecko) "
                    "Chrome/131.0 Safari/537.36"
                )
            },
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove elements that don't contain useful product information.
        for element in soup(
            ["script", "style", "noscript", "svg"]
        ):
            element.decompose()

        title = soup.title.get_text(strip=True) if soup.title else ""

        text = soup.get_text(
            separator=" ",
            strip=True,
        )

        return RetrievedDocument(
            url=url,
            title=title,
            text=text,
            status_code=response.status_code,
            success=True,
        )

    except requests.RequestException as exc:

        return RetrievedDocument(
            url=url,
            title="",
            text="",
            status_code=0,
            success=False,
            error=str(exc),
        )