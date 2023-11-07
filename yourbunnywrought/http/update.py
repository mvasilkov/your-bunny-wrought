#!/usr/bin/env python

import json
from pathlib import Path

import httpx

SAVE_FILE = Path(__file__).parent.resolve() / 'useragents.json'


def update():
    response = httpx.get('https://www.useragents.me/api')
    response.raise_for_status()
    useragents = response.json().get('data')
    SAVE_FILE.write_text(
        json.dumps(useragents, separators=(',', ':')),
        encoding='utf-8',
        newline='\n',
    )


if __name__ == '__main__':
    update()
