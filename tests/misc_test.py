from leidenmark import leiden_plus


def test_handshift():
    assert leiden_plus('$m4') == '<handShift new="m4"/>'
