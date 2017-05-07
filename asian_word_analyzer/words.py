
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
    def etymology(self):
        return ''.join([block.etymology for block in self.blocks[self.selected_meaning]
                        if block.etymology])

