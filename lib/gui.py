from local import *


class Button(object):

    def __init__(self, action, label, x, y, w, h, callback=None):
        self.callback = callback
        self.action = action
        self.image = pygame.Surface([w, h])
        self.rect = pygame.Rect(x, y, w, h)
        self.image.fill(BUTTON_BG_COLOR)
        if BUTTON_BORDER_WIDTH > 0:
            border_rect = pygame.Rect(0, 0, w, h)
            pygame.draw.rect(self.image, BUTTON_BORDER_COLOR, border_rect, BUTTON_BORDER_WIDTH)
        self.text = FONT_16.render(label, True, BUTTON_TEXT_COLOR)
        text_rect = self.text.get_rect()
        text_align_rect = pygame.Rect(0, 0, w, h)
        text_align_rect.x = self.image.get_rect().w // 2 - text_rect.w // 2
        text_align_rect.y = self.image.get_rect().h // 2 - text_rect.h // 2
        self.image.blit(self.text, text_align_rect)

    def check(self, mouse_rect):
        if self.rect.colliderect(mouse_rect):
            if self.callback is not None:
                self.callback()


class ScrollPoint(pygame.sprite.Sprite):

    def __init__(self, rect, scroll_range):
        super().__init__()
        self._point = 1
        self._range = scroll_range
        self.rect = rect
        self.image = pygame.Surface([self.rect.w, self.rect.h])
        self._build()

    def scroll(self, amount):
        old_p = self._point
        self._point += amount
        if self._point > self._range:
            self._point = self._range
        if self._point < 1:
            self._point = 1
        if self._point != old_p:
            self._build()

    def mouse_over(self, mouse_rect):
        if self.rect.colliderect(mouse_rect):
            # okay, so what I need to do here is take the Y of this rect and compare it with the Y from the mouse
            # rect, this will give me a "relative" position, then we figure out where in our scroll this falls
            rel_y = max(self.rect.y, mouse_rect.y) - min(self.rect.y, mouse_rect.y)
            # to figure out where the relative position lies, we just need to figure out what divisor point the Y is at
            if rel_y == 0:  # protect against / by zero
                rel_y_point = 1
            else:
                rel_y_point = rel_y // (self.rect.h // self._range)
            # prevent 0 point
            if rel_y_point <= 0:
                rel_y_point = 1
            if self._point != rel_y_point:
                self._point = rel_y_point
                self._build()
                return self._point
            return None

    def _build(self):
        self.image = pygame.Surface([self.rect.w, self.rect.h])
        self.image.fill(TRANSPARENCY_COLOR)
        center_y = (self.rect.h // self._range) * self._point
        center_x = self.rect.w // 2
        pygame.draw.circle(self.image, BUTTON_BORDER_COLOR, (center_x, center_y), 4, 0)
        self.image.set_colorkey(TRANSPARENCY_COLOR)


class GuiButton(object):

    def __init__(self, action, label, rect, callback=None):
        self.callback = callback
        self._state = 0
        self._images = {}
        self.action = action
        self.rect = rect
        btn = pygame.Surface([self.rect.w, self.rect.h])
        btn.fill(BUTTON_BG_COLOR)
        if BUTTON_BORDER_WIDTH > 0:
            border_rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
            pygame.draw.rect(btn, BUTTON_BORDER_COLOR, border_rect, BUTTON_BORDER_WIDTH)
        text = FONT_16.render(label, True, BUTTON_TEXT_COLOR)
        text_rect = text.get_rect()
        text_align_rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
        text_align_rect.x = self.rect.w // 2 - text_rect.w // 2
        text_align_rect.y = self.rect.h // 2 - text_rect.h // 2
        btn.blit(text, text_align_rect)
        self._images[0] = btn
        # mouse over
        btn = pygame.Surface([self.rect.w, self.rect.h])
        btn.fill(BUTTON_MO_BG_COLOR)
        if BUTTON_BORDER_WIDTH > 0:
            border_rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
            pygame.draw.rect(btn, BUTTON_MO_BORDER_COLOR, border_rect, BUTTON_BORDER_WIDTH)
        text = FONT_16.render(label, True, BUTTON_MO_TEXT_COLOR)
        text_rect = text.get_rect()
        text_align_rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
        text_align_rect.x = self.rect.w // 2 - text_rect.w // 2
        text_align_rect.y = self.rect.h // 2 - text_rect.h // 2
        btn.blit(text, text_align_rect)
        self._images[1] = btn

    @property
    def image(self):
        return self._images[self._state]

    def state_none(self):
        self._state = 0

    def state_hover(self):
        self._state = 1


"""
This is going to be somewhat of a GUI manager, basically I want to just add elements to the GUI then have the GUI watch
events and do it's thing and check for certain "actions" that can occur with the GUI, I'll need to think this through a bit
"""


class Gui(object):

    def __init__(self):
        # TODO, this might need to be specific element types (e.g buttons, text boxes, etc)
        self._buttons = []
        self._action_timer = 0.0
        self._action_delay = 0.15
        self._button_action = None

    def button_action(self):
        action = self._button_action
        self._button_action = None
        return action

    def create_button(self, action, label, rect, callback=None):
        self._buttons.append(GuiButton(action, label, rect, callback))

    def add_button(self, btn: GuiButton):
        self._buttons.append(btn)

    def update(self, dt):
        action = None
        self._action_timer += dt
        mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
        button_states = pygame.mouse.get_pressed()
        # check for button state changes
        for btn in self._buttons:
            if mouse_rect.colliderect(btn.rect):
                btn.state_hover()
                if button_states[0]:
                    action = btn.action
            else:
                btn.state_none()
        if action is not None and self._button_action is None:
            if self._action_timer < self._action_delay:
                return None
            else:
                self._action_timer = 0.0
                print("ACTION DOINK {}".format(action))
                self._button_action = action

    def draw(self, display):
        for btn in self._buttons:
            display.blit(btn.image, btn.rect)
