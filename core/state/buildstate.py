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
        self._gui_images = GuiImageButtonGroup(pygame.Rect(128, 220, 544, 160))
        self._images = Manager()
        self._current_image = CompoundImage()
        self._image_count = 0
        self._preview_image = None

    def input(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and self._preview_image is not None:
                    self._current_image.add(self._preview_image.get_raw())

    def update(self, dt):
        action = self._gui.update(dt)
        if action is not None:
            if action == 'quit':
                self.parent.trigger_quit()
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

    def draw(self, display):
        self._gui.draw(display)
        self._gui_images.draw(display)  # draw this after the other gui elements
        if self._preview_image is not None:
            # get the center of the preview box
            cp = self._gui.find_element("content_mouse_over").rect.center
            pr = self._preview_image.get_raw().get_rect()
            pr.center = cp
            display.blit(self._preview_image.get_raw(), pr)
        if self._current_image.has_content():
            cp = self._gui.find_element("content_preview_16").rect.center
            pi = self._current_image.get_image(1)
            pr = pi.get_rect()
            pr.center = cp
            display.blit(pi, pr)
            cp = self._gui.find_element("content_preview_32").rect.center
            pi = self._current_image.get_image(2)
            pr = pi.get_rect()
            pr.center = cp
            display.blit(pi, pr)
            cp = self._gui.find_element("content_preview_64").rect.center
            pi = self._current_image.get_image(4)
            pr = pi.get_rect()
            pr.center = cp
            display.blit(pi, pr)

    def on_enter(self):
        if not self._loaded:
            self._gui.create_button("btn_undo", "undo", "Undo Last", pygame.Rect(464, 40, 96, 32))
            self._gui.create_button("btn_save", "save", "Save", pygame.Rect(240, 40, 96, 32))
            self._gui.create_button("btn_clear", "clear", "Clear", pygame.Rect(352, 40, 96, 32))
            self._gui.create_button("btn_quit", "quit", "Quit", pygame.Rect(128, 40, 96, 32))
            self._gui.create_button("btn_scroll_top", "scroll_top", "First", pygame.Rect(680, 220, 48, 32))
            self._gui.create_button("btn_scroll_up", "scroll_up", "Up", pygame.Rect(680, 260, 48, 32))
            self._gui.create_button("btn_scroll_down", "scroll_down", "Down", pygame.Rect(680, 300, 48, 32))
            self._gui.create_button("btn_scroll_end", "scroll_end", "Last", pygame.Rect(680, 340, 48, 32))
            self._gui.create_content_box("content_images", pygame.Rect(128, 220, 544, 160))
            self._gui.create_content_box("content_mouse_over", pygame.Rect(592, 130, 80, 80))
            self._gui.create_content_box("content_preview_16", pygame.Rect(128, 130, 80, 80))
            self._gui.create_content_box("content_preview_32", pygame.Rect(228, 130, 80, 80))
            self._gui.create_content_box("content_preview_64", pygame.Rect(328, 130, 80, 80))
            self._gui.create_text_input("input_image_label", "Text", pygame.Rect(200, 86, 200, 30), "")
            self._gui.create_text_label("filename_label", "Filename", 130, 92)
            self._load_images()
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
        self._gui_images.load(images)

    def _save_image(self):
        if self._current_image.has_content():
            file_name = self._gui.find_element('input_image_label').get_text()
            if len(file_name) == 0:
                file_name = get_save_image_path()
            else:
                file_name = path.join(CREATED_IMAGE_DIR, "{}.png".format(file_name))
            print("Attempting to save image to {}".format(file_name))
            pygame.image.save(self._current_image.get_image(1), file_name)
            if path.isfile(file_name):
                self._current_image.reset()
                self._gui.find_element('input_image_label').clear()
