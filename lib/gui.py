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

    def __init__(self, parent):
        self.parent = parent
        self.rect = None
        self.image = None

    def update(self, mouse_rect, btn_state, dt):
        pass

    def mouse_over(self, mouse_rect):
        return mouse_rect.colliderect(self.rect)

    def tool_tip(self):
        pass


class GuiContentBox(GuiElement):

    def __init__(self, parent, rect):
        super().__init__(parent)
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

    def __init__(self, parent, rect, label, action, big=False):
        super().__init__(parent)
        self._images = {}
        self.action = action
        self.label = label
        self.rect = rect
        btn = pygame.Surface([self.rect.w, self.rect.h])
        btn.fill(GUI_BG_CLR)
        if GUI_BDR_WIDTH > 0:
            border_rect = pygame.Rect(0, 0, self.rect.w, self.rect.h)
            pygame.draw.rect(btn, GUI_BDR_CLR, border_rect, GUI_BDR_WIDTH)
        if big:
            text = FONT_24.render(label, True, GUI_FONT_CLR)
        else:
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
        if big:
            text = FONT_24.render(label, True, GUI_FONT_CLR_HVR)
        else:
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

    def tool_tip(self):
        return self.label


class GuiTextInput(GuiElement):

    # TODO we'll need to handle clicking on text and figuring out where to put the cursor
    def __init__(self, parent, rect, label, text: list, max_len=0):
        super().__init__(parent)
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
        self._cursor_blink = 0.5
        self._del_timer = 0.0  # prevent delete from going nuts
        self._del_limit = 0.1
        self._content_box = GuiContentBox(self.parent, rect)
        self.cursor_to_end()  # This calls render

    def neglect(self):
        self.focused = False
        self.image = self._images['no_cursor']
        self._del_timer = 0.0

    def focus(self):
        self.focused = True
        self.image = self._images['cursor']

    def cursor_blink(self, dt):
        if self.focused:
            self._blink_timer += dt
            self._del_timer += dt
            if self._blink_timer > self._cursor_blink:
                self._cursor_state = not self._cursor_state
                self._blink_timer = 0.0
                if self._cursor_state:
                    self.image = self._images['cursor']
                else:
                    self.image = self._images['no_cursor']

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

    def get_text(self):
        return "".join(self._text)

    def type(self, char):
        # only allow input if we have a max len and it isn't surpassed
        if 0 <= self._max <= len(self._text):
            self._text.append(char)
            self.cursor_forward()

    def backspace(self):
        if self._del_timer >= self._del_limit:
            self._del_timer = 0.0
            if self._cursor_pos > 0:
                self._cursor_pos -= 1
                self._text.pop(self._cursor_pos)
                self.render_text()

    def delete(self):
        if self._del_timer >= self._del_limit:
            self._del_timer = 0.0
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

    def __init__(self, parent, surface):
        super().__init__(parent)
        self._raw_image = surface  # copy of original surface for reference
        self.image = get_transparent_surface(64, 64)
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

    def __init__(self, gui, display_rect):
        self._gui_ref = gui
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

    def load(self, gui_parent, image_list):
        # calculate the number of rows we need
        images_per_row = self.rect.w // 64
        self._rows_shown = self.rect.h // 64
        self._row_count = (len(image_list) // images_per_row) + 1  # pad by one
        # now we loop and build each row walking the image list
        for r in range(0, self._row_count):
            row = []
            for _ in range(0, images_per_row):
                try:
                    row.append(GuiImageButton(gui_parent, image_list.pop(0)))
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

    def __init__(self, parent, text, x, y):
        super().__init__(parent)
        self.image = FONT_16.render(text, True, GUI_FONT_CLR)
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y


class GuiColorCell(GuiElement):

    def __init__(self, rect, color, grid_color=BLACK):
        super().__init__(None)  # we hand None to GuiElement as we don't need a parent ref for this class
        self.rect = rect
        self._color = color
        self._grid_color = grid_color
        self._build_image()

    def _build_image(self):
        self.image = pygame.Surface([self.rect.w, self.rect.h]).convert()
        self.image.fill(self._color)
        dr = pygame.Rect(0, 0, self.rect.w, self.rect.h)
        pygame.draw.rect(self.image, self._grid_color, dr, 1)

    def set_color(self, color):
        self._color = color
        self._build_image()

    def set_grid_color(self, color):
        self._grid_color = color
        self._build_image()

    def get_color(self):
        return self._color


class GuiColorCellGrid(object):

    def __init__(self, x, y, image_width=16, image_height=16):
        self._x = x
        self._y = y
        self._w = image_width
        self._h = image_height
        self._cells = []
        for cy in range(0, self._h):
            for cx in range(0, self._w):
                cell_x = self._x + (cx * self._w)
                cell_y = self._y + (cy * self._h)
                cell_rect = pygame.Rect(cell_x, cell_y, self._w, self._h)
                self._cells.append(GuiColorCell(cell_rect, TRANSPARENCY_COLOR))

    def draw(self, display):
        for cell in self._cells:
            display.blit(cell.image, cell.rect)
        pygame.draw.rect(display, GUI_BDR_CLR, pygame.Rect(self._x-2, self._y-2, (self._w*16)+4, (self._h*16)+4), 1)


class GuiMouseButtonState(object):

    def __init__(self):
        self.state = False  # True - down, False - Up
        self.state_time = 0.0

    def update(self, dt):
        self.state_time += dt

    def change_state(self, state):
        self.state = state
        self.state_time = 0.0


class GuiKeyboardState(object):

    # Note, for key_down/up, key_event needs to come from pygame.event
    def __init__(self):
        self.backspace_down = False
        self.delete_down = False
        self.left_down = False
        self.right_down = False
        self.up_down = False
        self.down_down = False  # best naming scheme ever
        self._typing_queue = []
        self._allowed = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_- "  # allowed chars

    def key_down(self, key_event):
        if key_event.key == pygame.K_DELETE:
            self.delete_down = True
            return None
        if key_event.key == pygame.K_BACKSPACE:
            self.backspace_down = True
            return None
        if key_event.key == pygame.K_UP:
            self.up_down = True
            return None
        if key_event.key == pygame.K_DOWN:
            self.down_down = True
            return None
        if key_event.key == pygame.K_LEFT:
            self.left_down = True
            return None
        if key_event.key == pygame.K_RIGHT:
            self.right_down = True
            return None
        if key_event.unicode in self._allowed:
                self._typing_queue.append(key_event.unicode)

    def key_up(self, key_event):
        if key_event.key == pygame.K_DELETE:
            self.delete_down = False
            return None
        if key_event.key == pygame.K_BACKSPACE:
            self.backspace_down = False
            return None
        if key_event.key == pygame.K_UP:
            self.up_down = False
            return None
        if key_event.key == pygame.K_DOWN:
            self.down_down = False
            return None
        if key_event.key == pygame.K_LEFT:
            self.left_down = False
            return None
        if key_event.key == pygame.K_RIGHT:
            self.right_down = False
            return None

    def has_input(self):
        return len(self._typing_queue) > 0 or self.delete_down or self.backspace_down

    def has_text(self):
        return len(self._typing_queue) > 0

    def get(self):
        s = "".join(self._typing_queue)
        self._typing_queue.clear()
        return s


class Gui(object):

    def __init__(self):
        # TODO, this might need to be specific element types (e.g buttons, text boxes, etc)
        self._elements = {
            "button": {},
            "content_box": {},
            "text_input": {},
            "text_label": {}
        }
        self._focused_input = None
        # click speed control
        self._mouse_action_timer = 0.0
        self._mouse_action_delay = 0.15
        self._mouse_helper_text_obj = None
        self._current_mouse_helper_text = None
        # 0.1.2 elements
        self._mouse_over_element = None
        self._click_action = None
        # mouse controls
        self.mouse_btn_states = {
            1: GuiMouseButtonState(), 2: GuiMouseButtonState, 3: GuiMouseButtonState
        }
        self.mouse_scroll = 0  # mouse button 4 = up, 5 = down, up +, down -, so -3 means mouse scrolled down 3
        self.keyboard_state = GuiKeyboardState()
        self.mouse_rect = pygame.Rect(0, 0, 1, 1)

    def mouse_text(self, text):
        if self._current_mouse_helper_text != text:
            self._current_mouse_helper_text = text
            txt_obj = FONT_12.render(text, True, GUI_FONT_CLR, GUI_BG_CLR)
            self._mouse_helper_text_obj = pygame.Surface([txt_obj.get_rect().w + 4, txt_obj.get_rect().h + 4]).convert()
            self._mouse_helper_text_obj.blit(txt_obj, (2, 2))
            if GUI_BDR_WIDTH > 0:
                r = self._mouse_helper_text_obj.get_rect()
                r.topleft = 0, 0
                pygame.draw.rect(self._mouse_helper_text_obj, GUI_BDR_CLR, r, GUI_BDR_WIDTH)

    def no_mouse_text(self):
        self._current_mouse_helper_text = None
        self._mouse_helper_text_obj = None

    def add_element(self, category, key, element):
        self._elements[category][key] = element

    def find_element(self, cat, key):
        return self._elements.get(cat).get(key, None)

    def create_button(self, key, action, label, rect):
        self.add_element("button", key, GuiButton(self, rect, label, action))

    def create_large_button(self, key, action, label, rect):
        self.add_element("button", key, GuiButton(self, rect, label, action, True))

    def create_content_box(self, key, rect):
        self.add_element("content_box", key, GuiContentBox(self, rect))

    def create_text_input(self, key, label, rect, text, max_len=0):
        self.add_element("text_input", key, GuiTextInput(self, rect, label, text, max_len))

    def create_text_label(self, key, text, point):
        self.add_element("text_label", key, GuiTextLabel(self, text, point[0], point[1]))

    def input(self, events):  # events should be handed over from pygame.event.get()
        self.mouse_rect.topleft = pygame.mouse.get_pos()
        self.mouse_scroll = 0
        for e in events:
            # check for mouse 1, 2, 3 (clicks) and 4, 5 scroll (only checking btn down for 4/5)
            if e.type == pygame.MOUSEBUTTONDOWN:
                if e.button in self.mouse_btn_states.keys():
                    self.mouse_btn_states[e.button].change_state(True)
                if e.button == 4:
                    self.mouse_scroll = 1
                if e.button == 5:
                    self.mouse_scroll = -1
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button in self.mouse_btn_states.keys():
                    self.mouse_btn_states[e.button].change_state(False)
            # should have mouse state and position done now
            if e.type == pygame.KEYDOWN:
                self.keyboard_state.key_down(e)
            if e.type == pygame.KEYUP:
                self.keyboard_state.key_up(e)

    def update(self, dt):
        self._mouse_action_timer += dt
        # first, lets check for mouse-over's on buttons and change their state as needed
        hover_check = False
        for k, btn in self._elements['button'].items():
            if btn.mouse_over(self.mouse_rect):
                btn.state_hover()
                self.mouse_text(btn.tool_tip())
                hover_check = True
                # check if LMB is down, if it is, return the buttons action
                if self.mouse_btn_states[1].state:
                    # ensure we don't send actions too quickly
                    if self._mouse_action_timer > self._mouse_action_delay:
                        self._mouse_action_timer = 0.0
                        return btn.action
            else:
                btn.state_none()
        # just checks if the mouse was over a button, if it wasn't we make sure we don't have tool tip text
        if not hover_check:
            self.no_mouse_text()
        # next, lets to check our text boxes IF we have keyboard input
        for k, txt in self._elements['text_input'].items():
            # if focused check if the element is still in focus (clicked off)
            if txt.focused:
                if self.mouse_btn_states[1].state:
                    if not txt.mouse_over(self.mouse_rect):
                        txt.neglect()
            else:  # otherwise, check if it's been clicked (focused on)
                if self.mouse_btn_states[1].state:
                    if txt.mouse_over(self.mouse_rect):
                        txt.focus()
            # now if the object is still in focus, process whatever input we caught
            if txt.focused:  # TODO need to handle arrow keys moving the cursor
                if self.keyboard_state.backspace_down:
                    txt.backspace()
                if self.keyboard_state.delete_down:
                    txt.delete()
                if self.keyboard_state.has_text():
                    txt.type(self.keyboard_state.get())
                # lastly, after all text has been updated, we call cursor blink
                txt.cursor_blink(dt)
        return None

    def draw(self, display):
        for k, e in self._elements['button'].items():
            display.blit(e.image, e.rect)
        for k, e in self._elements['content_box'].items():
            display.blit(e.image, e.rect)
        for k, e in self._elements['text_input'].items():
            display.blit(e.image, e.rect)
        for k, e in self._elements['text_label'].items():
            display.blit(e.image, e.rect)

    def draw_tooltip(self, display):
        if self._mouse_helper_text_obj is not None:
            p = pygame.mouse.get_pos()
            mt_rect = self._mouse_helper_text_obj.get_rect()
            if p[0] + self._mouse_helper_text_obj.get_rect().w + GUI_TOOLTIP_PADDING > SCREEN_WIDTH:
                mt_rect.x = p[0] - mt_rect.w - GUI_TOOLTIP_PADDING
            else:
                mt_rect.x = p[0] + GUI_TOOLTIP_PADDING
            if p[1] + self._mouse_helper_text_obj.get_rect().h + GUI_TOOLTIP_PADDING > SCREEN_HEIGHT:
                mt_rect.y = p[1] - mt_rect.h - GUI_TOOLTIP_PADDING
            else:
                mt_rect.y = p[1] + GUI_TOOLTIP_PADDING
            display.blit(self._mouse_helper_text_obj, mt_rect)