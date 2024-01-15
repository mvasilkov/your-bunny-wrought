from __future__ import annotations

from pathlib import Path

from .lazy import LazyVariable
from .singleton import SingletonMetaclass

__all__ = ['Store']


def get_default_working_dir() -> Path:
    from .args import state

    return state.working_dir


class Store(metaclass=SingletonMetaclass):
    burrow: Path
    working_directory: Path = LazyVariable(get_default_working_dir)

    def set_burrow(self, burrow: Path):
        if not burrow.is_dir():
            burrow.mkdir(parents=True)

        self.burrow = burrow
