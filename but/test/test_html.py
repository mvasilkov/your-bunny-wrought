from ..html import get_title


def test_get_title():
    assert get_title('<title>Title</title>') == 'Title'
    assert get_title('<h1>Title</h1>') == 'Title'
    assert get_title('<h2>Title</h2>') is None
    assert get_title('<h1>Title(1)</h1><h1>Title(2)</h1>') == 'Title(1)'
    assert get_title('<title>Title(1)</title><h1>Title(2)</h1>') == 'Title(2)'
