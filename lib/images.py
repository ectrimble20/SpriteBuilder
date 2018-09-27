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
