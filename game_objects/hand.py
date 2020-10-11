import pygame

import config as c
from game_objects.game_object import GameObject


class Hand(GameObject):
    def __init__(self, cards, is_user=True):
        self.is_user = is_user
        y = 0
        if self.is_user:
            y = c.screen_height - 2 * c.hand_offset_y - c.card_h
        GameObject.__init__(self, 0, y, c.hand_w, c.hand_h)
        self.cards = cards
        self.settle()

        # Карта, на которой сфокусирован пользователь,
        # т.е. которую он собирается переместить.
        self.card_focused_on = None

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
        int_between = min(c.hand_max_int_between_cards,
                          (self.width - 2 * c.hand_offset_x - self.size * c.card_w) // (self.size - 1))
        offset_x = (self.width - 2 * c.hand_offset_x - self.size * c.card_w - int_between * (self.size - 1)) // 2
        for i, card in enumerate(self.cards):
            card.move(self.left + c.hand_offset_x + offset_x - card.left + int_between * i + c.card_w * i,
                      self.top + c.hand_offset_y - card.top)

    # ToDo
    # Изменить логику обработки событий мыши:
    # разделить нажатия кнопок и движение
    def handle_mouse_button_event(self, button, type, pos):
        if type == pygame.MOUSEMOTION:
            self.handle_mouse_motion(pos)
        elif type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(button, pos)
        elif type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(button, pos)

    def handle_mouse_motion(self, pos):
        if not self.any_card_in_state('selected') \
                and (self.card_focused_on is None
                     or not self.card_focused_on.in_bounds(pos)):
            self.focus_on_next(pos)

    def handle_mouse_down(self, button, pos):
        # Нажата правая кнопка мыши
        if button == 3:
            self.focus_on_next(pos)

    def handle_mouse_up(self, button, pos):
        pass

    def any_card_in_state(self, state):
        cards_in_state = [card for card in self.cards if card.state == state]
        if len(cards_in_state) == 0:
            return False
        else:
            return True

    # Находит карты, в чьи границы попадает определённая точка (например, указатель курсора).
    # Можно сказать, возвращает список "конфликтующих" карт.
    def find_collided_cards(self, pos):
        collided_cards = [card for card in self.cards if card.bounds.collidepoint(pos)]
        return collided_cards

    # Сменяет фокус на следующую карту из списка конфликтующих.
    def focus_on_next(self, pos):
        collided_cards = self.find_collided_cards(pos)

        # Нет конфликтующих за фокус карт
        if len(collided_cards) == 0:
            # Убрать фокус
            self.card_focused_on = None
            return

        # Нет выделенных карт
        if self.card_focused_on is None:
            # Выделить последнюю отображённую Карту, т.е. ту, что "лежит" поверх других, ведь
            # Карты хранятся в Руке в порядке их отображения.
            card_to_focus_on = collided_cards.pop()
        # Есть выделенная карта
        else:
            # Ещё конфликтует за фокус?
            still_collided = collided_cards.__contains__(self.card_focused_on)
            if not still_collided:
                # Больше не претендует на фокус - выделить последнюю
                card_to_focus_on = collided_cards.pop()
            else:
                # Ещё конфликтует
                # Индекс выделенной карты в списке конфликтующих
                cur_collided_card_index = collided_cards.index(self.card_focused_on)
                # Индекс следующей карты в списке конфликтующих
                next_collided_card_index = (cur_collided_card_index + 1) % len(collided_cards)
                # Следующая карта
                card_to_focus_on = collided_cards[next_collided_card_index]

        self.card_focused_on = card_to_focus_on

    def update(self):
        for card in self:
            if card != self.card_focused_on:
                card.state = 'normal'
            else:
                if card.state == 'normal':
                    card.state = 'hover'
            card.update()

    def draw(self, surface):
        for card in [card for card in self if card.state == 'normal']:
            card.draw(surface)
        for card in [card for card in self if card.state == 'hover']:
            card.draw(surface)
        for card in [card for card in self if card.state == 'selected']:
            card.draw(surface)
