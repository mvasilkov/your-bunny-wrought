from ..lazy import LazyVariable


def test_lazy_variable_class():
    init_called = 0

    def init():
        nonlocal init_called
        init_called += 1

        return 'value'

    class T:
        prop = LazyVariable(init)

    assert init_called == 0
    for _ in range(2):
        assert T.prop == 'value'
        assert init_called == 1


def test_lazy_variable_instance():
    init_called = 0

    def init():
        nonlocal init_called
        init_called += 1

        return 'value'

    class T:
        prop = LazyVariable(init)

    t = T()

    assert init_called == 0
    for _ in range(2):
        assert t.prop == 'value'
        assert init_called == 1
