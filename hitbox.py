import pygame

class AttackHitbox(pygame.sprite.Sprite):
    def __init__(self, rect):
        super().__init__()
        self.rect = rect
