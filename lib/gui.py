from local import *


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
        pygame.draw.circle(self.image, GUI_BDR_CLR, (center_x, center_y), 4, 0)
        self.image.set_colorkey(TRANSPARENCY_COLOR)


class GuiElement(object):

    def __init__(self):
        self.rect = None
        self.image = None

    def update(self, mouse_rect, btn_state, dt):
        return None


class GuiContentBox(GuiElement):

    def __init__(self, rect):
        super().__init__()
        self.rect = rect
        self.image = pygame.Surface([self.rect.w, self.rect.h])
        self.image.fill(GUI_BG_CLR)
        if GUI_BDR_WIDTH > 0:
            border_rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
            pygame.draw.rect(self.image, GUI_BDR_CLR, border_rect, GUI_BDR_WIDTH)

    def get_center(self):
        # just a shortcut for the rect's center
        return self.rect.center


class GuiButton(GuiElement):

    def __init__(self, action, label, rect):
        super().__init__()
        self._images = {}
        self.action = action
        self.rect = rect
        btn = pygame.Surface([self.rect.w, self.rect.h])
        btn.fill(GUI_BG_CLR)
        if GUI_BDR_WIDTH > 0:
            border_rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
            pygame.draw.rect(btn, GUI_BDR_CLR, border_rect, GUI_BDR_WIDTH)
        text = FONT_16.render(label, True, GUI_FONT_CLR)
        text_rect = text.get_rect()
        text_align_rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
        text_align_rect.x = self.rect.w // 2 - text_rect.w // 2
        text_align_rect.y = self.rect.h // 2 - text_rect.h // 2
        btn.blit(text, text_align_rect)
        self._images[0] = btn
        # mouse over
        btn = pygame.Surface([self.rect.w, self.rect.h])
        btn.fill(GUI_BG_CLR_HVR)
        if GUI_BDR_WIDTH > 0:
            border_rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
            pygame.draw.rect(btn, GUI_BDR_CLR_HVR, border_rect, GUI_BDR_WIDTH)
        text = FONT_16.render(label, True, GUI_FONT_CLR_HVR)
        text_rect = text.get_rect()
        text_align_rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
        text_align_rect.x = self.rect.w // 2 - text_rect.w // 2
        text_align_rect.y = self.rect.h // 2 - text_rect.h // 2
        btn.blit(text, text_align_rect)
        self._images[1] = btn

    def state_none(self):
        self.image = self._images[0]

    def state_hover(self):
        self.image = self._images[1]

    def update(self, mouse_rect, btn_state, dt):
        # check for button state changes
        if mouse_rect.colliderect(self.rect):
            self.state_hover()
            if btn_state[0]:
                return self.action
        else:
            self.state_none()
        return None


