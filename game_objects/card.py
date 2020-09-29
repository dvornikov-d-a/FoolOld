import pygame

import config as c
from game_objects.game_object import GameObject
from game_objects.timer import Timer


class Card(GameObject):
    def __init__(self, x, y, w, h, suit, nominal):
        GameObject.__init__(self, x, y, w, h)
        self.hidden = True
        self.state = 'normal'
        self.dest_point = (self.left, self.top)
        self.cur_point = (self.left, self.top)
        self.suit = suit
        self.nominal = nominal

        self.long_hover = False
        self.hover_timer = Timer()

        image_path = 'images/cards/'+self.suit+'/'+self.nominal+'.png'
        image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(image, (w, h))
        flop_path = 'images/cards/flop.png'
        flop = pygame.image.load(flop_path)
        self.flop = pygame.transform.scale(flop, (w, h))

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def draw(self, surface):
        if self.hidden:
            surface.blit(self.flop, (self.left, self.top))
        else:
            surface.blit(self.image, (self.left, self.top))

    def update(self):
        if self.state == 'hover':
            if self.hover_timer.is_ringing:
                self.long_hover = True
                self.hover_timer.reset()
            elif self.hover_timer.is_on:
                pass
            elif not self.long_hover:
                self.hover_timer.run(c.long_hover_sec)
        else:
            self.long_hover = False
            self.hover_timer.reset()

        dx = self.dest_point[0] - self.cur_point[0]
        dy = self.dest_point[1] - self.cur_point[1]
        self.move(dx, dy)
        self.cur_point = self.dest_point

    def handle_mouse_event(self, type, pos):
        if type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        if self.state == 'selected':
            self.dest_point = pos
        elif self.bounds.collidepoint(pos):
            self.state = 'hover'

    def handle_mouse_down(self, pos):
        if self.bounds.collidepoint(pos):
            self.state = 'selected'
            self.cur_point = pos
            self.dest_point = pos

    def handle_mouse_up(self, pos):
        if self.state == 'selected':
            self.state = 'hover'
