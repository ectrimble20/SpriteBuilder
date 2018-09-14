from lib.manage import Manager
from local import *  # NOTE: pygame is imported in local and thus accessible here
import os
from lib.gui import Button, ScrollPoint
from lib.images import ImageItem, PreviewImage, CompoundImage


# TODO implement mouse scroll wheel - need to handle timing and what not
# TODO implement naming images
# TODO checkbox for save with alpha channel
# TODO save compound image to a file for editing later
class Builder(object):

    def __init__(self):
        self.display = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("Sprite Builder: 1.0.0 Alpha")
        self.running = True
        self._scroll = 0
        self._images = Manager()  # images loaded in
        self._image_count = 0
        self._mgr = Manager()  # general objects
        self.load_images()  # do this once we get stuff done
        self.gui_group = pygame.sprite.Group()
        self.active_image_group = pygame.sprite.Group()
        self.gui_btn_group = pygame.sprite.Group()
        self._scroll_indicator = ScrollPoint(pygame.Rect(128, 221, 16, 78), (self._image_count//32)+1)
        self.build_lower_gui(self._scroll)
        self.build_gui_buttons()
        self.btns = ['btn_undo', 'btn_quit', 'btn_clear', 'btn_save', 'btn_scroll_up', 'btn_scroll_down', 'ph']
        self.img = CompoundImage()
        self.preview64 = None
        self.preview32 = None
        self.preview16 = None
        self.preview_mouse_over = None
        self._update_gui = False

    def run(self):
        while self.running:
            self.input()
            self.update()
            self.draw()

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.scroll_down()
                if event.key == pygame.K_w:
                    self.scroll_up()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
                    mouse_sprite = pygame.sprite.Sprite()
                    mouse_sprite.rect = mouse_rect
                    for btn_key in self.btns:
                        self._mgr.get(btn_key).check(mouse_rect)
                    active_image_clicked = pygame.sprite.spritecollideany(mouse_sprite, self.active_image_group)
                    if active_image_clicked is not None:
                        self.img.add(active_image_clicked.image, (0, 0))
                        self.update_preview()
            if self._update_gui:
                self.build_lower_gui(self._scroll)
                self._update_gui = False

    def update(self):
        # this is kinda fucky, need to work on this logic to make it less redundant
        mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
        if mouse_rect.colliderect(self._scroll_indicator.rect):
            pressed1 = pygame.mouse.get_pressed()[0]
            if pressed1:
                to = self._scroll_indicator.mouse_over(mouse_rect)
                if to is not None:
                    self.scroll_to(to)
        mouse_sprite = pygame.sprite.Sprite()
        mouse_sprite.rect = mouse_rect
        pv_img = pygame.sprite.spritecollideany(mouse_sprite, self.active_image_group)
        if pv_img is not None:
            self.preview_mouse_over = PreviewImage(pv_img.image, 600, 138, 4)
        else:
            self.preview_mouse_over = None

    def draw(self):
        self.display.fill((0, 0, 0))
        self.gui_group.draw(self.display)
        for btn_key in self.btns:
            self.display.blit(self._mgr.get(btn_key).image, self._mgr.get(btn_key).rect)
        self.active_image_group.draw(self.display)
        self.display.blit(self._scroll_indicator.image, self._scroll_indicator.rect)
        if self.preview16 is not None:
            self.display.blit(self.preview16.image, self.preview16.rect)
        if self.preview32 is not None:
            self.display.blit(self.preview32.image, self.preview32.rect)
        if self.preview64 is not None:
            self.display.blit(self.preview64.image, self.preview64.rect)
        if self.preview_mouse_over is not None:
            self.display.blit(self.preview_mouse_over.image, self.preview_mouse_over.rect)
        pygame.display.update()

    def load_images(self):
        img_dir_contents = os.listdir(LIST_IMAGE_DIR)
        key = 0
        for raw_image in img_dir_contents:
            img_path = os.path.join(LIST_IMAGE_DIR, raw_image)
            if os.path.isfile(img_path):
                img = pygame.image.load(img_path).convert()
                img.set_colorkey(TRANSPARENCY_COLOR)  # convert magenta to alpha
                self._images.add("{}".format(key), img)
                key += 1
                self._image_count += 1
        print("Loaded {} images from {}".format(self._image_count, LIST_IMAGE_DIR))

    def build_lower_gui(self, scroll=0):
        self.active_image_group.empty()
        if not self._mgr.has('lower_image_area'):
            lia = pygame.sprite.Sprite()
            lia.image = pygame.Surface((544, 80))
            lia.image.fill(BUTTON_BG_COLOR)
            pygame.draw.rect(lia.image, BUTTON_BORDER_COLOR, pygame.Rect(0, 0, 544, 80), BUTTON_BORDER_WIDTH)
            lia.rect = lia.image.get_rect()
            lia.rect.topleft = 128, 220
            self._mgr.add('lower_image_area', lia)
            self.gui_group.add(lia)
        if not self._mgr.has('lower_hover_preview_area'):
            lhpa = pygame.sprite.Sprite()
            lhpa.image = pygame.Surface((80, 80))
            lhpa.image.fill(BUTTON_BG_COLOR)
            pygame.draw.rect(lhpa.image, BUTTON_BORDER_COLOR, pygame.Rect(0, 0, 80, 80), BUTTON_BORDER_WIDTH)
            lhpa.rect = lhpa.image.get_rect()
            lhpa.rect.topleft = 592, 130
            self._mgr.add('lower_hover_preview_area', lhpa)
            self.gui_group.add(lhpa)
        if not self._mgr.has('preview_16_area'):
            p16 = pygame.sprite.Sprite()
            p16.image = pygame.Surface((80, 80))
            p16.image.fill(BUTTON_BG_COLOR)
            pygame.draw.rect(p16.image, BUTTON_BORDER_COLOR, pygame.Rect(0, 0, 80, 80), BUTTON_BORDER_WIDTH)
            p16.rect = p16.image.get_rect()
            p16.rect.topleft = 128, 130
            self._mgr.add('preview_16_area', p16)
            self.gui_group.add(p16)
        if not self._mgr.has('preview_32_area'):
            p32 = pygame.sprite.Sprite()
            p32.image = pygame.Surface((80, 80))
            p32.image.fill(BUTTON_BG_COLOR)
            pygame.draw.rect(p32.image, BUTTON_BORDER_COLOR, pygame.Rect(0, 0, 80, 80), BUTTON_BORDER_WIDTH)
            p32.rect = p32.image.get_rect()
            p32.rect.topleft = 228, 130
            self._mgr.add('preview_32_area', p32)
            self.gui_group.add(p32)
        if not self._mgr.has('preview_64_area'):
            p64 = pygame.sprite.Sprite()
            p64.image = pygame.Surface((80, 80))
            p64.image.fill(BUTTON_BG_COLOR)
            pygame.draw.rect(p64.image, BUTTON_BORDER_COLOR, pygame.Rect(0, 0, 80, 80), BUTTON_BORDER_WIDTH)
            p64.rect = p64.image.get_rect()
            p64.rect.topleft = 328, 130
            self._mgr.add('preview_64_area', p64)
            self.gui_group.add(p64)
        orig_x = self._mgr.get('lower_image_area').rect.x+16
        start_x = orig_x
        start_y = self._mgr.get('lower_image_area').rect.y+8
        for j in range(0, 3):
            for k in range((scroll+j)*32, ((scroll+j+1)*32)-1):
                img = self._images.get("{}".format(k))
                if img is not None:
                    img_item = ImageItem(img, start_x, start_y)
                    self.active_image_group.add(img_item)
                    start_x += 16
            start_y += 24
            start_x = orig_x
        # scroll indicator
        # self._scroll_indicator = ScrollPoint(pygame.Rect(128, 520, 16, 16), (self._image_count//32)+1)

    def build_gui_buttons(self):
        self._mgr.add("btn_undo", Button("undo", "Undo Last", 464, 40, 96, 32, self.undo_last))
        self._mgr.add("btn_save", Button("save", "Save", 240, 40, 96, 32, self.save_current_image))
        self._mgr.add("btn_clear", Button("clear", "Clear", 352, 40, 96, 32, self.clear_preview))
        self._mgr.add("btn_quit", Button("quit", "Quit", 128, 40, 96, 32, self.trigger_quit))
        self._mgr.add("btn_scroll_up", Button("up", "Up", 680, 220, 48, 32, self.scroll_up))
        self._mgr.add("btn_scroll_down", Button("down", "Down", 680, 260, 48, 32, self.scroll_down))
        self._mgr.add("ph", Button("ph", "Image Name: (Not Implemented)", 128, 88, 350, 32))

    def trigger_quit(self):
        self.running = False

    def clear_preview(self):
        self.preview16 = None
        self.preview32 = None
        self.preview64 = None

    def update_preview(self):
        self.clear_preview()
        self.preview16 = PreviewImage(self.img.image, 160, 162, 1)
        self.preview32 = PreviewImage(self.img.image, 252, 154, 2)
        self.preview64 = PreviewImage(self.img.image, 336, 138, 4)

    def scroll_to(self, point):
        self._scroll = point
        if self._scroll < 0:
            self._scroll = 0
        if self._scroll > self._image_count // 32:
            self._scroll = self._image_count // 32
        self._update_gui = True

    def scroll_up(self):
        self._scroll -= 1
        self._scroll_indicator.scroll(-1)
        if self._scroll < 0:
            self._scroll = 0
        self._update_gui = True

    def scroll_down(self):
        self._scroll += 1
        self._scroll_indicator.scroll(1)
        if self._scroll > self._image_count // 32:
            self._scroll = self._image_count // 32
        self._update_gui = True

    def save_current_image(self):
        p = get_save_image_path()
        print("Attempting to save image to {}".format(p))
        pygame.image.save(self.img.image, p)
        self.clear_preview()

    def undo_last(self):
        self.img.undo()
        self.update_preview()
