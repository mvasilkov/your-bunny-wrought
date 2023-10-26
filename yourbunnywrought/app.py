#!/usr/bin/env python

from pathlib import Path
import sys

OUR_ROOT = Path(__file__).parents[1].resolve()

if __name__ == '__main__' and not __package__:
    sys.path.insert(0, str(OUR_ROOT))
    __package__ = 'yourbunnywrought'

from . import VERSION

BUNNER = rf'''
   YOUR (\_/)
  BUNNY ( •.•)
WROUGHT /    つ v{VERSION}
'''


def run():
    print(BUNNER)


if __name__ == '__main__':
    run()
