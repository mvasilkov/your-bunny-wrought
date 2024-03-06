#!/usr/bin/env python

from pathlib import Path
import sys

from zenith import zprint

OUR_ROOT = Path(__file__).parents[1].resolve()

if __name__ == '__main__' and not __package__:
    sys.path.insert(0, str(OUR_ROOT))
    __package__ = 'but'

from . import VERSION
from .binaries import PLATFORM
from .scripts.batch import run

BUNNER = rf'''
[010]   YOUR [011](\_/)
[010]  BUNNY [011]( •.•)
[010]WROUGHT [011]/    つ [010]v{VERSION} │ {PLATFORM}[/]
'''


def main():
    from .args import get_args_module

    args, module = get_args_module()

    zprint(BUNNER)

    if (thread := run(args, module)) is not None:
        try:
            thread.join()
        except KeyboardInterrupt:
            pass


if __name__ == '__main__':
    main()
