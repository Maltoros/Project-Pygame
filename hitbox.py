import pygame
from os import path

class AttackHitbox(pygame.sprite.Sprite):
    def __init__(self, rect, attackerPos):
        super().__init__()
        self.rect = rect.move(attackerPos)

class MagicHitbox(pygame.sprite.Sprite):
    def __init__(self, attackerPos, facingRight):
        super().__init__()
        self.image = pygame.image.load(path.join('Assets','player','Laserball.png'))
        self.rect = self.image.get_rect(midleft = attackerPos + pygame.math.Vector2(5, 0))
        self.goingRight = facingRight
        self.velx = 10

    def update(self):
        if self.goingRight:
            self.rect.x += self.velx
        else:
            self.rect.x -= self.velx
