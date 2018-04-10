#!/usr/bin/python
# -*- coding: utf-8 -*-

from kivy.graphics import Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy_communication.logged_widgets import *
from kivy.storage.jsonstore import JsonStore
from kivy.uix.screenmanager import Screen


class DetailsScreenFaculty(Screen):

    def add_widget(self, widget, index=0):
        super(Screen, self).add_widget(widget, index)
        self.bind(on_enter=widget.on_enter)


class DetailsFormFaculty(BoxLayout):
    details = {}
    the_app = None
    faculty_spinner = None
    first_update = True

    def __init__(self, the_app):
        super(DetailsFormFaculty, self).__init__()
        self.the_app = the_app

        with self.canvas.before:
            self.rect = Rectangle(source='back3.png')
            self.bind(size=self._update_rect, pos=self._update_rect)

        dict = {}
        self.answers = {}
        store = JsonStore('details.json').get('details')

        for key, value in store.items():
            if key in ['FirstName', 'LastName', 'Email', 'end_button','details_title','Age']:
                dict[key] = value[::-1]
            if key in ['Gender','Faculty']:
                dict[key] = {}
                for kqa, qa in value.items():
                    if kqa=='text':
                        dict[key][kqa] = qa[::-1]
                    elif kqa == 'default':
                        dict[key][kqa] = qa[::-1]
                    elif kqa != 'ages':
                        dict[key][kqa]=[]
                        for k,v in value[kqa].items():
                           dict[key][kqa].append(v[::-1])
                    else:
                        dict[key][kqa]=[]
                        age=10
                        while age<100:
                            dict[key][kqa].append(str(age))
                            age += 1

        # definitions of all the GUI
        y_size = 0.2

        temp_faculty = []
        for f in range(len(dict['Faculty']['Faculties'])):
            if f == 0:
                temp_faculty.append(dict['Faculty']['Faculties'][4])
            elif f == 4:
                temp_faculty.append(dict['Faculty']['Faculties'][0])
            else:
                temp_faculty.append(dict['Faculty']['Faculties'][f])
        dict['Faculty']['Faculties'] = temp_faculty

        self.faculty_default = dict['Faculty']['default']

        # faculty spinner
        self.faculty_spinner_1st = LoggedSpinner(text=dict['Faculty']['default'],
            values=dict['Faculty']['Faculties'],
            size=(50, 50),
            font_name="fonts/the_font.ttf",
            font_size=30,
            option_cls=MySpinnerOption,
            size_hint_y=y_size)
        self.faculty_spinner_1st.name = 'faculty_1st'
        self.faculty_spinner_1st.bind(text=self.faculty_spinner_1st.on_spinner_text)

        self.faculty_spinner_2nd = LoggedSpinner(text=dict['Faculty']['default'],
            values=dict['Faculty']['Faculties'],
            size=(50, 50),
            font_name="fonts/the_font.ttf",
            font_size=30,
            option_cls=MySpinnerOption,
            size_hint_y=y_size)
        self.faculty_spinner_2nd.name = 'faculty_2nd'
        self.faculty_spinner_2nd.bind(text=self.faculty_spinner_2nd.on_spinner_text)

        self.faculty_spinner_3rd = LoggedSpinner(text=dict['Faculty']['default'],
            values=dict['Faculty']['Faculties'],
            size=(50, 50),
            font_name="fonts/the_font.ttf",
            font_size=30,
            option_cls=MySpinnerOption,
            size_hint_y=y_size)
        self.faculty_spinner_3rd.name = 'faculty_3rd'
        self.faculty_spinner_3rd.bind(text=self.faculty_spinner_3rd.on_spinner_text)

        end_button = Button(background_color=[0, 0.71, 1, 1],
                            background_normal="",
                            text=dict['end_button'], font_size=30,
                            font_name="fonts/the_font.ttf",
                            halign='right', on_press=self.next)

        end_button.bind(on_press=self.save)  # layout of the GUI

        layoutup = BoxLayout(orientation='vertical')
        layoutup.add_widget(BoxLayout(size_hint_y=y_size))
        layoutup.add_widget(
             Label(text=dict['details_title'], 
                   font_size=50, font_name="fonts/the_font.ttf",
                   halign='right', size_hint_y=y_size,
                   color=[0,0,0,1]))

        layout = GridLayout(cols=8, rows=6)

        # === first line ===
        layout.add_widget(end_button)
        layout.add_widget(BoxLayout(size_hint_x=0.1, size_hint_y=y_size))

        layout.add_widget(self.faculty_spinner_3rd)
        layout.add_widget(
            Label(text=u'תישילש תופידע',
                  font_size=30, font_name="fonts/the_font.ttf",
                  halign='right', size_hint_x=1.5,
                  color=[0, 0, 0, 1]))

        layout.add_widget(self.faculty_spinner_2nd)
        layout.add_widget(
            Label(text=u'הינש תופידע',
                  font_size=30, font_name="fonts/the_font.ttf",
                  halign='right', size_hint_x=1.5,
                  color=[0, 0, 0, 1]))

        layout.add_widget(self.faculty_spinner_1st)
        layout.add_widget(
            Label(text=dict['Faculty']['text'],
                  font_size=30, font_name="fonts/the_font.ttf",
                  halign='right', size_hint_x=1.5,
                  color=[0, 0, 0, 1]))

    # === second line ===
        layout.add_widget(BoxLayout(size_hint_y=y_size))
        layout.add_widget(BoxLayout(size_hint_x=0.1, size_hint_y=y_size))
        layout.add_widget(BoxLayout())
        layout.add_widget(BoxLayout(size_hint_y=y_size))

        layout.add_widget(BoxLayout())
        layout.add_widget(BoxLayout())
        layout.add_widget(BoxLayout(size_hint_x=1.5))
        layout.add_widget(BoxLayout(size_hint_x=1.5))

        # === space lines ===
        for lines in range(2):
            for space_line in range(8):
                layout.add_widget(BoxLayout(size_hint_x=0.1, size_hint_y=1))
                # layout.add_widget(BoxLayout(size_hint_y=1))

        # === last line ===
        layout.add_widget(BoxLayout(size_hint_x=0.2))
        layout.add_widget(BoxLayout(size_hint_x=0.1, size_hint_y=y_size))
        layout.add_widget(BoxLayout())

        layout.add_widget(BoxLayout(size_hint_x=0.2))

        layout.add_widget(
            Label(text="ךתופתתשה לע הדות", font_size=36,
                  color=[0, 0, 0, 1],
                  font_name="fonts/the_font.ttf", halign='right', size_hint_x=1.5))

        layout.add_widget(BoxLayout())
        layout.add_widget(BoxLayout())

        # === space lines ===
        for lines in range(1):
            for space_line in range(7):
                layout.add_widget(BoxLayout(size_hint_x=0.1, size_hint_y=1))
                # layout.add_widget(BoxLayout(size_hint_y=1))
        # ======= end =======

        layoutup.add_widget(layout)
        self.add_widget(layoutup)

    def start(self):
        if self.first_update:
            self.first_update = False
            dx = float(self.the_app.sm.size[0]) / float(self.the_app.original_size[0])
            dy = float(self.the_app.sm.size[1]) / float(self.the_app.original_size[1])
            text_based_widgets = [Label, LoggedSpinner, LoggedTextInput]
            for l1 in self.children:
                if type(l1) in text_based_widgets:
                    l1.font_size = int(l1.font_size * dx)
                    l1.size_hint_y *= dy
                else:
                    for l2 in l1.children:
                        if type(l2) in text_based_widgets:
                            l2.font_size = int(l2.font_size * dx)
                            l2.size_hint_y *= dy
                        else:
                            for l3 in l2.children:
                                if type(l3) in text_based_widgets:
                                    l3.font_size = int(l3.font_size * dx)
                                    l3.size_hint_y *= dy
    def on_enter(self, *args):
        self.faculty_spinner_1st.text = self.faculty_default
        self.faculty_spinner_2nd.text = self.faculty_default
        self.faculty_spinner_3rd.text = self.faculty_default


    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def justify_hebrew(self, instance, value):
        print("justify hebrew", instance, value)
        if len(value) > 0:
            if len(instance.the_text) != len(value):
                instance.the_text = value
                instance.text = value[-1] + instance.the_text[:-1]

    def save(self, instance):
        details = {'faculty_1st': self.faculty_spinner_1st.text,
                   'faculty_2nd': self.faculty_spinner_2nd.text,
                   'faculty_3rd': self.faculty_spinner_3rd.text}
        self.the_app.score.add_details(details)

    def next(self, pars):
        self.the_app.sm.current = self.the_app.sm.next()