#!/usr/bin/python
# -*- coding: utf-8 -*-
from cg_graphics_audio import *
from cei2 import *
from details_form_personal import *
from details_form_faculty import *
from details_form_grades import *
from consent_form import ConsentForm
from framing_form import FramingForm
from learning_form import *
from final_form import FinalForm
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from curiosity_score import *
from kivy_communication import KL
from consent_form import *


# version 2.0

conditions = ['no_framing/no_stop', 'framing/no_stop', 'no_framing/stop', 'framing/stop']


class ZeroScreen(Screen):

    def on_enter(self, *args):
        KL.restart()

    def start(self):
        self.ids['subject_id'].bind(text=self.ids['subject_id'].on_text_change)


class FacultyGameApp(App):
    sm = None
    cg = None
    cf = None
    qf = None
    lf = None
    dfp = None
    dff = None
    dfg = None
    ff = None
    framing_form = None
    score = None
    float_layout = None

    cei2 = None
    bfi = None
    learn = None

    the_condition = ''
    # game_mode:
    #   True: game, no framing, no stop, no details
    #   False: Keren's study
    game_mode = True

    original_size = [1920, 1128]

    def build(self):
        # initialize logger
        self.init_communication()

        self.cg = CuriosityGame(self)
        self.cf = ConsentForm(self)
        self.framing_form = FramingForm(self)

        self.cei2 = CEI2('questions.json')
        self.bfi  = CEI2('more_questions.json')
        self.qf = []
        for p in range(0, len(self.cei2.page_dict)):
            self.qf.append(QuestionsForm(self, self.cei2.page_dict[p]))
        for p in range(0, len(self.bfi.page_dict)):
            self.qf.append(QuestionsForm(self, self.bfi.page_dict[p]))

        self.learn = Learning(self)
        self.lf = [LearningForm(self)]
        for i in range(1, self.learn.max_number_questions / self.lf[0].q_per_page):
            self.lf.append(LearningForm(self))

        self.dfp = DetailsFormPersonal(self)
        self.dff = DetailsFormFaculty(self)
        self.dfg = DetailsFormGrades(self)
        self.ff = FinalForm(self)

        self.score = CuriosityScore(self.cg.game_duration,
                                    len(self.cg.items),
                                    self.user_data_dir)

        self.sm = ScreenManager()

        if self.game_mode:
            screen = ZeroScreen()
            screen.start()
            screen.ids['subject_id'].bind(text=screen.ids['subject_id'].on_text_change)
            self.sm.add_widget(screen)
        else:
            screen = ConsentScreen(name='consent')
            screen.add_widget(self.cf)
            self.sm.add_widget(screen)

        if not self.game_mode:
            screen = Screen(name='framing')
            screen.add_widget(self.framing_form)
            self.sm.add_widget(screen)

        screen = Screen(name='thegame')
        screen.add_widget(self.cg.the_widget)
        self.sm.add_widget(screen)

        for kqf in range(0, len(self.qf)):
            screen = Screen(name="question"+str(kqf))
            screen.add_widget(self.qf[kqf])
            self.sm.add_widget(screen)

        for i, ilf in enumerate(self.lf):
            screen = Screen(name="learning_" + str(i))
            screen.add_widget(ilf)
            screen.bind(on_pre_enter=self.learn.start)
            self.sm.add_widget(screen)

        if not self.game_mode:
            screen = Screen(name="details_personal")
            screen.add_widget(self.dfp)
            self.sm.add_widget(screen)

            screen = DetailsScreenFaculty(name="details_faculty")
            screen.add_widget(self.dff)
            self.sm.add_widget(screen)

            screen = Screen(name="details_grades")
            screen.add_widget(self.dfg)
            self.sm.add_widget(screen)

        screen = Screen(name="final")
        screen.bind(on_enter=self.ff.start)
        screen.add_widget(self.ff)
        self.sm.add_widget(screen)

        if self.game_mode:
            self.sm.current = 'zero_screen'
        else:
            self.sm.current = 'consent'

        return self.sm

    def on_start(self):
        self.start()

    def start(self):
        self.cf.start(self)
        for qf in self.qf:
            qf.start()
        self.dfp.start()
        self.dff.start()
        self.dfg.start()
        self.score.init_score()

        self.choose_condition()

        if self.game_mode:
            self.sm.current = 'zero_screen'
        else:
            self.sm.current = 'consent'

    def choose_condition(self):
        if self.game_mode:
            self.the_condition = 'no_framing/no_stop'
        else:
            self.the_condition = random.choice(conditions)
        KL.log.insert(action=LogAction.data, obj='condition', comment=self.the_condition)

        self.framing_form.set_text(self.the_condition)
        self.cg.set_stop_button(self.the_condition)

    def on_pause(self):
        return True

    def init_communication(self):
        KC.start(the_ip='192.168.1.254', the_parents=[self])  # 127.0.0.1
        KL.start(mode=[DataMode.file], pathname=self.user_data_dir)

    def press_start(self, *args):
        self.cg.start()
        self.sm.current = self.sm.next()

if __name__ == '__main__':
    FacultyGameApp().run()

