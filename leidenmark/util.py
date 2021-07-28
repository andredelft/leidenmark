class ContextInlineMixin:
    """
    A mixin for inline processors that obtains information about the element
    tree
    """

    def get_ancestors(self):
        try:
            inline_processor = self.md.treeprocessors['inline']
        except KeyError:
            raise KeyError(
                'InlineProcessor not found (ContextInlineMixin depends on it)'
            )
        else:
            return inline_processor.ancestors

    def in_leiden_plus(self):
        """
        Derives from the ancestors whether we are in a Leiden+ block
        (essentially an educated guess rn, perhaps we can make this more
        robust)
        """
        ancestors = self.get_ancestors()
        if not ancestors:
            return False
        else:
            # Perhaps we can make this more sophisticated in the future
            return ancestors[-1] == 'l' or 'ab' in ancestors
