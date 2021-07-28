import pytest
from leidenmark import leiden_plus


def test_base():
    # Paragraphs/sections/textparts
    assert leiden_plus('no paragraph') == 'no paragraph'
    assert leiden_plus('paragraph', enable_paragraphs=True) == '<p>paragraph</p>'
    # Issue #1: assert leiden_plus('<= Leiden+ section =>', enable_paragraphs=True) == '<ab>Leiden+ section</ab>'
    assert leiden_plus('<= Leiden+ section =>') == '<ab>Leiden+ section</ab>'
    assert leiden_plus('<D=.1 Leiden+ textpart =D>') == '<div n="1" type="textpart">Leiden+ textpart</div>'


LEIDEN_PLUS_SAMPLE = """\
<D=.r<=
1. Lorem ipsum dolor
vac.1lin
2. sit amet, con[ca.3]c
3.-etur adipiscing
=>=D>
<D=.v<=
lost.2lin
6. ut labore et dol
7.-ore magna aliqua
=>=D>
"""

LEIDEN_PLUS_SAMPLE_OUTPUT = """\
<div n="r" type="textpart">
  <ab>
    <l n="1">Lorem ipsum dolor</l>
    <space quantity="1" unit="line"/>
    <l n="2">sit amet, con<gap precision="low" quantity="3" reason="lost" unit="character"/>c</l>
    <l break="no" n="3">etur adipiscing</l>
  </ab>
</div>
<div n="v" type="textpart">
  <ab>
    <gap quantity="2" unit="line"/>
    <l n="6">ut labore et dol</l>
    <l break="no" n="7">ore magna aliqua</l>
  </ab>
</div>\
"""


@pytest.fixture
def leiden_plus_sample():
    return LEIDEN_PLUS_SAMPLE


@pytest.fixture
def leiden_plus_sample_output():
    return LEIDEN_PLUS_SAMPLE_OUTPUT


def test_conversion(leiden_plus_sample, leiden_plus_sample_output):
    assert leiden_plus(leiden_plus_sample, indent=True) == leiden_plus_sample_output
