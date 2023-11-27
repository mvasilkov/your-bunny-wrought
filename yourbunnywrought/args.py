from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path

from .cli_modules import CLI_MODULES, CLI_RESOLVE_CMD_TO_MOD

__all__ = ['args']


class ArgTypes:
    @staticmethod
    def path_type(value):
        result = Path(value).resolve()

        if result.exists() and not result.is_dir():
            raise ArgumentTypeError(f'{value!r} is not a directory')

        return result

    @staticmethod
    def existing_path_type(value):
        result = Path(value).resolve()

        if not result.is_dir():
            raise ArgumentTypeError(f'{value!r} is not a directory')

        return result


parser = ArgumentParser(add_help=False)

parser.add_argument('--burrow', type=ArgTypes.path_type, default=Path.home() / '.burrow')

subparsers = parser.add_subparsers(dest='command')
for module in CLI_MODULES:
    for command in module.init_cli(subparsers, ArgTypes):
        CLI_RESOLVE_CMD_TO_MOD[command] = module

args = parser.parse_args()
