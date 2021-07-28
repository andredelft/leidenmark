from leidenmark import leiden_plus


def test_paragraphos():
    assert leiden_plus('---') == '<hr/>'
    assert leiden_plus('<= --- =>') == '<ab><milestone rend="paragraphos" unit="undefined"/></ab>'
    assert (
        leiden_plus('<= 1. In between\n---\n2. Two lines =>') ==
        '<ab><l n="1">In between</l><milestone rend="paragraphos" unit="undefined"/><l n="2">Two lines</l></ab>'
    )


def test_diple():
    assert leiden_plus('((diple))') == '<milestone rend="diple" unit="undefined"/>'
