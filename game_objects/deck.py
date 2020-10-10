import pygame
import random

import config as c
from game_objects.card import Card
from game_objects.game_object import GameObject


# Колода карт
class Deck(GameObject):
    def __init__(self):
        GameObject.__init__(self,
                            c.screen_width - c.card_h // 2,
                            c.screen_height // 2 - c.card_w // 2,
                            c.card_h, c.card_w)
        self.image = pygame.transform.scale(c.flop_90, (self.width, self.height))

        self.cards = []

        self.fill_deck()
        self.shuffle()
        self.choose_trump()

    @property
    def size(self):
        return len(self.cards)
                
    def fill_deck(self):
        self.cards = []
        for suit in c.suits:
            for nominal in c.nominals:
                card = Card(0, 0, c.card_w, c.card_h, suit, nominal)
                self.cards.append(card)

    # ToDo
    # Изменить логику обработки событий мыши:
    # разделить нажатия кнопок и движение

    def shuffle(self):
        random.shuffle(self.cards)

    def choose_trump(self):
        self.trump = random.choice(c.suits)

    def give_cards(self, count=6):
        given_cards = []
        for i in range(count):
            given_cards.append(self.cards.pop())
        return given_cards

    def draw(self, surface):
        surface.blit(self.image, (self.left, self.top))