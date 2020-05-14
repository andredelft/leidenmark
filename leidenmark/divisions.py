import re
from xml.etree import ElementTree as etree

from markdown.preprocessors import Preprocessor
from markdown.blockprocessors import BlockProcessor
from markdown.treeprocessors import Treeprocessor

from .exceptions import LeidenPlusSyntaxError


class DivisionsPreproc(Preprocessor):

    RE_OPEN = re.compile(r'<D=\.(.+?)\.([a-z]+)<=|<D=.([rv])<=')
    RE_CLOSE = re.compile(r'=>=D>')

    def _find_first_mark(self, line):
        open_match = self.RE_OPEN.search(line)
        close_match = self.RE_CLOSE.search(line)
        if (not open_match) and (not close_match):
            return None, ''
        elif (not open_match) and close_match:
            return close_match, 'c'
        elif open_match and (not close_match):
            return open_match, 'o'
        else: # open_match and close_match
            if open_match.start() < close_match.start():
                return open_match, 'o'
            else: # open_match.start() > close_match.start()
                return close_match, 'c'

    def run(self, lines):
        new_lines = []
        div_ids = []
        div_counter = 1
        for i, line in enumerate(lines):
            match, mark_type = self._find_first_mark(line)
            if not match:
                new_lines.append(line)
            while match:
                new_lines.append(line[:match.start()])
                if mark_type == 'o':
                    n, div_type, rv = match.groups()
                    if rv:
                        new_line = f'{{DIV-OPEN id={div_counter} n={rv}}}'
                    else:
                        new_line = f'{{DIV-OPEN id={div_counter} subtype={div_type} n={n}}}'
                    new_lines += [
                        '', new_line, ''
                    ]
                    div_ids.append(div_counter)
                    div_counter += 1
                elif mark_type == 'c':
                    try:
                        new_lines += ['', f'{{DIV-CLOSE id={div_ids[-1]}}}', '']
                    except IndexError:
                        i_start = i - 3 if i >= 3 else 0
                        traceback = '\n'.join(lines[i_start:i+1])
                        raise LeidenPlusSyntaxError(
                            f"Text has a '=>=D>' too many, traceback:\n\n{traceback}"
                        )
                    else:
                        del div_ids[-1]
                line = line[match.end():]
                match, mark_type = self._find_first_mark(line)
        if div_ids != []:
            raise LeidenPlusSyntaxError(
                "Text ended while some Leiden+ division marks have not been closed"
            )
        return new_lines


class DivisionMarkProcessor(BlockProcessor):

    RE_OPEN = re.compile(r'^\{(DIV-OPEN) (.+?)\}')
    RE_CLOSE = re.compile(r'^\{(DIV-CLOSE) (.+?)\}')

    def test(self, parent, block):
        return bool(self.RE_OPEN.search(block)) or bool(self.RE_CLOSE.search(block))

    def run(self, parent, blocks):
        lines = blocks.pop(0).split('\n')
        if len(lines) > 1 and not all(re.search(r'\s*', line) for line in lines[1:]):
            blocks.insert(0, '\n'.join(lines[1:]))

        match = self.RE_OPEN.search(lines[0])
        if not match:
            match = self.RE_CLOSE.search(lines[0])
        el = etree.SubElement(parent, match.group(1))
        attribs = [attr.split('=', maxsplit = 1) for attr in match.group(2).split(' ')]
        [el.set(*attrib) for attrib in attribs]


class DivisionMarkTreeproc(Treeprocessor):

    def run(self, root):
        el_close = root.find('./DIV-CLOSE')
        while el_close != None:
            ID = el_close.attrib['id']
            el_open = root.find(f'./DIV-OPEN[@id="{ID}"]')
            i_open = root.getchildren().index(el_open)
            i_close = root.getchildren().index(el_close)
            for _ in range(i_open + 1, i_close):
                # We don't have to increase the index since it shifts
                # automatically when elements are deleted
                root[i_open].append(root[i_open + 1])
                del root[i_open + 1]
            el_open.tag = 'div'
            el_open.attrib.pop('id')
            el_open.attrib['type'] = 'textpart'
            del root[root.getchildren().index(el_close)]
            el_close = root.find('./DIV-CLOSE')
