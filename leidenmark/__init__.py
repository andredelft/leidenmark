from markdown.extensions import Extension
from markdown import markdown

from dh_utils.tei.markdown import TEIPostprocessor

from .divisions import (
    DivisionsPreproc,
    DivisionMarkProcessor,
    DivisionMarkTreeproc,
    ColumnContainerTreeproc,
    TrivialProcessor,
    RemoveThrowaway
)
from .line_nums import LineNumsPreproc, NumberedBlocksProcessor
from .milestones import RE_MIL, MilestoneProcessor
from .gaps_spaces import (
    CompleteSquareBrackets,
    RE_SPACE, SpaceProcessor,
    RE_LINE_LOST, LineGapProcessor,
    RE_CHARACTER_LOST, CharacterLostProcessor,
    RE_CHARACTER_ILLEGIBLE, CharacterIllegibleProcessor
)
from .brackets import (
    RE_SUPPLIED, SuppliedProcessor,
    RE_ERASURE, ErasureProcessor
)
from .foreign import RE_FOREIGN, ForeignProcessor
from .misc import HetaProcessor, RE_HETA
from .exceptions import LeidenPlusSyntaxError


class LeidenPlus(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'strict' : [False, 'Toggle strict mode (omit all Markdown specific conventions)'],
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

        md.parser.blockprocessors.deregister('paragraph')
        md.parser.blockprocessors.register(TrivialProcessor(md.parser), 'fallback', 0)

        md.preprocessors.register(DivisionsPreproc(md), 'divison_preproc', 120)
        md.preprocessors.register(CompleteSquareBrackets(md), 'complete_square_brackets', 119)
        md.preprocessors.register(LineNumsPreproc(md), 'linenums_preproc', 118)
        md.parser.blockprocessors.register(NumberedBlocksProcessor(md.parser), 'lineblocks', 120)
        md.parser.blockprocessors.register(DivisionMarkProcessor(md.parser), 'divison_marks', 119)
        md.parser.blockprocessors.register(TrivialProcessor(md.parser), 'fallback', 0)
        md.inlinePatterns.register(MilestoneProcessor(RE_MIL, md), 'milestones', 120)
        md.inlinePatterns.register(SpaceProcessor(RE_SPACE, md), 'spaces', 119)
        md.inlinePatterns.register(LineGapProcessor(RE_LINE_LOST, md), 'line_gaps', 118)
        md.inlinePatterns.register(CharacterLostProcessor(RE_CHARACTER_LOST, md), 'character_lost', 117)
        md.inlinePatterns.register(ForeignProcessor(RE_FOREIGN, md), 'foreign', 116)
        md.inlinePatterns.register(ErasureProcessor(RE_ERASURE, md), 'erasure',  115)
        md.inlinePatterns.register(SuppliedProcessor(RE_SUPPLIED, md), 'supplied', 5)
        md.inlinePatterns.register(CharacterIllegibleProcessor(RE_CHARACTER_ILLEGIBLE, md), 'character_illegible', 4)
        md.inlinePatterns.register(HetaProcessor(RE_HETA, md), 'heta', 49) # After UnderscoreProcessor
        md.treeprocessors.register(DivisionMarkTreeproc(md), 'divison_treeproc', 120)
        md.treeprocessors.register(ColumnContainerTreeproc(md), 'col_container', 119)
        md.postprocessors.register(RemoveThrowaway(md), 'remove_throwaway', 1)
        md.postprocessors.register(TEIPostprocessor(md, configs['indent'], configs['with_root']), 'to_epidoc', 0)


class LeidenEscape(Extension):

    def extendMarkdown(self, md):
        md.postprocessors.register(TEIPostprocessor(md), 'to_xml', 0)


def leiden_plus(content, **kwargs):
    extensions = [LeidenPlus(**kwargs)]
    if not kwargs.get('strict', False):
        extensions.append('tables')
    return markdown(content, extensions=extensions)

def leiden_escape(content, **kwargs):
    return markdown(content, extensions = [LeidenEscape(**kwargs), 'tables'])
