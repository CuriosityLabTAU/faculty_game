#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.utils import get_color_from_hex
from hebrew_management import HebrewManagement
from kivy_communication.logged_widgets import *
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen


class ConsentScreen(Screen):

    def add_widget(self, widget, index=0):
        super(Screen, self).add_widget(widget, index)


class ConsentCheckBox(LoggedCheckBox):
    the_form = None

    def on_press(self, *args):
        super(ConsentCheckBox, self).on_press(*args)
        if self.the_form:
            self.the_form.mark_checkbox()


class ConsentButton(LoggedButton):
    the_form = None

    def on_press(self, *args):
        super(ConsentButton, self).on_press(*args)
        if self.the_form:
            self.the_form.contin()


class ConsentForm(BoxLayout):
    title=ObjectProperty()
    body=ObjectProperty()
    checkbox_agree=ObjectProperty()
    checkbox_txt=ObjectProperty()
    button=ObjectProperty()
    the_app = None
    dict = None
    body_labels = None

    def __init__(self, the_app):
        super(ConsentForm, self).__init__()
        self.the_app = the_app
        self.dict = {'title':self.title,
                'body':self.body,
                'checkbox_txt':self.checkbox_txt,
                'button':self.button}
        store = JsonStore('consent_form.json').get('agreement')
        for key, value in store.items():
            self.dict[key].text = value[::-1]

        self.body_labels = []
        txt = self.dict['body'].text
        new_lines = HebrewManagement.multiline(txt, 50)
        for nl in new_lines[::-1]:
            self.body_labels.append(Label(text=nl,
                      font_name="fonts/the_font",
                      font_size=36,
                      color=[0,0,0,1]))
            self.dict['body'].add_widget(self.body_labels[-1])


    def start(self, the_app):
        self.button.disabled = True
        self.checkbox_agree.active = False
        self.button.background_color = (0, 0.71, 1, 1)
        for l in self.dict['body'].children:
            l.font_size = int(36.0 * float(self.the_app.sm.size[0]) / float(self.the_app.original_size[0]))

    def contin(self):
        if self.checkbox_agree.active:
            self.the_app.sm.current = self.the_app.sm.next()
        else:
            print("pls mark checkbox")

    def mark_checkbox(self):
        if self.checkbox_agree.active:
            self.button.background_color = (0, 0.71, 1, 1)
            # self.button.background_color = (0.71, 0, 1., 1)
            self.button.disabled = False
        else:
            self.button.disabled = True

    def get_color_from_hex(self, color):
        return get_color_from_hex(color)

