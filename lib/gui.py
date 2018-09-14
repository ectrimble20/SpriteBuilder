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
