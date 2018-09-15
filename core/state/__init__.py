class RunState(object):

    def __init__(self, parent):
        self.parent = parent

    def input(self, events):
        pass

    def update(self, dt):
        pass

    def draw(self, display):
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass
