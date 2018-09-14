from local import *
from lib.structure import Pair


class ImageItem(pygame.sprite.Sprite):

    def __init__(self, surface, x, y):
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

    def mouse_over(self, mouse_rect):
        self.rect.colliderect(mouse_rect)


class PreviewImage(object):

    def __init__(self, surface, x, y, scale_size=2):
        self.image = surface
        self.scale = scale_size * 16
        # scale the image
        self.image = pygame.transform.scale(self.image, (self.scale, self.scale))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y


class CompoundImage(object):

    def __init__(self, size=16):
        self._images = []
        self.size = size
        self.image = None
        self._init_image()

    def _init_image(self):
        self.image = pygame.Surface((self.size, self.size)).convert()
        self.image.fill(TRANSPARENCY_COLOR)
        self.image.set_colorkey(TRANSPARENCY_COLOR)

    def add(self, img, offset=(0, 0)):
        self._images.append(Pair(img, offset))
        self.build()

    def build(self):
        self._init_image()
        for pair in self._images:
            self.image.blit(pair.first, pair.second)

    def undo(self):
        if len(self._images) > 0:
            self._images.pop(len(self._images)-1)
            self.build()

    def reset(self):
        self._images = []
