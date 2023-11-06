#!/usr/bin/env python

from pathlib import Path
import sys

from zenith import zprint

OUR_ROOT = Path(__file__).parents[1].resolve()

if __name__ == '__main__' and not __package__:
    sys.path.insert(0, str(OUR_ROOT))
    __package__ = 'yourbunnywrought'

from . import VERSION
from .binaries import PLATFORM
from .store import Store

BUNNER = rf'''
[010]   YOUR [011](\_/)
[010]  BUNNY [011]( •.•)
[010]WROUGHT [011]/    つ [010]v{VERSION} │ {PLATFORM}[/]
'''


def run(args):
    zprint(BUNNER)

    store = Store()
    store.set_burrow(args.burrow)


if __name__ == '__main__':
    from .args import args

    run(args)
