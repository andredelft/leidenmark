from markdown.postprocessors import Postprocessor
from lxml import etree
import re

class TEIPostprocesor(Postprocessor):

    def run(self, text):
        root_tag = 'root'
        indent_unit = '  '

        tree = etree.fromstring(f'<{root_tag}>{text}</{root_tag}>')

        # Replace some html:
        for el in tree.xpath('//em'):
            el.tag = 'hi'
            el.attrib['rend'] = 'italic'

        for el in tree.xpath('//strong'):
            el.tag = 'hi'
            el.attrib['rend'] = 'bold'

        etree.indent(tree, space = indent_unit)

        new_text = etree.tostring(tree, encoding = 'unicode')
        # Remove wrapped root element and remove one level of indentation
        new_text = re.sub(rf'</?{root_tag}>\s*|(?<=\n){indent_unit}', '', new_text)

        return new_text
