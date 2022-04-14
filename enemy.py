import pygame, os
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos):#groups => sprite group it should be part of
        super().__init__()
        self.image = pygame.image.load(os.path.join('Assets','player2','idle','0.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos) 

