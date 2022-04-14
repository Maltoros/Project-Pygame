from settings import SCREENHEIGHT, SCREENWIDTH
import pygame

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = - target.hitbox.centerx + int(SCREENWIDTH / 2)
        y = - target.hitbox.centery + int(SCREENHEIGHT / 2)
        self.camera = pygame.Rect(x, y, self.width, self.height)