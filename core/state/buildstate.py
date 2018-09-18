from core.state import RunState
from local import *
from lib.gui import Gui, GuiImageButtonGroup
from lib.images import CompoundImage
from lib.manage import Manager


class BuildState(RunState):

    def __init__(self, parent):
        super().__init__(parent)
        self._loaded = False
        self._gui = Gui()
        self._gui_images = GuiImageButtonGroup(self._gui, POS_CTB_IMAGES)
        self._images = Manager()
        self._current_image = CompoundImage()
        self._image_count = 0
        self._preview_image = None

    def input(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self._preview_image is not None:
                    self._current_image.add(self._preview_image.get_raw())
        self._gui.input(events)

    def update(self, dt):
        action = self._gui.update(dt)
        if action is not None:
            if action == 'back':
                self.parent.trigger_state_change('menu')
            if action == 'save':
                self._save_image()
            if action == 'clear':
                self._current_image.reset()
                # self.clear_preview(False)
            if action == 'undo':
                self._current_image.undo()
                # self.undo_last()
            if action == 'scroll_up':
                self._gui_images.row_up()
                # self.scroll_up()
            if action == 'scroll_down':
                self._gui_images.row_down()
                # self.scroll_down()
            if action == 'scroll_top':
                self._gui_images.row_first()
            if action == 'scroll_end':
                self._gui_images.row_last()
        self._preview_image = self._gui_images.mouse_over()
        # check for mouse scroll
        if self._gui.mouse_scroll != 0:
            if self._gui.mouse_scroll > 0:
                    self._gui_images.row_up()
            else:
                    self._gui_images.row_down()

    def draw(self, display):
        self._gui.draw(display)
        self._gui_images.draw(display)  # draw this after the other gui elements
        if self._preview_image is not None:
            # get the center of the preview box
            cp = self._gui.find_element("content_box", "content_mouse_over").rect.center
            pv_img = self._preview_image.get_raw()
            pr = pv_img.get_rect()
            # we need to adjust the preview to 64x64
            if pr.w != 64:
                tmp = pygame.Surface([64, 64])
                tmp.fill(TRANSPARENCY_COLOR)
                tmp.set_colorkey(TRANSPARENCY_COLOR)
                pygame.transform.scale(pv_img, (64, 64), tmp)
                pv_img = tmp
                pr = pv_img.get_rect()
            pr.center = cp
            display.blit(pv_img, pr)
        if self._current_image.has_content():
            cp = self._gui.find_element("content_box", "content_preview_16").rect.center
            pi = self._current_image.get_image(1)
            pr = pi.get_rect()
            pr.center = cp
            display.blit(pi, pr)
            cp = self._gui.find_element("content_box", "content_preview_32").rect.center
            pi = self._current_image.get_image(2)
            pr = pi.get_rect()
            pr.center = cp
            display.blit(pi, pr)
            cp = self._gui.find_element("content_box", "content_preview_64").rect.center
            pi = self._current_image.get_image(4)
            pr = pi.get_rect()
            pr.center = cp
            display.blit(pi, pr)
        self._gui.draw_tooltip(display)  # we draw this last as it needs to overlay everything if it's present

    def on_enter(self):
        if not self._loaded:
            self._gui.create_button("btn_undo", "undo", "Undo Last", POS_BTN_UNDO)
            self._gui.create_button("btn_save", "save", "Save", POS_BTN_SAVE)
            self._gui.create_button("btn_clear", "clear", "Clear", POS_BTN_CLEAR)
            self._gui.create_button("btn_back", "back", "Back", POS_BTN_QUIT)
            self._gui.create_button("btn_scroll_top", "scroll_top", "First", POS_BTN_S_TOP)
            self._gui.create_button("btn_scroll_up", "scroll_up", "Up", POS_BTN_S_UP)
            self._gui.create_button("btn_scroll_down", "scroll_down", "Down", POS_BTN_S_DOWN)
            self._gui.create_button("btn_scroll_end", "scroll_end", "Last", POS_BTN_S_END)
            self._gui.create_content_box("content_images", POS_CTB_IMAGES)
            self._gui.create_content_box("content_mouse_over", POS_CTB_MO_PV)
            self._gui.create_content_box("content_preview_16", POS_CTB_PV_16)
            self._gui.create_content_box("content_preview_32", POS_CTB_PV_32)
            self._gui.create_content_box("content_preview_64", POS_CTB_PV_64)
            self._gui.create_text_input("input_image_label", "Text", POS_TXT_IN_IMG_LABEL, "")
            self._gui.create_text_label("filename_label", "Image Name", POS_LABEL_FILENAME)
            self._load_images()
            # self._gui.mouse_text("TEST MOUSE TEXT")
            # add image btn group here
            self._loaded = True

    def on_exit(self):
        pass

    def _load_images(self):
        self._images.clear()
        images = []
        files = get_dir_contents(LIST_IMAGE_DIR)
        for f in files:
            full_path = path.join(LIST_IMAGE_DIR, f)
            img = pygame.image.load(full_path).convert()
            # we only handle up to 64x64 images
            if img.get_rect().w > 64 or img.get_rect().h > 64:
                continue
            img.set_colorkey(TRANSPARENCY_COLOR)
            images.append(img)
        self._gui_images.load(self._gui, images)

    def _save_image(self):
        if self._current_image.has_content():
            file_name = self._gui.find_element("text_input", 'input_image_label').get_text()
            if len(file_name) == 0:
                file_name = get_save_image_path()
            else:
                file_name = path.join(CREATED_IMAGE_DIR, "{}.png".format(file_name))
            print("Attempting to save image to {}".format(file_name))
            pygame.image.save(self._current_image.get_image(1), file_name)
            if path.isfile(file_name):
                self._current_image.reset()
                self._gui.find_element("text_input", 'input_image_label').clear()
