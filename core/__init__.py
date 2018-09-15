from local import *
from core.state.buildstate import BuildState


class SpriteBuilder(object):

    def __init__(self):
        self._states = {}
        self._active_state = None
        self._change_state_to = None
        # TODO allow resize
        self.display = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION)
        self.init_states()
        self._running = True
        self.clock = pygame.time.Clock()
        self.dt = 0.0

    def init_states(self):
        self._states["build"] = BuildState(self)
        self._active_state = self._states["build"]
        self._active_state.on_enter()

    def run(self):
        while self._running:
            self.display.fill((0, 0, 0))  # TODO import my color lib stuff
            self._active_state.input(self.process_event_queue())
            self._active_state.update(self.dt)
            self._active_state.draw(self.display)
            self.dt = self.clock.tick(60) / 1000
            pygame.display.update()
            if self._change_state_to is not None:
                self._active_state.on_exit()
                self._active_state = self._change_state_to
                self._change_state_to = None
                self._active_state.on_enter()

    def process_event_queue(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.trigger_quit()
        return events

    def trigger_quit(self):
        self._running = False

    def trigger_state_change(self, to):
        if to in self._states.keys():
            self._change_state_to = to
