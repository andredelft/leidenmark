import re
import xml.etree.ElementTree as etree

from markdown.inlinepatterns import InlineProcessor

__all__ = ['RE_SUPPLIED', 'RE_ERASURE', 'SuppliedProcessor', 'ErasureProcessor']

def format_bracket_re(opening_bracket, closing_bracket):
    return fr'[{opening_bracket}]([^{opening_bracket}{closing_bracket}\n]*?)[{closing_bracket}]'

RE_SUPPLIED = format_bracket_re(r'\[', r'\]')
RE_ERASURE  = format_bracket_re(r'\u301a\u27e6', r'\u301b\u27e7')


class BracketProcessor(InlineProcessor):

    tag = ''
    attrs = {}

    def handleMatch(self, m, data):
        el = etree.Element(self.tag)
        for attr, value in self.attrs.items():
            el.set(attr, value)
        el.text = m.group(1)
        return el, m.start(), m.end()


class SuppliedProcessor(BracketProcessor):

    tag = 'supplied'
    attrs = {'reason': 'lost'}


class ErasureProcessor(BracketProcessor):

    tag = 'del'
    attrs = {'rend': 'erasure'}