class GuiTextInput(GuiElement):

    # TODO we'll need to handle clicking on text and figuring out where to put the cursor
    def __init__(self, label, rect, text: list, max_len=0):
        super().__init__()
        self.label = label
        self.rect = rect
        self.focused = False
        self._max = max_len
        if not isinstance(text, list):
            text = list(text)
        self._text = text
        self._images = {}
        self._cursor_pos = 0
        self._cursor_state = False
        self._blink_timer = 0.0
        self._type_timer = 0.0
        self._cursor_blink = 0.5
        self._type_delay = 0.15
        self._content_box = GuiContentBox(rect)
        self.cursor_to_end()  # This calls render

    def update(self, mouse_rect, btn_state, dt):
        if self.focused:
            # TODO if we're focused, we'll need input capture
            self._blink_timer += dt
            self._type_timer += dt
            if self._blink_timer > self._cursor_blink:
                self._cursor_state = not self._cursor_state
                self._blink_timer = 0.0
            if self._cursor_state:
                self.image = self._images['cursor']
            else:
                self.image = self._images['no_cursor']
            if self._type_timer > self._type_delay:
                self.handle_text_input()
        # check for mouse clicked on us
        if btn_state[0]:
            if mouse_rect.colliderect(self.rect):
                self.focused = True
            else:
                self.focused = False
                # ensure we're not stuck with cursor shown
                self.image = self._images['no_cursor']
        return None

    def render_text(self):
        # TODO bug fix: need to calculate position of cursor as it's not working too well
        self._type_timer = 0.0  # this is where the typing timer is set
        text_str = "".join(self._text)
        text = FONT_16.render(text_str, True, GUI_FONT_CLR)
        # if the text is longer than the input box, we want to shift the text left
        if text.get_rect().w > self._content_box.rect.w - 10:
            # okay, we need to walk forward and check our size until it fits
            start = 1
            while True:
                fix_text = text_str[start:]
                size = FONT_16.size(fix_text)
                if size[0] > self._content_box.rect.w - 10:
                    start += 1
                else:
                    # found something that fits
                    text = FONT_16.render(fix_text, True, GUI_FONT_CLR)
                    text_str = fix_text
                    break
        ty = ((self._content_box.image.get_rect().h - text.get_rect().h) // 2) + GUI_BDR_WIDTH
        no_c = self._content_box.image.copy()
        no_c.blit(text, (GUI_BDR_WIDTH+1, ty))
        self._images['no_cursor'] = no_c
        with_c = self._content_box.image.copy()
        with_c.blit(text, (GUI_BDR_WIDTH+1, ty))
        fs = FONT_16.size(text_str)
        cp = fs[0]+GUI_BDR_WIDTH + 1, ty - GUI_BDR_WIDTH + 1
        cursor_end = cp[0], ty + fs[1] - GUI_BDR_WIDTH + 1
        pygame.draw.line(with_c, (255, 255, 255), cp, cursor_end, 1)
        self._images['cursor'] = with_c
        # set initial image state to no_cursor
        self.image = self._images['no_cursor']

    def handle_text_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            self.backspace()
        if keys[pygame.K_DELETE]:
            self.delete()
        if keys[pygame.K_LEFT]:
            self.cursor_backwards()
        if keys[pygame.K_RIGHT]:
            self.cursor_forward()
        # check alpha keys
        mods = pygame.key.get_mods()
        # handle 0-9
        for k in range(48, 58):
            if keys[k]:
                self.type(pygame.key.name(k))
        # handle a-z + shift/caps
        for k in range(97, 123):
            if keys[k]:
                k_letter = pygame.key.name(k)
                if mods & CAPS_ON:
                    if not mods & SHIFT_DOWN:
                        k_letter = str.capitalize(k_letter)
                else:
                    if mods & SHIFT_DOWN:
                        k_letter = str.capitalize(k_letter)
                self.type(k_letter)
        # check specific characters
        if keys[pygame.K_MINUS] and mods & SHIFT_DOWN:
            self.type("_")
        if keys[pygame.K_SPACE]:
            self.type("_")

    def get_text(self):
        return "".join(self._text)

    def type(self, char):
        # only allow input if we have a max len and it isn't surpassed
        if 0 <= self._max <= len(self._text):
            self._text.append(char)
            self.cursor_forward()

    def backspace(self):
        if self._cursor_pos > 0:
            self._cursor_pos -= 1
            self._text.pop(self._cursor_pos)
            self.render_text()

    def delete(self):
        if 0 < self._cursor_pos < len(self._text):
            self._text.pop(self._cursor_pos + 1)
            self.render_text()

    def cursor_to_end(self):
        self._cursor_pos = len(self._text)
        self.render_text()

    def cursor_forward(self):
        self._cursor_pos += 1
        self._cursor_bounds()
        self.render_text()

    def cursor_backwards(self):
        self._cursor_pos -= 1
        self._cursor_bounds()
        self.render_text()

    def position_cursor(self, at):
        self._cursor_pos = at
        self._cursor_bounds()
        self.render_text()

    def _cursor_bounds(self):
        if self._cursor_pos < 0:
            self._cursor_pos = 0
        if self._cursor_pos >= len(self._text):
            self._cursor_pos = len(self._text)

    def clear(self):
        self._text.clear()
        self._cursor_pos = 0
        self.render_text()


class GuiImageButton(GuiElement):

    def __init__(self, surface):
        super().__init__()
        self._raw_image = surface  # copy of original surface for reference
        self.image = pygame.Surface([64, 64])
        self.image.fill(TRANSPARENCY_COLOR)
        self.image.set_colorkey(TRANSPARENCY_COLOR)
        pt = 0, 0
        # adjust draw point if image is not 64x64, we want to draw in the center
        if self._raw_image.get_rect().w < 64 and self._raw_image.get_rect().h < 64:
            pt = (self.image.get_rect().w - self._raw_image.get_rect().w)//2, \
                 (self.image.get_rect().h - self._raw_image.get_rect().h)//2
        self.image.blit(self._raw_image, pt)
        # debug - just want to see that it's positioned correctly
        # pygame.draw.rect(self.image, (0, 0, 0), self.image.get_rect(), 1)
        self.rect = self.image.get_rect()

    def move_to(self, x, y):
        self.rect.topleft = x, y

    def get_raw(self):
        return self._raw_image


class GuiImageButtonGroup(object):

    def __init__(self, display_rect):
        self._image_button_rows = {}
        self.rect = display_rect
        self._rows_shown = 0
        self._row_count = 0
        self._row_display = 0  # what row are we starting at
        self._current_images = []

    def row_up(self):
        self._row_display -= 1
        if self._row_display < 0:
            self._row_display = 0
        else:
            self._populate_current_images()

    def row_down(self):
        self._row_display += 1
        if self._row_display > self._row_count - self._rows_shown:
            self._row_display = self._row_count - self._rows_shown
        else:
            self._populate_current_images()

    def row_first(self):
        if self._row_display != 0:
            self._row_display = 0
            self._populate_current_images()

    def row_last(self):
        if self._row_display != self._row_count - self._rows_shown:
            self._row_display = self._row_count - self._rows_shown
            self._populate_current_images()

    def load(self, image_list):
        # calculate the number of rows we need
        images_per_row = self.rect.w // 64
        self._rows_shown = self.rect.h // 64
        self._row_count = (len(image_list) // images_per_row) + 1  # pad by one
        # now we loop and build each row walking the image list
        for r in range(0, self._row_count):
            row = []
            for _ in range(0, images_per_row):
                try:
                    row.append(GuiImageButton(image_list.pop(0)))
                except IndexError:  # this means we ran out of images
                    break
            self._image_button_rows[r] = row
        self._populate_current_images()

    def _populate_current_images(self):
        self._current_images.clear()
        x_origin = self.rect.x + ((self.rect.w - ((self.rect.w // 64) * 64)) // 2)
        start_x = x_origin
        start_y = self.rect.y + ((self.rect.h - ((self.rect.h // 64) * 64)) // 2)
        for i in range(self._row_display, self._row_display+self._rows_shown):
            if i not in self._image_button_rows.keys():
                break
            row = self._image_button_rows[i]
            for img_btn in row:
                img_btn.move_to(start_x, start_y)
                self._current_images.append(img_btn)
                start_x += 64
            start_x = x_origin
            start_y += 64

    def mouse_over(self):
        # find an image if the mouse is over it
        mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
        for img_btn in self._current_images:
            if mouse_rect.colliderect(img_btn.rect):
                return img_btn
        return None

    def draw(self, display):
        for img_btn in self._current_images:
            display.blit(img_btn.image, img_btn.rect)


class GuiTextLabel(GuiElement):

    def __init__(self, text, x, y):
        super().__init__()
        self.image = FONT_16.render(text, True, GUI_FONT_CLR)
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

"""
This is going to be somewhat of a GUI manager, basically I want to just add elements to the GUI then have the GUI watch
events and do it's thing and check for certain "actions" that can occur with the GUI, I'll need to think this through a bit
"""


class Gui(object):

    def __init__(self):
        # TODO, this might need to be specific element types (e.g buttons, text boxes, etc)
        self._elements = {}
        self._focused_input = None
        self._action_timer = 0.0
        self._action_delay = 0.15

    def find_element(self, key):
        return self._elements.get(key, None)

    def create_button(self, key, action, label, rect):
        self._elements[key] = GuiButton(action, label, rect)

    def create_content_box(self, key, rect):
        self._elements[key] = GuiContentBox(rect)

    def create_text_input(self, key, label, rect, text):
        self._elements[key] = GuiTextInput(label, rect, text)

    def create_text_label(self, key, text, x, y):
        self._elements[key] = GuiTextLabel(text, x, y)

    def update(self, dt):
        action = None
        self._action_timer += dt
        mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
        button_states = pygame.mouse.get_pressed()
        for k, e in self._elements.items():
            a = e.update(mouse_rect, button_states, dt)
            if a is not None:
                action = a
        if action is not None:
            if self._action_timer < self._action_delay:
                return None
            else:
                self._action_timer = 0.0
                return action
        return None

    def draw(self, display):
        for k, e in self._elements.items():
            display.blit(e.image, e.rect)
