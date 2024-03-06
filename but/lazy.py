__all__ = ['LazyVariable']


class LazyVariable:
    def __init__(self, init):
        self._init = init
        self._cache = None

    def __get__(self, instance, owner=None):
        if self._cache is None:
            self._cache = self._init()
        return self._cache
