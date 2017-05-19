import pandas as pd
import pytest

from asian_word_analyzer.korean.word import KoreanWord
from asian_word_analyzer.block import Block
import asian_word_analyzer.ui as ui


class TestUi:
    @staticmethod
    def korean_word():
        return KoreanWord(u'남대문', u'南大門',
                          u'(건축물) Namdaemun, the (Great) South Gate (of Seoul)')

    @staticmethod
    def block():
        return Block(u'안', u'安', u'편안할 안, 어찌 안', 'some meaning')

    def test_render_error(self):
        ui.render_error('some error')

    def test_render_debug(self, monkeypatch):
        monkeypatch.setattr('asian_word_analyzer.ui.DEBUG', True)
        ui.render_debug('some debug msg')

    def test_render_empty(self):
        ui.render_empty()

    def test_render_main(self):
        ui.render_main(self.korean_word())

    def test_render_block(self):
        words = [KoreanWord(string=u'남대문', etymology=u'南大門',
                            meaning=u'(건축물) Namdaemun, the (Great) South Gate (of Seoul)')]
        ui.render_block(self.block(), words)
