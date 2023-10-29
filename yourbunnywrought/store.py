from pathlib import Path

from .singleton import SingletonMetaclass

__all__ = ['Store']


class Store(metaclass=SingletonMetaclass):
    def __init__(self, burrow: Path):
        if not burrow.exists():
            burrow.mkdir(parents=True)

        self.burrow = burrow
