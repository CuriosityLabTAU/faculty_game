#!/usr/bin/python
# -*- coding: utf-8 -*-
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.utils import get_color_from_hex
from hebrew_management import HebrewManagement
from kivy_communication.logged_widgets import *
from kivy.storage.jsonstore import JsonStore


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


class FramingForm(BoxLayout):
    title=ObjectProperty()
    framing_text=ObjectProperty()
    button=ObjectProperty()
    the_app = None
    dict = None
    body_labels = None

    def __init__(self, the_app):
        super(FramingForm, self).__init__()
        self.the_app = the_app
        self.button.text = u'ךשמה'
        self.framing_text.text = u'םולש'

    def start(self, the_app):
        self.button.disabled = True
        self.button.background_color = (0, 0.71, 1, 1)

    def contin(self):
        # the next screen is the game
        # start the clock and then transition
        if not self.the_app.game_mode:
            self.the_app.cg.start()
        self.the_app.sm.current = self.the_app.sm.next()

    def get_color_from_hex(self, color):
        return get_color_from_hex(color)

    def set_text(self, the_condition):
        if 'no_framing' in the_condition:
            self.framing_text.text = u'אבה ךסמל ךשמה'
        else:
            self.framing_text.text = u'תונרקס ךסמל ךשמה'
