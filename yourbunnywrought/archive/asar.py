from __future__ import annotations

from contextlib import contextmanager
import json
from pathlib import Path
from struct import unpack

__all__ = ['align_int', 'load_asar']


def align_int(n: int, p: int) -> int:
    '''
    Round the integer `n` up to the nearest multiple of `p` (a power of 2).
    '''
    return (n + p - 1) & -p


class Asar:
    def __init__(self, fp):
        fp.seek(12)
        size = unpack('<I', fp.read(4))[0]
        header_str = fp.read(size).decode('utf-8')

        self.fp = fp
        self.header = json.loads(header_str)
        self.header_end = align_int(16 + size, 4)


@contextmanager
def load_asar(infile: Path):
    with infile.open('rb') as fp:
        yield Asar(fp)
