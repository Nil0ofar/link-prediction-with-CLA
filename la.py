from numpy.random import choice

class LA:
    def __init__(self):
        self.action = [0, 1]
        self.probability = [0.5, 0.5]

    def get_action(self):
        return choice(self.action, 1, self.probability)[0]