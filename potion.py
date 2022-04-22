import pygame

class Potion(pygame.sprite.Sprite):
    def __init__(self, potionType):
        super().__init__
        self.spawnTime = pygame.time.get_ticks()
        self.image = 0
        self.rect = 0
        self.potionType = potionType
        self.pickedUp = False
        self.lifeTime = 10000

    def update(self):
        pass