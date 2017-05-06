# -*- coding: utf-8 -*-

import sys
import os

# TODO: find a solution for this hack
try:
    stdin, stdout = sys.stdin, sys.stdout
    reload(sys)
    sys.stdin, sys.stdout = stdin, stdout
    sys.setdefaultencoding('utf-8')
except Exception:
    pass

from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.listview import ListView, ListItemLabel
from kivy.adapters.simplelistadapter import SimpleListAdapter
#from kivy.core.window import Window
#Window.clearcolor = (1, 1, 1, 1)

from asian_word_analyzer.korean.word import KoreanWord as Word
from asian_word_analyzer.korean.db import DbUtil

folder = os.path.split(os.path.realpath(__file__))[0]
FONT = os.path.join(folder, 'fonts/wqy-microhei/wqy-microhei.ttc')



class BlockColumn(GridLayout):    
    def __init__(self, block, words):
        super(BlockColumn, self).__init__(cols=1)
        
        column_title = '[b][color=3333ff]{}[/color][/b]'.format(block.string)
        if block.ethym:
            column_title += '([color=3333ff]{}[/color])'.format(block.ethym)
        if block.name:
            column_title += ' - ' + block.name
        if block.meaning:
            column_title += ' - [color=3333ff]{}[/color]'.format(block.meaning)

        self.add_widget(Label(text=column_title, font_name=FONT, font_size=30, size_hint_y=0.1, markup=True))
                
        data = ['{} {}'.format(words.ix[word_idx].word, words.ix[word_idx].meaning)
                for word_idx in range(len(words))]
                    
        def args_converter(row_index, data_item):
            return {'text': data_item, 'font_name': FONT, 'size_hint_y': None, 'height' : 30}
                                                
        simple_list_adapter = SimpleListAdapter(data=data,
                                                args_converter=args_converter,
                                                cls=ListItemLabel)
        
        list_view = ListView(adapter=simple_list_adapter, height=500)

        self.add_widget(list_view)


def emphasize_part(input_str, idx, color='3333ff'):
    return '{}[color={}]{}[/color]{}'.format(input_str[:idx], 
                                             color, 
                                             input_str[idx:idx+1], 
                                             input_str[idx+1:])
    


class Columns(GridLayout):
    def __init__(self, text, **kwargs):
        super(Columns, self).__init__(size_hint_x=1, rows=2)
        self.current_block = 0
        self.carousel = Carousel(direction='right', size_hint_x=1, size_hint_y=1)
        self.carousel.bind(index=self.update_title)
        
        self.title_label = Label(font_name=FONT, markup=True,
                              font_size=30, size_hint_y=0.1)

        self.update_content(text)
        
        
    def update_title(self, *kwargs):
        if len(kwargs) > 0:
            self.current_block = kwargs[1] or 0
        title = emphasize_part(self.word.string, idx=self.current_block)
        ethym_str = ' ({})'.format(emphasize_part(self.word.ethym, idx=self.current_block)) if self.word.ethym else ''
        title += ethym_str 
        self.title_label.text = title
        
    def analyze(self, text):
        self.word = Word(text, compute_ethym=True)
        self.blocks = self.word.get_blocks_for_selected_meaning()

    
    def update_content(self, text):
        self.clear_widgets()
        self.carousel.clear_widgets()
        self.analyze(text)
        self.update_title()        
                        
        for block in self.blocks:
            words = DbUtil().get_words_with_block(block, exclude=self.word)
            self.carousel.add_widget(BlockColumn(block, words))

        self.add_widget(self.title_label)
        self.add_widget(self.carousel)



class AwaApp(App):
    def __init__(self, **kwargs):
        super(AwaApp, self).__init__(**kwargs)
        self.user_input = None
        
    def build(self):
        layout = GridLayout(rows=3)
        top_row = GridLayout(cols=2, size_hint_y=0.1)
        textinput = TextInput(text=u'남자', multiline=False, size_hint_x=0.8,
                              size_hint_y=0.1,
                              height=10,
                              font_name=FONT)
        button = Button(text='Analyze', font_size=50, font_name=FONT)        
        columns = Columns(textinput.text)

        def analyze(instance):
            columns.update_content(textinput.text)
                        
        button.bind(on_press=analyze) 
        textinput.bind(on_text_validate=analyze)        
                
        top_row.add_widget(textinput)
        top_row.add_widget(button)
        layout.add_widget(top_row)
        layout.add_widget(columns)
        return layout


AwaApp().run()
