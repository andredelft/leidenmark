import re
from xml.etree import ElementTree as etree

from markdown.preprocessors import Preprocessor
from markdown.inlinepatterns import InlineProcessor

from .line_nums import LINE_NUM

CA_DOT  = r'((?:ca\.)?)'
CA      = r'((?:ca)?)'
NUM     = r'(\d+(?:-\d+)?|\?|)'
LINE    = r'((?:lin)?)'

RE_CHARACTER_GAP = fr'\[{CA}\.{NUM}\]'
RE_LINE_GAP      = fr'lost\.{CA_DOT}{NUM}lin'
RE_SPACE         = fr'vac\.{CA_DOT}{NUM}{LINE}'

RE_SUPPLIED = r'\[([^\[\]\n]*?)\]'

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
        el.set('quantity', num if num else '1')


class CompleteSquareBrackets(Preprocessor):

    RE_START = re.compile(fr'^(?P<start>(?:{LINE_NUM})?\s*)(?P<end>[^\[\]\n]*?\])')
    RE_END = re.compile(r'(?P<start>\[[^\[\]\n]*?)(?<!\s)\s*$')

    def run(self, lines):
        new_lines = []

        for line in lines:
            line = self.RE_START.sub(
                lambda m: f'{m.group("start")}[.?]' if m.group('end') == ']'
                else f'{m.group("start")}[{m.group("end")}',
                line
            )
            line = self.RE_END.sub(
                lambda m: '[.?]' if m.group() == '['
                else f'{m.group("start")}]',
                line
            )
            new_lines.append(line)

        return new_lines


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


class SuppliedProcessor(InlineProcessor):

    def handleMatch(self, m, data):
        el = etree.Element('supplied')
        el.set('reason', 'lost')
        el.text = m.group(1)
        return el, m.start(), m.end()
