from markdown.extensions import Extension

from .divisions import DivisionsPreproc, DivisionMarkProcessor, DivisionMarkTreeproc, TrivialProcessor
from .line_nums import LineNumsPreproc, NumberedBlocksProcessor
from .milestones import RE_MIL, MilestoneProcessor
from .gaps_spaces import RE_SPACE, SpaceProcessor, RE_LINE_GAP, LineGapProcessor, RE_CHARACTER_GAP, CharacterGapProcessor
from .to_xml import TEIPostprocesor
from .misc import HetaProcessor, RE_HETA


class LeidenPlus(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'strict' : [False, 'Toggle strict mode (omit all Markdown specific conventions)']
        }
        super(LeidenPlus, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        configs = self.getConfigs()

        md.parser.blockprocessors.deregister('paragraph')
        md.parser.blockprocessors.deregister('olist')
        if configs['strict']:
            md.inlinePatterns.deregister('em_strong')
            md.inlinePatterns.deregister('em_strong2')

        md.preprocessors.register(DivisionsPreproc(md), 'divison_preproc', 120)
        md.preprocessors.register(LineNumsPreproc(md), 'linenums_preproc', 119)
        md.parser.blockprocessors.register(NumberedBlocksProcessor(md.parser), 'lineblocks', 120)
        md.parser.blockprocessors.register(DivisionMarkProcessor(md.parser), 'divison_marks', 119)
        md.parser.blockprocessors.register(TrivialProcessor(md.parser), 'fallback', 0)
        md.inlinePatterns.register(MilestoneProcessor(RE_MIL, md), 'milestones', 120)
        md.inlinePatterns.register(SpaceProcessor(RE_SPACE, md), 'spaces', 119)
        md.inlinePatterns.register(LineGapProcessor(RE_LINE_GAP, md), 'line_gaps', 118)
        md.inlinePatterns.register(CharacterGapProcessor(RE_CHARACTER_GAP, md), 'character_gaps', 117)
        md.inlinePatterns.register(HetaProcessor(RE_HETA, md), 'heta', 49) # After UnderscoreProcessor
        md.treeprocessors.register(DivisionMarkTreeproc(md), 'divison_treeproc', 120)
        md.postprocessors.register(TEIPostprocesor(md), 'to_xml', 0)


class LeidenEscape(Extension):

    def extendMarkdown(self, md):
        md.postprocessors.register(TEIPostprocesor(md), 'to_xml', 0)

# TODO: Create Leiden+ escape possibility that works with inline escapes `<= Some content =>`{.leiden+} or blocks:
# ```leiden+
# <=
# Some content
# =>
# ```
