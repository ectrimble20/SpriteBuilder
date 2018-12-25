from os import path
from os import listdir
import pygame
from time import time
from random import randint
from lib.colors import *

VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_BUILD = 4

CAPTION = "SpriteBuilder: {}.{}.{}".format(VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD)

pygame.init()
pygame.font.init()
pygame.key.set_repeat(100, 100)  # we need this to handle typing properly

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT

HORIZONTAL_CENTER = SCREEN_WIDTH // 2
VERTICAL_CENTER = SCREEN_HEIGHT // 2
SCREEN_CENTER = HORIZONTAL_CENTER, VERTICAL_CENTER


IMAGE_DIR = "images"
# images create by the user
CREATED_IMAGE_DIR = path.join(IMAGE_DIR, "created")
# images loaded into the program
LIST_IMAGE_DIR = path.join(IMAGE_DIR, "list")
# images used by the program
SYS_IMAGE_DIR = path.join(IMAGE_DIR, "sys")

_sys_img_list = [
    'arrowDown', 'arrowLeft', 'arrowRight', 'arrowUp', 'cross', 'down', 'import', 'larger', 'next',
    'previous', 'return', 'save', 'scrollVertical', 'smaller', 'trashcanOpen', 'wrench'
]
SYS_IMAGES = {}

# Compound saved image file  NOT IMPLEMENTED YET
COMPOUND_IMAGE_FILE = path.join(CREATED_IMAGE_DIR, "compound.dat")

# Set magenta as the alpha color
TRANSPARENCY_COLOR = MAGENTA

FONT_FILE = "trebuc.ttf"
FONT_24 = pygame.font.Font(FONT_FILE, 24)
FONT_16 = pygame.font.Font(FONT_FILE, 16)
FONT_12 = pygame.font.Font(FONT_FILE, 12)

# 1.0.4 new font objects are dynamically generated and cached
# the old objects are still there for backwards compatibility
FONT = {}

# GUI Colors
# BDR - border
# CLR - color
# BG - background
# HVR - hover (mouse over)
GUI_BDR_WIDTH = 1
GUI_FONT_CLR = WHITE_SMOKE
GUI_FONT_CLR_HVR = ANTIQUE_WHITE
GUI_BG_CLR = GRAY
GUI_BG_CLR_HVR = DIM_GREY
GUI_BDR_CLR_HVR = NAVAJO_WHITE
GUI_BDR_CLR = WHITE
GUI_TOOLTIP_PADDING = 10

# Key mods, these are mods for cap/shift
CAPS_ON = pygame.KMOD_CAPS
SHIFT_DOWN = pygame.KMOD_LSHIFT | pygame.KMOD_RSHIFT


# Positioning
POS_BTN_UNDO = pygame.Rect(HORIZONTAL_CENTER, 20, 96, 32)
POS_BTN_SAVE = pygame.Rect(HORIZONTAL_CENTER - 200, 20, 96, 32)
POS_BTN_CLEAR = pygame.Rect(HORIZONTAL_CENTER - 100, 20, 96, 32)
POS_BTN_QUIT = pygame.Rect(HORIZONTAL_CENTER - 300, 20, 96, 32)
POS_BTN_S_TOP = pygame.Rect(HORIZONTAL_CENTER + 304, 220, 48, 32)
POS_BTN_S_UP = pygame.Rect(HORIZONTAL_CENTER + 304, 260, 48, 32)
POS_BTN_S_DOWN = pygame.Rect(HORIZONTAL_CENTER + 304, 300, 48, 32)
POS_BTN_S_END = pygame.Rect(HORIZONTAL_CENTER + 304, 340, 48, 32)
POS_CTB_IMAGES = pygame.Rect(HORIZONTAL_CENTER - 272, 220, 544, SCREEN_HEIGHT - 256)
POS_CTB_MO_PV = pygame.Rect(592, 130, 80, 80)
POS_CTB_PV_16 = pygame.Rect(128, 130, 80, 80)
POS_CTB_PV_32 = pygame.Rect(228, 130, 80, 80)
POS_CTB_PV_64 = pygame.Rect(328, 130, 80, 80)
POS_TXT_IN_IMG_LABEL = pygame.Rect(220, 86, 200, 30)
POS_LABEL_FILENAME = 130, 92


def get_transparent_surface(w, h):
    img = pygame.Surface([w, h]).convert()
    img.fill(TRANSPARENCY_COLOR)
    img.set_colorkey(TRANSPARENCY_COLOR)
    return img


def get_save_image_path():
    return path.join(CREATED_IMAGE_DIR, "{}.{}.png".format(int(time()), randint(1000, 9999)))


def get_dir_contents(d):
    if path.isdir(d):
        return listdir(d)
    else:
        raise RuntimeError("Directory expected at {} is not a directory".format(d))


def load_sys_images():
    for f_name in _sys_img_list:
        full_path = path.join(SYS_IMAGE_DIR, "{}.png".format(f_name))
        i = pygame.image.load(full_path).convert_alpha()
        SYS_IMAGES[f_name] = i


def get_font(size=16):
    if size not in FONT.keys():
        FONT[size] = pygame.font.Font(FONT_FILE, size)
    return FONT[size]
