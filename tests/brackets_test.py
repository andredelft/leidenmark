from leidenmark import leiden_plus


def test_above():
    assert leiden_plus('\\above/') == '\\above/'
    assert leiden_plus('<= \\above/ =>') == '<ab><add place="above">above</add></ab>'


def test_interlinear():
    assert leiden_plus('||interlin: some text||') == '<add place="interlinear">some text</add>'
