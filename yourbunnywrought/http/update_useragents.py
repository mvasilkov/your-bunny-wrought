#!/usr/bin/env python

import json
from pathlib import Path

from bs4 import BeautifulSoup
import httpx

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/605.1.15 (KHTML, like Gecko) '
        'Version/17.3.1 Safari/605.1.15'
    )
}
SAVE_FILE = Path(__file__).parent.resolve() / 'useragents.json'


def update_api():
    response = httpx.get('https://www.useragents.me/api', headers=HEADERS)
    response.raise_for_status()
    useragents = response.json().get('data')
    SAVE_FILE.write_text(
        json.dumps(useragents, separators=(',', ':')),
        encoding='utf-8',
        newline='\n',
    )


def update():
    response = httpx.get('https://www.useragents.me', headers=HEADERS)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html5lib')
    container = soup.find(id='most-common-desktop-useragents-json-csv')
    textarea = container.find('textarea')
    useragents = json.loads(textarea.get_text())
    SAVE_FILE.write_text(
        json.dumps(useragents, separators=(',', ':')),
        encoding='utf-8',
        newline='\n',
    )


if __name__ == '__main__':
    # update_api()
    update()
