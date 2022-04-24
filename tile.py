import pygame
from os import path

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, breakable = False):#groups => sprite group it should be part of
        super().__init__()
        self.displaySurface = surface
        self.image = pygame.image.load(path.join('Assets','tiles','0.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos) 
        self.breakable = breakable

    def drawing(self, scrolling):
        x = int(self.rect.x - scrolling.x)
        y = int(self.rect.y - scrolling.y)
        self.displaySurface.blit(self.image, (x, y))

class TrapTile(Tile):
    def __init__(self, pos, surface, breakable = False):
        super().__init__(pos, surface, breakable)
        self.image = pygame.image.load(path.join('Assets','tiles','spikeUp.png'))
        self.damage = 3
        self.hitbox = pygame.Rect(pos[0], pos[1]-5, 16, 11)

class ExitLevel(Tile):
   def __init__(self, pos, surface, breakable = False):
        super().__init__(pos, surface, breakable)
        self.image = pygame.image.load(path.join('Assets','tiles','leaveLevel.png'))
         


