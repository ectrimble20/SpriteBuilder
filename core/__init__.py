from local import *


class SpriteBuilder(object):

    def __init__(self):
        self._states = {}
        self._active_state = None
        self._change_state_to = None
        # TODO allow resize
        self.display = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION)
        # TODO init states
        # TODO init GUI
        self._running = True

    def init_states(self):
        pass

    def init_gui(self):
        pass

    def run(self):
        while self._running:
            self.display.fill((0, 0, 0))  # TODO import my color lib stuff
            self._active_state.input()
            self._active_state.update()
            self._active_state.draw(self.display)
            if self._change_state_to is not None:
                self._active_state.on_exit()
                self._active_state = self._change_state_to
                self._change_state_to = None
                self._active_state.on_enter()

    def trigger_quit(self):
        self._running = False

    def trigger_state_change(self, to):
        if to in self._states.keys():
            self._change_state_to = to
