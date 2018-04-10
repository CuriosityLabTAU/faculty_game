#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.graphics import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
import collections
from kivy_communication.logged_widgets import *
from kivy.storage.jsonstore import JsonStore


class CEI2():
    dict = None
    page_dict = None

    def __init__(self, question_filename='question.json'):
        self.dict = {'q_in_page': [], 'qu_title': "", 'qu_description': "", 'ques': {},
                'ans': {}, 'next_button': "", 'prev_button': ""}
        store = JsonStore(question_filename, encoding='utf-8').get('questionnaire')

        for key, value in store.items():
            if key in ['qu_title', 'next_button', 'prev_button', 'questions']:
                self.dict[key] = value[::-1]
            if key in ['qu_description', 'ques', 'ans']:
                self.dict[key] = {}
                for kqa, qa in value.items():
                    self.dict[key][kqa] = qa[::-1]
            if key in ['q_in_page']:
                self.dict[key] = int(value)

        self.dict['ques'] = collections.OrderedDict(sorted(self.dict['ques'].items()))
        self.dict['ans'] = collections.OrderedDict(sorted(self.dict['ans'].items()))

        k_page = 0
        k_page_ques = 0
        self.page_dict = []
        for k, v in self.dict['ques'].items():
            if k_page_ques == 0:
                page_questions = {}
            page_questions[k] = v
            k_page_ques += 1
            if k_page_ques == self.dict['q_in_page']:
                new_page = {}
                new_page['ques'] = page_questions
                new_page = collections.OrderedDict(sorted(new_page.items()))
                self.page_dict.append(new_page)
                k_page_ques = 0

        for pd in self.page_dict:
            for k,v in self.dict.items():
                if k != 'ques':
                    pd[k] = v


class QuestionsForm(BoxLayout):
    answers = {}
    ans_button = []
    the_app = None
    questions = {}
    next_button = None
    num_pages = 1
    first_update = True

    def __init__(self, app, dict):
        super(QuestionsForm, self).__init__()
        self.the_app = app
        with self.canvas.before:
            self.rect = Rectangle(source='back4.png')
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.answers = {}
        self.questions = dict['ques']
        num_questions = len(dict['ques'].keys())

        layoutup = BoxLayout(orientation='vertical')
        layoutup.add_widget(BoxLayout(size_hint_y=0.7))
        layoutup.add_widget(
            Label(text=dict['qu_title'],
                  font_size=50, font_name="fonts/the_font.ttf",
                  halign='right', size_hint_y=0.4,size_hint_x=1.5,
                  color=[0,0,0,1]))
        layoutup.add_widget(BoxLayout(size_hint_y=0.1))
        layoutup.add_widget(
            Label(text=dict['qu_description']['d1'],
                  font_name="fonts/the_font.ttf", font_size=36, halign='right',
                  size_hint_y=0.15,
                  color=[0,0,0,1]))
        layoutup.add_widget(
            Label(text=dict['qu_description']['d2'],
                  font_name="fonts/the_font.ttf", font_size=36, halign='right',
                  size_hint_y=0.15,
                  color=[0,0,0,1]))
        layoutup.add_widget(
            Label(text=dict['qu_description']['d3'],
                  font_name="fonts/the_font.ttf", font_size=36, halign='right',
                  size_hint_y=0.15,
                  color=[0,0,0,1]))
        layoutup.add_widget(BoxLayout(size_hint_y=0.2))

        # question matrix
        layout = GridLayout(cols=len(dict['ans']) + 2,
                            rows=len(dict['ques']) + 1,
                            row_default_height=400 / num_questions)

        dict['ques'] = collections.OrderedDict(sorted(dict['ques'].items()))

        q_counter = 0
        for ques, values in dict['ques'].items():
            layout.add_widget(BoxLayout(size_hint_x=0.05))
            q_counter += 1
            if q_counter == 1:
                for ans in dict['ans']:
                    layout.add_widget(
                        Label(size_hint_x=0.1,
                              text=dict['ans'][ans],
                              font_name="fonts/the_font.ttf",
                              font_size=25,
                              halign='right',
                              color=[0,0,0,1]))
                layout.add_widget(
                    Label(text="תולאש",
                          font_name="fonts/the_font.ttf",
                          font_size=42,
                          halign='right', orientation='vertical',
                          color=[0,0,0,1]))
                layout.add_widget(BoxLayout(size_hint_x=0.1, name='space_between'))

            for ans in dict['ans']:
                ab = AnswerButton(size_hint_x=0.15,
                                  text="", group=str(q_counter))
                ab.name = str(ques) + "," + str(ans)
                ab.question = ques
                ab.answer = ans
                ab.form = self
                self.ans_button.append(ab)
                layout.add_widget(ab)

            # CHECK ID AND KEEP THE CLICK VALUE
            layout.add_widget(
                Label(halign='right', text=dict['ques'][ques],
                      font_name="fonts/the_font.ttf", orientation='vertical',
                      font_size=36,
                      color=[0,0,0,1]))

        layoutup.add_widget(layout)
        layoutup.add_widget(BoxLayout())
        layoutbuttons = BoxLayout(size_hint_y=0.2)
        self.next_button = Button(on_press=self.next,
                                  background_color=(0, 0.71, 1., 1),
                                  background_normal="",
                                  size_hint_x=0.3,
                                  text=dict['next_button'],
                                  font_name="fonts/the_font",
                                  font_size=20,
                                  disabled=True)

        layoutbuttons.add_widget(BoxLayout(size_hint_x=0.2))
        layoutbuttons.add_widget(self.next_button)
        layoutbuttons.add_widget(BoxLayout())
        layoutbuttons.add_widget(BoxLayout(size_hint_x=0.7))

        layoutup.add_widget(layoutbuttons)
        layoutup.add_widget(BoxLayout(size_hint_y=0.1))
        self.add_widget(layoutup)

    def start(self):
        if self.first_update:
            self.first_update = False
            dx = float(self.the_app.sm.size[0]) / float(self.the_app.original_size[0])
            dy = float(self.the_app.sm.size[1]) / float(self.the_app.original_size[1])
            for l1 in self.children:
                if type(l1) is Label:
                    l1.font_size = int(l1.font_size * dx)
                else:
                    for l2 in l1.children:
                        if type(l2) is Label:
                            l2.font_size = int(l2.font_size * dx)
                        elif type(l2) is GridLayout:
                            l2.row_default_height *= dy
                            for l3 in l2.children:
                                if type(l3) is Label:
                                    l3.font_size = int(l3.font_size * dx)

        for b in self.ans_button:
            b.active = False
        self.next_button.disabled = True

    def set_answer(self, question, answer):
        self.answers[question] = answer
        all_answered = True
        for qk,qv in self.questions.items():
            if qk not in self.answers:
                all_answered = False
        if all_answered:
            self.next_button.disabled = False

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def next(self, pars):
        self.the_app.score.set_cei2(self.answers)
        self.the_app.sm.current = self.the_app.sm.next()
