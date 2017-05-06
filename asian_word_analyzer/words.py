
class AsianWord(object):
    language = None

    @property
    def meaning(self):
        """ Meaning getter """
        return self.meanings[self.selected_meaning]

    def get_blocks_for_selected_meaning(self):
        """ Getter for the blocks corresponding to the selected meaning """
        return self.blocks[self.selected_meaning]

    @property
    def ethym(self):
        return ''.join([block.ethym for block in self.blocks[self.selected_meaning] if block.ethym])

    def print_blocks_for_selected_meaning(self):
        """ This methods prints the block strings for the selected meaning.

        Example:
        --------
            For the word '안녕', the printed blocks will be ['안', '녕']
        """
        return [block.string for block in self.blocks[self.selected_meaning]]

