import config as c
from game_objects.game_object import GameObject


class Table(GameObject):
    def __init__(self):
        GameObject.__init__(self, 
                            c.hand_offset_x,
                            2*c.hand_offset_y + c.hand_h,
                            c.hand_w,
                            c.screen_height - 4*c.hand_offset_y + c.hand_h)
        self.user_pool = []
        self.bot_pool = []

    def settle(self):
        pass

    def user_attack(self, card):
        pass
