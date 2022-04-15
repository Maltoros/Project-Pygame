import pygame
vec = pygame.math.Vector2
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frameIndex = 0
        self.animationSpeed = 0.15

        #playermovement
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.canJump = True
        self.canDoubleJump = True
