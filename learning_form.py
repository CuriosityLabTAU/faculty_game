#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.graphics import *
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy_communication.logged_widgets import *
import random


class Learning():
    the_app = None
    questions = []
    page_questions = []

    max_number_questions = 10

    def __init__(self, the_app):
        self.the_app = the_app

        if self.the_app.game_mode:
            self.the_next_page = 'final'
        else:
            self.the_next_page = "details_personal"

    def start(self, pars):
        cg = self.the_app.cg.items
        sequence = self.the_app.score.game_sequence

        s_iter = {}
        self.questions = []
        for s in sequence:
            s_name = s[0]
            if s_name in s_iter:
                s_iter[s_name] = s_iter[s_name] + 1
            else:
                s_iter[s_name] = 1
            if s_iter[s_name] in cg[s_name].question:
                # there is a question for the item
                q = {}
                q = cg[s_name].question[s_iter[s_name]]
                q['name'] = s_name + "_" + str(s_iter[s_name])
                self.questions.append(q)

        q_per_page = 2
        k_page_ques = 0
        self.page_questions = []
        for q in self.questions:
            if k_page_ques == 0:
                new_page = []

            a_question = {}
            a_question['question'] = {'text': q['question'], 'name': q['name']}
            answer_list = [{'text': q['correct'], 'name': 'correct'},
                           {'text': q['wrong1'], 'name': 'wrong1'},
                           {'text': q['wrong2'], 'name': 'wrong2'},
                           {'text': q['wrong3'], 'name': 'wrong3'}]
            answer_sequence = [0,1,2,3]
            random.shuffle(answer_sequence)
            a_question['answers'] = []
            for a in answer_sequence:
                a_question['answers'].append(answer_list[a])

            new_page.append(a_question)

            k_page_ques += 1
            if k_page_ques == q_per_page:
                self.page_questions.append(new_page)
                k_page_ques = 0

        if len(self.page_questions) == 0:
            self.the_app.sm.current = self.the_next_page
        for i, ifl in enumerate(self.the_app.lf):
            if i == (len(self.page_questions)-1):
                ifl.next_page = self.the_next_page
                ifl.start(self.page_questions[-1])
            elif i < len(self.page_questions):
                if i < (len(self.the_app.lf) - 1):
                    ifl.next_page = "learning_" + str(i+1)
                else:
                    ifl.next_page = self.the_next_page
                ifl.start(self.page_questions[i])


class LearningForm(BoxLayout):
    answers = []
    the_app = None
    labels = []
    q_per_page = 2
    ans_per_q = 4
    next_page = None

    def __init__(self, app):
        super(LearningForm, self).__init__()
        self.the_app = app
        with self.canvas.before:
            self.rect = Rectangle(source='back3.png')
            self.bind(size=self._update_rect, pos=self._update_rect)

        self.labels = []
        for q in range(0, self.q_per_page):
            q_labels = {}
            q_labels['question'] = Label(font_size=40, font_name="fonts/the_font.ttf",
              halign='right', size_hint_y=0.4,size_hint_x=1.5,
              color=[0,0,0,1])
            q_labels['answers'] = []
            for a in range(0, self.ans_per_q):
                q_labels['answers'].append(Label(font_size=32, font_name="fonts/the_font.ttf",
                      halign='right', size_hint_y=0.4,size_hint_x=1.5,
                      color=[0,0,0,1]))
            self.labels.append(q_labels)

        layoutup = BoxLayout(orientation='vertical')
        layoutup.add_widget(BoxLayout(size_hint_y=2))
        text = u"מה למדת?"
        layoutup.add_widget(
            Label(text=text[::-1],
                  font_size=50, font_name="fonts/the_font.ttf",
                  halign='right', size_hint_y=0.4,size_hint_x=1.5,
                  color=[0,0,0,1]))
        layoutup.add_widget(BoxLayout(size_hint_y=1))

        text = u"ענה על השאלות הבאות לפי מה ששמעת."
        layoutup.add_widget(
            Label(text=text[::-1],
                  font_name="fonts/the_font.ttf", font_size=36, halign='right',
                  size_hint_y=0.2,
                  color=[0,0,0,1]))
        layoutup.add_widget(BoxLayout(size_hint_y=0.2))

        self.answers = []
        for q in range(0, self.q_per_page):
            q_layout = BoxLayout()
            q_layout.add_widget(self.labels[q]['question'])
            q_layout.add_widget(BoxLayout(size_hint_x=0.2))
            layoutup.add_widget(q_layout)

            answer_list = []
            for a in range(0, self.ans_per_q):
                answer = AnswerButton(size_hint_x=0.15,
                                  text="", group=str(q))
                answer.form = self
                answer_list.append(answer)
            self.answers.append(answer_list)
            for a in range(0, self.ans_per_q):
                q_layout = BoxLayout(size_hint_y=0.5)
                q_layout.add_widget(BoxLayout(size_hint_x=0.8))
                q_layout.add_widget(self.labels[q]['answers'][a])
                q_layout.add_widget(self.answers[q][a])
                q_layout.add_widget(BoxLayout(size_hint_x=0.8))
                layoutup.add_widget(q_layout)

        layoutup.add_widget(BoxLayout(size_hint_y=0.2))

        layoutbuttons = BoxLayout(size_hint_y=0.5)
        text = u"המשך"
        self.next_button = Button(on_press=self.next,
                                  background_color=(0, 0.71, 1., 1),
                                  background_normal="",
                                  size_hint_x=0.3,
                                  text=text[::-1],
                                  font_name="fonts/the_font",
                                  font_size=20,
                                  disabled=True)

        layoutbuttons.add_widget(BoxLayout(size_hint_x=0.2))
        layoutbuttons.add_widget(self.next_button)
        layoutbuttons.add_widget(BoxLayout())
        layoutbuttons.add_widget(BoxLayout(size_hint_x=0.7))

        layoutup.add_widget(layoutbuttons)
        layoutup.add_widget(BoxLayout(size_hint_y=0.3))
        self.add_widget(layoutup)

    def start(self, questions):
        for q in range(0, self.q_per_page):
            self.labels[q]['question'].text = questions[q]['question']['text'][::-1]
            for a in range(0, self.ans_per_q):
                self.labels[q]['answers'][a].text = questions[q]['answers'][a]['text'][::-1]
                self.answers[q][a].question = questions[q]['question']['name'] # the actual question
                self.answers[q][a].answer = questions[q]['answers'][a]['name'] # 'correct' / 'wrong'
                self.answers[q][a].name = self.answers[q][a].answer + ',' + self.answers[q][a].question

    def next(self, pars):
        self.the_app.sm.current = self.next_page

    def set_answer(self, question, answer):
        self.the_app.score.learning_add(question, answer)
        selected = 0
        for q in range(0, self.q_per_page):
            for a in range(0, self.ans_per_q):
                a_button = self.answers[q][a]
                if a_button.active:
                    selected += 1
        self.next_button.disabled = (selected < self.q_per_page)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

