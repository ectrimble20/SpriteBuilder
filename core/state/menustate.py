from core.state import RunState
from local import *
from lib.gui import Gui


class MenuState(RunState):

    def __init__(self, parent):
        super().__init__(parent)
        self._loaded = False
        self._gui = Gui()

    def input(self, events):
        self._gui.input(events)

    def update(self, dt):
        action = self._gui.update(dt)
        if action is not None:
            if action == 'nav_quit':
                self.parent.trigger_quit()
            if action == 'nav_builder':
                self.parent.trigger_state_change('build')
            if action == 'nav_create':
                self.parent.trigger_state_change('create')

    def draw(self, display):
        self._gui.draw(display)

    def on_enter(self):
        if not self._loaded:
            self._gui.create_large_button("btn_builder", "nav_builder", "Sprite Builder", pygame.Rect(200, 100, 300, 64))
            self._gui.create_large_button("btn_create", "nav_create", "Create Images", pygame.Rect(200, 250, 300, 64))
            self._gui.create_large_button("btn_quit", "nav_quit", "Exit", pygame.Rect(200, 400, 300, 64))
            self._loaded = True

    def on_exit(self):
        pass
