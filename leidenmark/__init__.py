from markdown.extensions import Extension
from markdown import markdown

from dh_utils.tei.markdown import TEIPostprocessor

from .divisions import register_divisions, deregister_paragraphs
from .line_nums import register_line_nums
from .milestones import register_milestones
from .gaps_spaces import register_gaps_spaces
from .brackets import register_brackets
from .foreign import register_foreign
from .glyphs import register_glyphs
from .misc import register_misc

__version__ = '0.2.2'


class LeidenPlus(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'strict': [
                False,
                'Toggle strict mode (omit all Markdown specific conventions)'
            ],
            'enable_paragraphs': [False, ''],
            'indent': [False, ''],
            'with_root': [False, '']
        }
        Extension.__init__(self, **kwargs)

    def extendMarkdown(self, md):
        configs = self.getConfigs()

        md.parser.blockprocessors.deregister('olist')
        if configs['strict']:
            md.inlinePatterns.deregister('em_strong')
            md.inlinePatterns.deregister('em_strong2')

        if not configs['enable_paragraphs']:
            deregister_paragraphs(md)

        register_divisions(md)
        register_milestones(md)
        register_line_nums(md)
        register_brackets(md)
        register_gaps_spaces(md)
        register_foreign(md)
        register_misc(md)
        register_glyphs(md)

        md.postprocessors.register(
            TEIPostprocessor(
                md, configs['indent'], configs['with_root']
            ), 'to_epidoc', 0
        )


class LeidenEscape(Extension):

    def extendMarkdown(self, md):
        md.postprocessors.register(TEIPostprocessor(md), 'to_xml', 0)


def leiden_plus(content, **kwargs):
    extensions = [LeidenPlus(**kwargs)]
    if not kwargs.get('strict', False):
        extensions.append('tables')
    return markdown(content, extensions=extensions)


def leiden_escape(content, **kwargs):
    return markdown(content, extensions=[LeidenEscape(**kwargs), 'tables'])
