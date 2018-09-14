from lib.manage import Manager


class RunState(object):

    def __init__(self):
        self.data = Manager()  # general data manager for a state

    def input(self):
        pass

    def update(self, delta_time):
        pass

    def draw(self, display):
        pass

    def on_enter(self):
        pass

    def on_exit(self):
        pass
