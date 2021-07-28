from leidenmark import leiden_plus


def above_test():
    assert leiden_plus('\\above/') == '\\above/'
    assert leiden_plus('<= \\above/ =>') == '<ab><add place="above">above</add></ab>'
