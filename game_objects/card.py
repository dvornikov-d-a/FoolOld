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

        # self.long_hover = False
        # self.hover_timer = Timer()

        image_path = 'source/images/cards/' + self.suit+'/' + self.nominal + '.png'
        image = pygame.image.load(image_path)
        self.image = pygame.transform.smoothscale(image, (w, h))
        # flop_path = 'source/images/cards/flop.png'
        # flop = pygame.image.load(flop_path)
        self.flop = pygame.transform.smoothscale(c.flop, (w, h))
        self.hover_bounds = pygame.transform.smoothscale(c.hover_bounds, (w, h))


    @ property
    def focused(self):
        if self.state == 'hover' or self.state == 'selected':
            return True
        else:
            return False

    def hide(self):
        self.hidden = True

    def show(self):
        self.hidden = False

    def in_bounds(self, pos):
        return self.bounds.collidepoint(pos)

    def draw(self, surface):
        if self.hidden:
            surface.blit(self.flop, (self.left, self.top))
        else:
            surface.blit(self.image, (self.left, self.top))
            if self.focused:
                surface.blit(self.hover_bounds, (self.left, self.top))

    def update(self):
        # if self.state == 'hover':
        #     if self.hover_timer.is_ringing:
        #         self.long_hover = True
        #         self.hover_timer.reset()
        #     elif self.hover_timer.is_on:
        #         pass
        #     elif not self.long_hover:
        #         self.hover_timer.run(c.long_hover_sec)
        # else:
        #     self.long_hover = False
        #     self.hover_timer.reset()

        dx = self.dest_point[0] - self.cur_point[0]
        dy = self.dest_point[1] - self.cur_point[1]
        self.move(dx, dy)
        self.cur_point = self.dest_point

    def handle_button_mouse_event(self, button, type, pos):
        if type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(button, pos)
        elif type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(button, pos)

    def handle_mouse_motion(self, pos):
        if self.state == 'selected':
            self.dest_point = pos
        # elif self.bounds.collidepoint(pos):
        #     self.state = 'hover'

    # ToDo
    # Передать контроль состояния (hover, selected) Карты Руке
    def handle_mouse_down(self, button, pos):
        if button == 1:
            if self.bounds.collidepoint(pos):
                if self.state == 'hover':
                    self.state = 'selected'
                    self.cur_point = pos
                    self.dest_point = pos

    def handle_mouse_up(self, button, pos):
        if button == 1:
            if self.bounds.collidepoint(pos):
                if self.state == 'selected':
                    self.state = 'hover'
