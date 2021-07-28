import re
from xml.etree import ElementTree as etree

from .divisions import LEIDEN_PLUS_STATE

from markdown.blockprocessors import BlockProcessor
from markdown.inlinepatterns import InlineProcessor

RE_MIL = r'<=\.(ms|lb|cb|pb|gb) ([^<\n]+?)\s*=>'
RE_DIPLE = r'\(\(diple\??\)\)'
RE_PARAGRAPHOS = r'(?<=\n)----[^\S\n]*(?=\n)'


class MilestoneProcessor(InlineProcessor):

    def handleMatch(self, m, data):
        mil_type, content = m.groups()
        cont_parts = re.split(r'\s+', content)
        el = etree.Element('milestone')
        el.set('unit', 'section')

        if mil_type == 'ms':
            if len(cont_parts) == 1:
                if content.startswith('par.'):
                    el.set('type', 'paragraph')
                    el.set('n', content[4:])
                else:
                    el.set('n', content)
            elif len(cont_parts) == 2:
                if re.search('^[0-9.]+$', cont_parts[0]):
                    el.set('ed', cont_parts[1])
                    el.set('n', cont_parts[0])
                else:
                    el.set('ed', cont_parts[0])
                    el.set('n', cont_parts[1])
            else:
                el.set('ed', ' '.join(cont_parts[:-1]))
                el.set('n', cont_parts[-1])

        elif mil_type == 'pb':
            el.set('type', 'page')
            if len(cont_parts) == 1 and re.search(r'^.+\.page\..+$', content):
                cont_parts = content.split('.')
                el.set('ed', cont_parts[0])
                el.set('n', cont_parts[2])
            elif len(cont_parts) == 2:
                if re.search('^[0-9.]+$', cont_parts[0]):
                    el.set('ed', cont_parts[1])
                    el.set('n', cont_parts[0])
                else:
                    el.set('ed', cont_parts[0])
                    el.set('n', cont_parts[1])
            else:
                el.set('ed', cont_parts[:-1])
                el.set('n', cont_parts[-1])

        elif mil_type in ['lb', 'cb', 'gb']:
            el.set(
                'type',
                {'lb': 'line', 'cb': 'column', 'gb': 'gathering'}[mil_type]
            )
            if len(cont_parts) > 1:
                el.set('ed', cont_parts[:-1])
            el.set('n', cont_parts[-1])

        return el, m.start(), m.end()


class DipleProcessor(InlineProcessor):

    def handleMatch(self, m, data):
        el = etree.Element('milestone', rend='diple', unit='undefined')
        return el, m.start(), m.end()


class ParagraphosProcessor(BlockProcessor):

    def test(self, parent, block):
        if not re.search('^-{3,}$', block.strip()):
            return False

        try:
            state = self.parser.state[-1]
        except IndexError:
            return False
        else:
            return state == LEIDEN_PLUS_STATE

    def run(self, parent, blocks):
        blocks.pop(0)
        etree.SubElement(
            parent, 'milestone', rend='paragraphos', unit='undefined'
        )


def register_milestones(md):
    # NB: MilestoneProcessor is not official Leiden+!
    md.inlinePatterns.register(
        MilestoneProcessor(RE_MIL, md), 'milestones', 120
    )
    md.inlinePatterns.register(
        DipleProcessor(RE_DIPLE, md), 'diple', 120
    )
    md.parser.blockprocessors.register(  # Before HRProcessor
        ParagraphosProcessor(md.parser), 'paragraphos', 51
    )
