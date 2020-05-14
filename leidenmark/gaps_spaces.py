import re
from xml.etree import ElementTree as etree

from markdown.inlinepatterns import InlineProcessor


CA_DOT  = r'((?:ca\.)?)'
CA      = r'((?:ca)?)'
NUM     = r'(\d+(?:-\d+)?|\?)'
LINE    = r'((?:lin)?)'

RE_CHARACTER_GAP = fr'\[{CA}\.{NUM}\]'
RE_LINE_GAP      = fr'lost\.{CA_DOT}{NUM}lin'
RE_SPACE         = fr'vac\.{CA_DOT}{NUM}{LINE}'


def _handle_ca(ca, el):
    if ca:
        el.set('precision', 'low')

def _handle_num(num, el):
    if num == '?':
        el.set('extent', 'unknown')
    elif '-' in num:
        num_range = [int(i) for i in num.split('-')]
        el.set('atLeast', str(min(num_range)))
        el.set('atMost', str(max(num_range)))
    else:
        el.set('quantity', num)


class CharacterGapProcessor(InlineProcessor):

    def handleMatch(self, m, data):
        ca, num = m.groups()
        el = etree.Element('gap')
        _handle_num(num, el)
        el.set('unit', 'character')
        _handle_ca(ca, el)
        return el, m.start(), m.end()


class LineGapProcessor(InlineProcessor):

    def handleMatch(self, m, data):
        ca, num = m.groups()
        el = etree.Element('gap')
        _handle_num(num, el)
        el.set('unit', 'line')
        _handle_ca(ca, el)
        return el, m.start(), m.end()


class SpaceProcessor(InlineProcessor):

    def handleMatch(self, m, data):
        ca, num, lin = m.groups()
        el = etree.Element('space')
        _handle_num(num, el)
        el.set('unit', 'line' if lin else 'character')
        _handle_ca(ca, el)
        return el, m.start(), m.end()
