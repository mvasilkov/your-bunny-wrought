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
from .scripts.batch import invoke

BUNNER = rf'''
[010]   YOUR [011](\_/)
[010]  BUNNY [011]( •.•)
[010]WROUGHT [011]/    つ [010]v{VERSION} │ {PLATFORM}[/]
'''


def app(args, module):
    zprint(BUNNER)

    invoke(args, module)


def run():
    from .args import args
    from .cli_modules import CLI_RESOLVE_CMD_TO_MOD

    module = CLI_RESOLVE_CMD_TO_MOD.get(args.command)

    app(args, module)


if __name__ == '__main__':
    run()
