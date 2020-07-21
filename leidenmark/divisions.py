import regex as re
from xml.etree import ElementTree as etree

from markdown.preprocessors import Preprocessor
from markdown.blockprocessors import BlockProcessor
from markdown.treeprocessors import Treeprocessor

from .exceptions import LeidenPlusSyntaxError

class DivisionsPreproc(Preprocessor):

    RE_OPEN = re.compile(r"""
        (?:
          <D=\.(\S+?)(?:\.([a-z]+))?    # Division mark <D=.number.divisontype ... =D>
          |<D=\.(r|v|le)                # Division mark (recto, versa, left edge)
          |(<=)(?!\.(?:ms|lb|cb|pb|gb)) # Paragraph mark <= ... => (Check if it is not a milestone)
        )\s*""",
        flags = re.VERBOSE
    )
    RE_CLOSE = re.compile(r"""
        (?:
          (=D>)                                             # Division mark end
          |(?<!<=\.(?:ms|lb|cb|pb|gb) (?:[^<\n]+?)\s*)=>    # Paragraph mark end
        )\s*""",
        flags = re.VERBOSE
    )

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

        in_ab = False
        for i, line in enumerate(lines):
            match, mark_type = self._find_first_mark(line)
            while match:
                new_lines.append(line[:match.start()])
                if mark_type == 'o':
                    if in_ab:
                        raise LeidenPlusSyntaxError('<= ... => cannot be nested')
                    n, div_type, rv, ab = match.groups()
                    if rv:
                        new_line = f'{{DIV-OPEN id={div_counter} n={rv}}}'
                    elif ab:
                        in_ab = True
                        new_line = f'{{AB-OPEN id={div_counter}}}'
                    elif div_type:
                        new_line = f'{{DIV-OPEN id={div_counter} subtype={div_type} n={n}}}'
                    else:
                        new_line = f'{{DIV-OPEN id={div_counter} n={n}}}'
                    new_lines += [
                        '', new_line, ''
                    ]
                    div_ids.append(div_counter)
                    div_counter += 1
                elif mark_type == 'c':
                    div = match.group(1)
                    if div and in_ab:
                        raise LeidenPlusSyntaxError('Incorrect division syntax: <= ... =D>')
                    elif (not div) and (not in_ab):
                        raise LeidenPlusSyntaxError('Incorrect division syntax: <D= ... =>')
                    try:
                        new_lines += ['', f'{{{"DIV" if div else "AB"}-CLOSE id={div_ids[-1]}}}', '']
                    except IndexError:
                        i_start = i - 3 if i >= 3 else 0
                        traceback = '\n'.join(lines[i_start:i+1])
                        raise LeidenPlusSyntaxError(
                            f"Text has a '={D if div else ''}>' too many, traceback:\n\n{traceback}"
                        )
                    else:
                        del div_ids[-1]
                        if not div:
                            in_ab = False
                line = line[match.end():]
                match, mark_type = self._find_first_mark(line)
            new_lines.append(line)
        if div_ids != []:
            raise LeidenPlusSyntaxError(
                "Text ended while some Leiden+ division marks have not been closed"
            )
        return new_lines

class DivisionMarkProcessor(BlockProcessor):

    RE_OPEN = re.compile(r'^\{(DIV-OPEN|AB-OPEN) (.+?)\}')
    RE_CLOSE = re.compile(r'^\{(DIV-CLOSE|AB-CLOSE) (.+?)\}')

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
        for tag in ['AB', 'DIV']:
            el_close = root.find(f'./{tag}-CLOSE')
            while el_close != None:
                ID = el_close.attrib['id']
                el_open = root.find(f'./{tag}-OPEN[@id="{ID}"]')
                if el_open.tail:
                    el_open.text = el_open.tail
                    el_open.tail = None
                i_open = root.getchildren().index(el_open)
                i_close = root.getchildren().index(el_close)
                for _ in range(i_open + 1, i_close):
                    # We don't have to increase the index since it shifts
                    # automatically when elements are deleted
                    root[i_open].append(root[i_open + 1])
                    del root[i_open + 1]
                el_open.tag = tag.lower()
                el_open.attrib.pop('id')
                if tag == 'DIV':
                    el_open.attrib['type'] = 'textpart'
                del root[root.getchildren().index(el_close)]
                el_close = root.find(f'./{tag}-CLOSE')

class TrivialProcessor(BlockProcessor):
    """ Fallback alternative to the ParagraphProcessor. """

    def test(self, parent, block):
        return True

    def run(self, parent, blocks):
        block = blocks.pop(0)
        content = block
        children = parent.getchildren()
        if len(children) == 0:
            if parent.text:
                parent.text += content
            else:
                parent.text = content
        else:
            last_child = children[-1]
            if last_child.tail:
                last_child.tail += content
            else:
                last_child.tail = content
