import pygame

import config as c
from game_objects.game_object import GameObject


class Hand(GameObject):
    def __init__(self, cards, is_user=True):
        self.is_user = is_user
        y = 0
        if self.is_user:
            y = c.screen_height - 2*c.hand_offset_y - c.card_h
        GameObject.__init__(self, 0, y, c.hand_w, c.hand_h)
        self.cards = cards
        self.settle()

    def __iter__(self):
        return self.cards.__iter__()

    def __next__(self):
        return self.cards.__next__()

    @property
    def size(self):
        return len(self.cards)
    
    def hide(self):
        for card in self:
            card.hide()

    def show(self):
        for card in self:
            card.show()

    def settle(self):
        int_between = min(c.hand_max_int_between_cards, (self.width - 2*c.hand_offset_x - self.size*c.card_w) // (self.size - 1))
        offset_x = (self.width - 2*c.hand_offset_x - self.size*c.card_w - int_between*(self.size - 1)) // 2
        for i, card in enumerate(self.cards):
            card.move(self.left + c.hand_offset_x + offset_x - card.left + int_between*i + c.card_w*i,
                      self.top + c.hand_offset_y - card.top)

    #def draw(self, surface):
    #    for card in self:
    #        card.draw(surface)

    #def update(self):
    #    for card in self:
    #        card.update()