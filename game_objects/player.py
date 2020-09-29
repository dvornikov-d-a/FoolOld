class Player():
    def __init__(self, hand, is_user=True):
        self.is_user = is_user
        self.hand = hand
        if self.is_user:
            self.show_hand()
        
    def hide_hand(self):
        self.hand.hide()

    def show_hand(self):
        self.hand.show()