import random


class Cell:
    def __init__(self, x, y, rez, options):
        self.x = x
        self.y = y
        self.rez = rez
        self.options = options
        self.collapsed = False

    def observe(self):
        try:
            self.options = [random.choice(self.options)]
            self.collapsed = True
        except:
            return

    def entropy(self):
        return len(self.options)

    def update(self):
        self.collapsed = bool(self.entropy == 1)
