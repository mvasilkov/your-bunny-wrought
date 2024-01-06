from bs4 import BeautifulSoup

__all__ = ['get_title']


def get_title(hypertext: str) -> str | None:
    soup = BeautifulSoup(hypertext, 'html5lib')

    if (h1 := soup.find('h1')) is not None:
        return h1.get_text()

    if (title := soup.find('title')) is not None:
        return title.get_text()

    return None
