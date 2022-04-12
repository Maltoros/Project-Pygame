import pygame, os
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):#groups => sprite group it should be part of
        super().__init__()
        self.image = pygame.image.load(os.path.join('Assets','tiles','0.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos) 

