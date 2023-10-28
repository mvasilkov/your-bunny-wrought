#!/usr/bin/env python

from pathlib import Path
import sys

from zenith import zprint

OUR_ROOT = Path(__file__).parents[1].resolve()

if __name__ == '__main__' and not __package__:
    sys.path.insert(0, str(OUR_ROOT))
    __package__ = 'yourbunnywrought'

from . import VERSION

BUNNER = rf'''
[010]   YOUR [012](\_/)
[010]  BUNNY [012]( •.•)
[010]WROUGHT [012]/    つ [010]v{VERSION}[/]
'''


def run():
    zprint(BUNNER)


if __name__ == '__main__':
    run()
