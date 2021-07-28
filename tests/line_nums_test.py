from leidenmark import leiden_plus


def test_line_nums():
    assert leiden_plus(
        '<=\n1. Line 1\n2. Line 2\n(3, indent) Indented line 3\n=>'
    ) == (
        '<ab><l n="1">Line 1</l>'
        '<l n="2">Line 2</l>'
        '<l n="3" rend="indent">Indented line 3</l></ab>'
    )
