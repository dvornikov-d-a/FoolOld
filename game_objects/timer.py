import time


class Timer():
    def __init__(self):
        self.finish_time = time.time()
        self.is_on = False

    def run(self, sec):
        self.finish_time = time.time() + sec
        self.is_on = True

    def reset(self):
        self.is_on = False

    @property
    def is_ringing(self):
        if self.is_on and time.time() >= self.finish_time:
            return True
        else:
            return False