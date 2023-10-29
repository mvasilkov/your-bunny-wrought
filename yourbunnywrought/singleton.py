from threading import Lock

__all__ = ['SingletonMetaclass']


class SingletonMetaclass(type):
    _cache = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        cache_key = (cls, args)
        if cache_key not in cls._cache:
            with cls._lock:
                if cache_key not in cls._cache:
                    cls._cache[cache_key] = super().__call__(*args, **kwargs)

        return cls._cache[cache_key]
