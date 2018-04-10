#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import log
from kivy_communication.kivy_logger import *


class CuriosityScore:
    id = ''
    start = []
    game_sequence = []
    cei2 = {}
    max_duration = 0
    num_options = 0
    score = {}
    pathname = ''
    learning = {}

    def __init__(self, max_duration, num_options, pathname):
        self.max_duration = max_duration
        self.num_options = num_options
        self.pathname = pathname + '/'
        self.id = datetime.now()
        self.game_sequence = []
        self.cei2 = {}
        self.init_score()

    def init_score(self):
        self.score['age'] = ''
        self.score['gender'] = ''
        self.score['faculty'] = -1
        self.score['init'] = -1
        self.score['total_info'] = -1
        self.score['multi'] = -1
        self.score['stretching'] = -1
        self.score['embracing'] = -1
        self.score['learning'] = -1
        self.score['q_asked'] = -1

        self.cei2 = {}
        self.learning = {}
        self.game_sequence = []


    def start_game(self):
        self.init_score()
        self.start.append(datetime.now())   # for t0 index, sets the time the game started

    def add_game_item_begin(self, item):
        self.game_sequence.append([item, datetime.now()])
        if len(self.start) == 1:    # for t0 index, if this is the first interaction, add the time
            self.start.append(datetime.now())
            KivyLogger.insert(action=LogAction.data, obj='t0',
                              comment=self.start[0].strftime('%Y_%m_%d_%H_%M_%S_%f') + ',' +
                              self.start[1].strftime('%Y_%m_%d_%H_%M_%S_%f'))

    def add_game_item_end(self, item):
        for i in self.game_sequence:
            if i[0] == item and len(i) == 2:
                i.append(datetime.now())
                i.append((i[2]-i[1]).seconds)
                i.append(i[3] / float(self.max_duration))
        self.calculate_score()

    def set_cei2(self, ans):
        for k,v in ans.items():
            self.cei2[k] = v
        self.calculate_score()

    def learning_add(self, question, answer):
        self.learning[question] = answer
        self.calculate_score()

    def add_details(self, details):
        for dk, dv in details.items():
            self.score[dk] = dv
        self.save()

    def print_me(self):
        for i in self.game_sequence:
            print(i[0], i[3], i[4])
        print(self.cei2)


    def calculate_score(self):
        # initial exploration
        init_exploration = 0
        if len(self.start) == 2:
            init_exploration = (self.start[1] - self.start[0]).seconds
        self.score['init'] = init_exploration

        # total listening time
        total_info = 0
        for i in self.game_sequence:
            total_info += i[4]
        self.score['total_info'] = total_info

        # multi-disciplinary, entropy
        multidisciplinary = 0
        if total_info > 0:
            prob = {}
            for i in self.game_sequence:
                if i[0] not in prob:
                    prob[i[0]] = i[4]
                else:
                    prob[i[0]] += i[4]
            for pk, pv in prob.items():
                p = pv / total_info
                multidisciplinary += p * log(p,2)
        self.score['multi'] = -multidisciplinary / log(self.num_options, 2)

        # cei2
        stretching = 0
        embracing = 0
        for ck, cv in self.cei2.items():
            if ck in ['q01', 'q03', 'q05', 'q07', 'q09']:
                print("stretching: ", cv, cv[3])
                stretching += int(cv[3])
            else:
                print("embracing: ", cv, cv[3])
                embracing += int(cv[3])
        self.score['stretching'] = stretching
        self.score['embracing'] = embracing

        # learning
        print(self.learning)
        learning = 0
        q_asked = 0
        for lk, lv in self.learning.items():
            q_asked += 1
            if lv == 'correct':
                learning += 1
        self.score['learning'] = learning
        self.score['q_asked'] = q_asked

        print(self.score)
        self.save()

    def save(self):
        store = JsonStore(self.pathname + 'CuriosityScore.txt')
        store.put(self.id.strftime('%Y_%m_%d_%H_%M_%S_%f'),
                  init=self.score['init'],
                  total=self.score['total_info'],
                  multi=self.score['multi'],
                  stretching=self.score['stretching'],
                  embracing=self.score['embracing'],
                  age=self.score['age'],
                  gender=self.score['gender'],
                  faculty=self.score['faculty'])

    def draw(self):
        pass
    # Ellipse:
    #             pos: 100, 100
    #             size: 200 * wm.value, 201 * hm.value
    #             source: 'data/logo/kivy-icon-512.png'
    #             angle_start: e1.value
    #             angle_end: e2.value



