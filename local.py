from os import path
import pygame
from time import time
from random import randint

pygame.init()
pygame.font.init()

IMAGE_DIR = "images"
CREATED_IMAGE_DIR = path.join(IMAGE_DIR, "created")
LIST_IMAGE_DIR = path.join(IMAGE_DIR, "list")

# Compound saved image file  NOT IMPLEMENTED YET
COMPOUND_IMAGE_FILE = path.join(CREATED_IMAGE_DIR, "compound.dat")

# Set magenta as the alpha color
TRANSPARENCY_COLOR = 255, 0, 255

FONT_FILE = "trebuc.ttf"
FONT_24 = pygame.font.Font(FONT_FILE, 24)
FONT_16 = pygame.font.Font(FONT_FILE, 16)

# GUI Colors
BUTTON_FONT_OBJECT = None
BUTTON_BORDER_COLOR = 255, 255, 255
BUTTON_BORDER_WIDTH = 1
BUTTON_TEXT_COLOR = 255, 255, 255
BUTTON_BG_COLOR = 90, 90, 90


def get_save_image_path():
    return path.join(CREATED_IMAGE_DIR, "{}.{}.png".format(int(time()), randint(1000, 9999)))
