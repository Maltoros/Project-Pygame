import pygame

class AttackHitbox(pygame.sprite.Sprite):
    def __init__(self, rect, attackerPos):
        super().__init__()
        self.rect = rect.move(attackerPos)

