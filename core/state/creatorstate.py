from core.state import RunState
from local import *
from lib.gui import Gui


class CreatorState(RunState):

    def __init__(self, parent):
        super().__init__(parent)
        self._loaded = False
        self._gui = Gui()

    def input(self, events):
        self._gui.input(events)

    def update(self, dt):
        action = self._gui.update(dt)
        if action is not None:
            if action == 'back':
                self.parent.trigger_state_change('menu')

    def draw(self, display):
        self._gui.draw(display)

    def on_enter(self):
        if not self._loaded:
            self._gui.create_button('btn_back', 'back', 'Back', POS_BTN_QUIT)
            self._loaded = True

    def on_exit(self):
        pass
