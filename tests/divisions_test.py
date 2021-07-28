from leidenmark import leiden_plus


def test_divisions():
    assert leiden_plus('<D=.1_2+3.fragment Test =D>') == '<div n="1_2+3" subtype="fragment" type="textpart">Test</div>'
