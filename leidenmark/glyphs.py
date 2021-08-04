from xml.etree import ElementTree as etree

from markdown.inlinepatterns import InlineProcessor

GLYPHS = ['slanting-stroke', 'tripunct', 'chirho', 'leaf']
RE_GLYPH = rf'\*({"|".join(GLYPHS)})(\??)\*'


class GlyphProcessor(InlineProcessor):

    def handleMatch(self, m, data):

        if m.group(2):
            el = etree.Element('unclear')
            etree.SubElement(el, 'g', type=m.group(1))
        else:
            el = etree.Element('g', type=m.group(1))

        return el, m.start(), m.end()


def register_glyphs(md):
    md.inlinePatterns.register(
        GlyphProcessor(RE_GLYPH, md), 'foreign', 61  # Before underscore proc
    )
