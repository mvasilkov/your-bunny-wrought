from ..singleton import SingletonMetaclass


def test_singleton():
    init_called = 0

    class T(metaclass=SingletonMetaclass):
        initialized = False

        def __init__(self):
            nonlocal init_called
            init_called += 1

            self.initialized = True

    a = T()
    b = T()

    assert init_called == 1
    assert a.initialized
    assert a is b
