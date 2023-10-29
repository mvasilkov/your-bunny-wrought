from argparse import ArgumentParser, ArgumentTypeError
from pathlib import Path

__all__ = ['args']


def path_type(value):
    result = Path(value).resolve()

    if result.exists() and not result.is_dir():
        raise ArgumentTypeError(f'{value!r} is not a directory')

    return result


parser = ArgumentParser(add_help=False)

parser.add_argument('--burrow', type=path_type, default=Path.home() / '.burrow')

args = parser.parse_args()
