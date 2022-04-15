import pygame, os
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, surface):#groups => sprite group it should be part of
        super().__init__()
        self.image = pygame.image.load(os.path.join('Assets','player','idle','0.png')).convert_alpha()
        self.rect = pygame.Rect(pos - vec(25, -21), (10, 17))
        #playermovement
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.canJump = True
        self.canDoubleJump = True

