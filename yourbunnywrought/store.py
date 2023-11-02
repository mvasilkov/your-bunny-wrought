from pathlib import Path

from .singleton import SingletonMetaclass

__all__ = ['Store']


class Store(metaclass=SingletonMetaclass):
    burrow: Path

    def set_burrow(self, burrow: Path):
        if not burrow.is_dir():
            burrow.mkdir(parents=True)

        self.burrow = burrow
