import re
from xml.etree import ElementTree as etree

from markdown.preprocessors import Preprocessor
from markdown.blockprocessors import BlockProcessor

LINE_NUM = r'([0-9]+[a-z]?´?(?:[–\-/][0-9]*[a-z]?)?)\.(-?)'


class LineNumsPreproc(Preprocessor):

    RE_REMAINDER = r'\s*(.*?)(?<!\s)\s*$'

    RE_LINE = re.compile(fr'^{LINE_NUM}{RE_REMAINDER}')
    RE_LINE_INDENT = re.compile(fr'^\((\d+),\s*indent\){RE_REMAINDER}')

    def run(self, lines):
        new_lines = []
        prev = True  # Track whether previous line has a line number or not
        # so we can separate numbered lines in blocks
        for line in lines:
            m = self.RE_LINE.search(line)
            if m:
                n, hyph, rem = m.groups()
                n = n.replace('-', '–')
                # Use en-dash for ranges instead of hyphen
                line_break = ' break=no' if hyph else ''
                if not prev:
                    new_lines.append('')
                new_lines.append(f'{{LINE n={n}{line_break}}}{rem}')
                prev = True
            else:
                m = self.RE_LINE_INDENT.search(line)
                if m:
                    n, rem = m.groups()
                    if not prev:
                        new_lines.append('')
                    new_lines.append(f'{{LINE n={n} rend=indent}}{rem}')
                    new_lines.append(f'')
                    prev = True
                else:
                    if prev:
                        new_lines.append('')
                    new_lines.append(line)
                    prev = False
        return new_lines


class NumberedBlocksProcessor(BlockProcessor):

    RE_LINE_DECL = re.compile(r'^\{LINE (.+?)\}')

    def test(self, parent, block):
        return all(
            self.RE_LINE_DECL.search(line) for line in block.split('\n')
        )

    def run(self, parent, blocks):
        lines = blocks.pop(0).split('\n')
        for line in lines:
            m = self.RE_LINE_DECL.search(line)
            attribs = [attr.split('=') for attr in m.group(1).split(' ')]
            content = line[m.end():]

            line_el = etree.SubElement(parent, 'l')
            for attr in attribs:
                line_el.set(*attr)
            line_el.text = content


def register_line_nums(md):
    md.preprocessors.register(
        LineNumsPreproc(md), 'linenums_preproc', 11
    )
    md.parser.blockprocessors.register(
        NumberedBlocksProcessor(md.parser), 'lineblocks', 120
    )
