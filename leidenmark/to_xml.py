from markdown.postprocessors import Postprocessor
from lxml import etree
import re


class TEIPostprocessor(Postprocessor):

    def __init__(self, md, indent=False, with_root=False):
        self.indent = indent
        self.with_root = with_root
        Postprocessor.__init__(self, md)

    def _replace_tag(self, old_tag, new_tag, **kwargs):
        for el in self.tree.xpath(f'//{old_tag}'):
            el.tag = new_tag
            el.attrib.update(kwargs)

    def run(self, text, indent_unit='  '):
        root_tag = 'root'

        # A dirty namespace hack
        text = text.replace('{http://www.w3.org/XML/1998/namespace}', 'xml:')

        self.tree = etree.fromstring(f'<{root_tag}>{text}</{root_tag}>')

        # heads (from old script, not sure if this is actually encountered, AvD)
        for el in self.tree.xpath('//head'):
            el.tag = 'p'
            head = etree.SubElement(el, 'seg')
            head.attrib['type'] = 'head'

            # Move content of over to <seg>
            head.text = el.text
            el.text = ''
            for child in el.getchildren():
                head.append(child)

        # tables
        for table in self.tree.xpath('//table'):
            new_table = etree.Element('table')

            if table.xpath('thead'):
                row = etree.SubElement(new_table, 'row')
                row.attrib['role'] = 'label'
                for cell in table.xpath('thead/tr/th'):
                    cell.tag = 'cell'
                    row.append(cell)

            for table_row in table.xpath('*[not(self::thead)]/tr'):
                row = etree.SubElement(new_table, 'row')
                for cell in table_row.xpath('td'):
                    cell.tag = 'cell'
                    row.append(cell)

            new_table.tail = table.tail

            container = table.getparent()
            container.insert(container.index(table) + 1, new_table)
            del container[container.index(table)]

        self._replace_tag('em', 'hi', rend='italic')
        self._replace_tag('i', 'hi', rend='italic')
        self._replace_tag('strong', 'hi', rend='bold')
        self._replace_tag('b', 'hi', rend='bold')
        self._replace_tag('sup', 'hi', rend='superscript')
        self._replace_tag('sub', 'hi', rend='subscript')
        self._replace_tag('small', 'hi', rend='smallcaps')
        for i in range(1, 7):
            self._replace_tag(f'h{i}', 'head')
        self._replace_tag('br', 'lb')
        self._replace_tag('ol', 'list')
        self._replace_tag('ul', 'list')
        self._replace_tag('li', 'item')
        self._replace_tag('blockquote', 'quote')
        for el in self.tree.xpath('//a'):
            el.tag = 'ref'
            target = el.attrib.pop('href', '')
            if target:
                el.attrib['target'] = target

        if self.indent:
            etree.indent(self.tree, space=indent_unit)

        new_text = etree.tostring(self.tree, encoding='unicode')

        if not self.with_root:
            # Remove wrapped root element
            new_text = re.sub(rf'^\s*<{root_tag}>|</{root_tag}>\s*$', '', new_text)
            if self.indent:
                new_text = new_text.replace('\n' + indent_unit, '\n')

        return new_text
