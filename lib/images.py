from local import *
from lib.structure import Pair


class CompoundImage(object):

    def __init__(self, size=1):
        self._size = size * 16
        self._image = get_transparent_surface(self._size, self._size)
        self._layers = []
        self._scales = {}

    def change_size(self, size):
        self._size = size * 16
        self._image = self._image = get_transparent_surface(self._size, self._size)

    def add(self, layer, offset=(0, 0)):
        self._layers.append(Pair(layer, offset))
        self._build()

    def undo(self):
        if len(self._layers) > 0:
            self._layers.pop(len(self._layers)-1)
            self._build()

    def _build(self):
        self._image = get_transparent_surface(self._size, self._size)  # rebuild the image
        self._scales.clear()
        for p in self._layers:
            self._image.blit(p.first, p.second)
        # build scaled images
        for i in range(1, 5):
            tmp = get_transparent_surface(i*16, i*16)
            if i*16 != self._size:
                pygame.transform.scale(self._image, (i*16, i*16), tmp)
            else:
                tmp = self._image.copy()
            self._scales[i] = tmp

    def has_content(self):
        return len(self._layers) > 0

    def get_image(self, size=4):
        if 0 < size < 5:
            return self._scales[size]

    def reset(self):
        self._layers.clear()
        self._scales.clear()
        self._image = get_transparent_surface(self._size, self._size)


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


class OldCompoundImage(object):

    def __init__(self, size=16):
        self._images = []
        self._size = size
        self.image = None
        self._init_image()

    def change_size(self, size=16):
        if self._size != size:
            self._size = size
            self.rescale()

    def rescale(self):
        for pair in self._images:
            tmp = pygame.Surface((self._size, self._size)).convert()
            tf_scale = pair.second[0]*self._size, pair.second[1]*self._size
            pygame.transform.scale(pair.first, tf_scale, tmp)
            pair.first.blit(tmp, (0, 0))

    def _init_image(self):
        self.image = pygame.Surface((self._size, self._size)).convert()
        self.image.fill(TRANSPARENCY_COLOR)
        self.image.set_colorkey(TRANSPARENCY_COLOR)

    # TODO we need be able to scale down as well
    def add(self, img, offset=(0, 0), scale=1):
        # if scale is requested, scale the image per the request
        if scale > 1:
            tmp = pygame.Surface((img.get_rect().w*scale, img.get_rect().h*scale)).convert()
            pygame.transform.scale(img, (img.get_rect().w*scale, img.get_rect().h*scale), tmp)
            img = tmp
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
        if len(self._images) > 0:
            self._images.clear()
