from __future__ import annotations

from argparse import ArgumentParser
from pathlib import Path

from .argtypes import ArgTypes
from .cli_modules import CLI_MODULES, CLI_RESOLVE_CMD_TO_MOD

__all__ = ['get_args_module', 'state']


class State:
    parser: ArgumentParser
    working_dir: Path

    def __init__(self):
        self.parser = ArgumentParser(add_help=False)

        self.parser.add_argument(
            '-B',
            '--burrow',
            type=ArgTypes.directory_type,
            default=Path('~/.burrow').expanduser(),
        )
        self.parser.add_argument(
            '-C',
            '--working-dir',
            type=ArgTypes.working_directory_type,
            default=Path('.').absolute(),
        )
        self.parser.add_argument(
            '-P',
            '--persistent',
            action='store_true',
        )

        self.working_dir = self.parser.get_default('working_dir')

        subparsers = self.parser.add_subparsers(dest='command')
        for module in CLI_MODULES:
            for command in module.init_cli(subparsers):
                CLI_RESOLVE_CMD_TO_MOD[command] = module


state = State()


def get_args_module(*xs):
    state.working_dir = state.parser.get_default('working_dir')
    args = state.parser.parse_args(*xs)
    module = CLI_RESOLVE_CMD_TO_MOD.get(args.command)

    return args, module
