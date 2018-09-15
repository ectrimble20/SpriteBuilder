from os import path
from os import listdir
import pygame
from time import time
from random import randint

VERSION_MAJOR = 0
VERSION_MINOR = 1
VERSION_BUILD = 0

CAPTION = "SpriteBuilder: {}.{}.{}".format(VERSION_MAJOR, VERSION_MINOR, VERSION_BUILD)

pygame.init()
pygame.font.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT

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
# BDR - border
# CLR - color
# BG - background
# HVR - hover (mouse over)
GUI_BDR_CLR = 255, 255, 255
GUI_BDR_WIDTH = 1
GUI_FONT_CLR = 255, 255, 255
GUI_BG_CLR = 90, 90, 90
GUI_BDR_CLR_HVR = 128, 128, 128
GUI_BG_CLR_HVR = 30, 30, 30
GUI_FONT_CLR_HVR = 225, 225, 225

# Key mods, these are mods for cap/shift
CAPS_ON = pygame.KMOD_CAPS
SHIFT_DOWN = pygame.KMOD_LSHIFT | pygame.KMOD_RSHIFT


def get_save_image_path():
    return path.join(CREATED_IMAGE_DIR, "{}.{}.png".format(int(time()), randint(1000, 9999)))


def get_dir_contents(d):
    if path.isdir(d):
        return listdir(d)
    else:
        raise RuntimeError("Directory expected at {} is not a directory".format(d))
