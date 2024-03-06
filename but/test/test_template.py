from ..template import render_to_string


def test_render_to_string():
    hello = render_to_string('{{ hello }}, {{ world }}!', {'hello': 'hello', 'world': 'world'})
    assert hello == 'hello, world!'
