from argparse import ArgumentTypeError
from pathlib import Path

__all__ = ['ArgTypes']


class ArgTypes:
    @staticmethod
    def directory_type(value):
        from .args import state

        result = Path(state.working_dir, value).resolve()

        if result.exists() and not result.is_dir():
            raise ArgumentTypeError(f'{value!r} is not a directory')

        return result

    @staticmethod
    def existing_directory_type(value):
        from .args import state

        result = Path(state.working_dir, value).resolve()

        if not result.is_dir():
            raise ArgumentTypeError(f'{value!r} is not a directory')

        return result

    @staticmethod
    def working_directory_type(value):
        from .args import state

        state.working_dir = ArgTypes.existing_directory_type(value)

        return state.working_dir
