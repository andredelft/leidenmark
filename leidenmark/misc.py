from xml.etree import ElementTree as etree

from markdown.inlinepatterns import InlineProcessor

RE_HETA = r'(?:[_*]\u0323?)(h\u0323?)(?:[_*]\u0323?)'


class HetaProcessor(InlineProcessor):

    def handleMatch(self, m, data):
        el = etree.Element('em')
        el.text = m.group(1)
        return el, m.start(), m.end()
