from markdown.extensions import Extension

from .divisions import DivisionsPreproc, DivisionMarkProcessor, DivisionMarkTreeproc
from .line_nums import LineNumsPreproc, NumberedBlocksProcessor
from .milestones import RE_MIL, MilestoneProcessor
from .gaps_spaces import RE_SPACE, SpaceProcessor, RE_LINE_GAP, LineGapProcessor, RE_CHARACTER_GAP, CharacterGapProcessor


class LeidenPlus(Extension):

    def extendMarkdown(self, md):
        md.preprocessors.register(DivisionsPreproc(md), 'divison_preproc', 50)
        md.preprocessors.register(LineNumsPreproc(md), 'linenums_preproc', 49)
        md.parser.blockprocessors.register(NumberedBlocksProcessor(md.parser), 'lineblocks', 50)
        md.parser.blockprocessors.register(DivisionMarkProcessor(md.parser), 'divison_marks', 49)
        md.inlinePatterns.register(MilestoneProcessor(RE_MIL, md), 'milestones', 50)
        md.inlinePatterns.register(SpaceProcessor(RE_SPACE, md), 'spaces', 49)
        md.inlinePatterns.register(LineGapProcessor(RE_LINE_GAP, md), 'line_gaps', 48)
        md.inlinePatterns.register(CharacterGapProcessor(RE_CHARACTER_GAP, md), 'character_gaps', 47)
        md.treeprocessors.register(DivisionMarkTreeproc(md), 'divison_treeproc', 50)


# TODO: Create Leiden+ escape possibility that works with inline escapes `<= Some content =>`{.leiden+} or blocks:
# ```leiden+
# <=
# Some content
# =>
# ```

# class LeidenEscape(Extension):
#     pass
