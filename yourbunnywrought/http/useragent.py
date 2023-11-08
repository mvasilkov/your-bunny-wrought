from functools import cache
import json
from pathlib import Path
import re

from ..binaries import PLATFORM

LOAD_FILE = Path(__file__).parent.resolve() / 'useragents.json'


@cache
def get_user_agent() -> str:
    pattern = None
    match PLATFORM[:3]:
        case 'lin':
            pattern = r'\bLinux\b'
        case 'mac':
            pattern = r'\bMac OS X\b'
        case 'win':
            pattern = r'\bWindows NT\b'

    useragents = json.loads(LOAD_FILE.read_text(encoding='utf-8'))
    if pattern and (useragents2 := [ua for ua in useragents if re.search(pattern, ua['ua'])]):
        useragents = useragents2

    useragents.sort(key=lambda ua: ua['pct'], reverse=True)
    return useragents[0]['ua']
