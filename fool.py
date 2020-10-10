import pygame
import random
from collections import defaultdict

import config as c
from game import Game
from game_objects.button import Button

from game_objects.deck import Deck
from game_objects.player import Player
from game_objects.table import Table
from game_objects.hand import Hand


class Fool(Game):
    def __init__(self):
        Game.__init__(self, 'Дурак', c.screen_width,  c.screen_height, c.menu_background, c.icon, c.frame_rate)
        self.pause = False
        self.mode = None
        self.menu_buttons = []
        self.create_main_menu()

        self.user_attack = random.choice((True, True))
        self.deck = None
        self.user = None
        self.bot = None
        self.table = None

        self.selected_cards = []

        self.timers = dict()

    def clear(self):
        self.objects = []
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_button_handlers = []
        self.mouse_motion_handlers = []

    def create_small_menu(self):
        pass

    def create_main_menu(self):
        def on_play_algo(button):
            self.clear()
            self.create_game('algo')

        def on_play_ai(button):
            pass

        def on_quit(button):
            self.running = False

        self.background_image = c.menu_background
        for i, (text, click_handler) in enumerate((('Играть с алгоритмом', on_play_algo), 
                                                   ('Играть с ИИ', on_play_ai),
                                                   ('Выйти', on_quit))):
            b = Button(c.main_menu_offset_x,
                       c.main_menu_offset_y + (c.main_menu_button_h + 5) * i,
                       c.main_menu_button_w,
                       c.main_menu_button_h,
                       text,
                       click_handler,
                       padding=5)
            self.objects.append(b)
            self.mouse_button_handlers.append(b.handle_mouse_button_event)
            self.mouse_motion_handlers.append(b.handle_mouse_motion)

    def create_game(self, mode='algo'):
        self.background_image = c.game_background

        self.deck = Deck()
        self.user = Player(Hand(self.deck.give_cards()))
        self.bot = Player(Hand(self.deck.give_cards(), False), False)

        self.objects.append(self.deck)
        self.objects.append(self.user.hand)
        self.objects.append(self.bot.hand)
        # for card in self.user.hand:
        #     self.objects.append(card)
        # for card in self.bot.hand:
        #     self.objects.append(card)

        if self.user_attack:
            self.mouse_motion_handlers.append(self.user.hand.handle_mouse_motion)
            self.mouse_button_handlers.append(self.user.hand.handle_mouse_button_event)
            for card in self.user.hand:
                self.mouse_button_handlers.append(card.handle_button_mouse_event)
                self.mouse_motion_handlers.append(card.handle_mouse_motion)

#
    # def handle_mouse_event(self, type, pos):
    #     if type == pygame.MOUSEMOTION:
    #         self.handle_mouse_move(pos)
    #     elif type == pygame.MOUSEBUTTONUP:
    #         self.handle_mouse_up(pos)
    #     elif type == pygame.MOUSEBUTTONDOWN:
    #         self.handle_mouse_down(pos)
#
    # def handle_mouse_move(self, pos):
    #     if len(self.selected_cards) != 0:
    #         if self.selected_nominal_has_more_twins():
    #             pass
#
    # def handle_mouse_up(self, pos):
    #     if len(self.selected_cards) != 0:
    #         if self.user.hand.bounds.collidepoint(pos):
    #             self.user.hand.settle()
    #         elif self.table.bounds.collidepoint(pos):
#
    #             self.table.settle()
#
    # def handle_mouse_down(self, pos):
    #     for card in self.user.hand:
    #         if card.state == 'selected':
    #             self.selected_cards.append(card)
    #             break
#
    # def selected_nominal_has_more_twins(self):
    #     selected_nominal = self.selected_cards[0].nominal
    #     selected_count = len(self.selected_cards)
    #     nominal_twin_count = 0
    #     for card in self.user.hand:
    #         if card.nominal == selected_nominal:
    #             nominal_twin_count += 1
    #     if nominal_twin_count > selected_count:
    #         return True
    #     else:
    #         return False
        
    
def main():
    Fool().run()


if __name__ == '__main__':
    main()
