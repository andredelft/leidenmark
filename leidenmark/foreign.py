from xml.etree import ElementTree as etree

from markdown.inlinepatterns import InlineProcessor

RE_FOREIGN = r'~\|(.+?)\|~([a-zA-Z\-]+)'


class ForeignProcessor(InlineProcessor):

    def handleMatch(self, m, data):
        el = etree.Element('foreign')
        el.set('xml:lang', m.group(2))
        el.text = m.group(1)
        return el, m.start(), m.end()


def register_foreign(md):
    md.inlinePatterns.register(
        ForeignProcessor(RE_FOREIGN, md), 'foreign', 116
    )
