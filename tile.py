import pygame
from os import path

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos):#groups => sprite group it should be part of
        super().__init__()
        self.image = pygame.image.load(path.join('Assets','tiles','0.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos) 

    def drawing(self, surface, scrolling):
        x = int(self.rect.x - scrolling.x)
        y = int(self.rect.y - scrolling.y)
        surface.blit(self.image, (x, y))

