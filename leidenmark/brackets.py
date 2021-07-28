import re
import xml.etree.ElementTree as etree

from markdown.inlinepatterns import InlineProcessor

from .util import ContextInlineMixin


def format_bracket_re(opening_bracket, closing_bracket):
    re_ob = re.escape(opening_bracket)
    re_cb = re.escape(closing_bracket)
    return fr'[{re_ob}]([^{re_ob}{re_cb}\n]*?)[{re_cb}]'


RE_SUPPLIED = format_bracket_re('[', ']')
RE_ERASURE = format_bracket_re('\u301a\u27e6', '\u301b\u27e7')
RE_ABOVE = format_bracket_re('\\', '/')
RE_INTERLINEAR = r"\|\|interlin:\s*([^\|\n]+?)\|\|"


class BracketProcessor(InlineProcessor, ContextInlineMixin):

    tag = ''
    attrs = {}

    def __init__(self, *args, **kwargs):
        InlineProcessor.__init__(self, *args, **kwargs)

    def handleMatch(self, m, data):
        if not self.in_leiden_plus():
            return None, None, None
        else:
            el = etree.Element(self.tag, **self.attrs)
            el.text = m.group(1)
            return el, m.start(), m.end()


class SuppliedProcessor(BracketProcessor):

    tag = 'supplied'
    attrs = {'reason': 'lost'}


class ErasureProcessor(BracketProcessor):

    tag = 'del'
    attrs = {'rend': 'erasure'}


class AboveProcessor(BracketProcessor):

    tag = 'add'
    attrs = {'place': 'above'}


class InterlinearProcessor(InlineProcessor):

    def handleMatch(self, m, data):
        el = etree.Element('add', place='interlinear')
        el.text = m.group(1)
        return el, m.start(), m.end()


def register_brackets(md):
    md.inlinePatterns.register(
        SuppliedProcessor(RE_SUPPLIED, md), 'supplied', 5
    )
    md.inlinePatterns.register(
        ErasureProcessor(RE_ERASURE, md), 'erasure',  115
    )
    md.inlinePatterns.register(
        AboveProcessor(RE_ABOVE, md), 'above', 114
    )
    md.inlinePatterns.register(
        InterlinearProcessor(RE_INTERLINEAR, md), 'interlinear', 113
    )
