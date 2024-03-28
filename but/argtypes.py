from __future__ import annotations

from argparse import ArgumentTypeError
from pathlib import Path
import sys
from typing import IO

__all__ = ['ArgTypes']


class ArgTypes:
    @staticmethod
    def directory_type(value: str) -> Path:
        from .args import state

        result = Path(state.working_dir, value).resolve()

        if result.exists() and not result.is_dir():
            raise ArgumentTypeError(f'{value!r} is not a directory')

        return result

    @staticmethod
    def existing_directory_type(value: str) -> Path:
        from .args import state

        result = Path(state.working_dir, value).resolve()

        if not result.is_dir():
            raise ArgumentTypeError(f'{value!r} is not a directory')

        return result

    @staticmethod
    def existing_file_type(value: str) -> Path:
        from .args import state

        result = Path(state.working_dir, value).resolve()

        if not result.is_file():
            raise ArgumentTypeError(f'{value!r} is not a file')

        return result

    @staticmethod
    def existing_script_file_type(value: str) -> Path:
        from .args import state

        results = [
            Path(state.working_dir, value).resolve(),
            Path(state.working_dir, value + '.py').resolve(),
            Path(state.working_dir, value + '.b').resolve(),
            Path(state.working_dir, 'scripts', value).resolve(),
            Path(state.working_dir, 'scripts', value + '.py').resolve(),
            Path(state.working_dir, 'scripts', value + '.b').resolve(),
        ]

        for result in results:
            if result.is_file():
                return result

        raise ArgumentTypeError(f'{value!r} is not a script file')

    @staticmethod
    def not_existing_path_type(value: str) -> Path:
        from .args import state

        result = Path(state.working_dir, value).resolve()

        if result.exists():
            raise ArgumentTypeError(f'{value!r} already exists')

        return result

    @staticmethod
    def working_directory_type(value: str) -> Path:
        '''
        Unique to the `--working-dir` option, this is used to set the working
        directory during `parse_args()`.
        '''
        from .args import state

        state.working_dir = ArgTypes.existing_directory_type(value)

        return state.working_dir

    @staticmethod
    def stdin_literal_type(value: str) -> IO[str]:
        if value == '-':
            return sys.stdin

        raise ArgumentTypeError(f'{value!r} is not the literal `-`')

    @staticmethod
    def one_of_type(*types):
        def _one_of_type(value):
            for fn in types:
                try:
                    return fn(value)
                except Exception:
                    continue

            readable_types = ', '.join(fn.__name__ for fn in types)
            raise ArgumentTypeError(f'{value!r} is not one of ({readable_types})')

        return _one_of_type
