import pygame
from os import path
from settings import SWITCHSTATESOUND, UNLOCKPASSAGESOUND

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, imagename, breakable = False):#groups => sprite group it should be part of
        super().__init__()
        self.displaySurface = surface
        self.image = pygame.image.load(path.join('Assets','tiles', imagename+'.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos) 
        self.breakable = breakable

    def drawing(self, scrolling):
        x = int(self.rect.x - scrolling.x)
        y = int(self.rect.y - scrolling.y)
        self.displaySurface.blit(self.image, (x, y))

class TrapTile(Tile):
    def __init__(self, pos, surface, imagename, breakable = False):
        super().__init__(pos, surface, imagename, breakable)
        self.damage = 3
        self.hitbox = pygame.Rect(pos[0], pos[1]+5, 16, 11)

class Switch(Tile):
    def __init__(self, pos, surface, imagename, breakable = False):
        super().__init__(pos, surface, imagename, breakable)
        self.state = False
        self.switchCD = 500
        self.switchedTime = 0
        self.hit = False

    def switchState(self):
        if not self.hit:
            SWITCHSTATESOUND.play(0)
            self.hit = True
            self.switchedTime = pygame.time.get_ticks()
            if not self.state:
                self.state = True
            else:
                self.state = False

        currentTime = pygame.time.get_ticks()
        if currentTime - self.switchedTime >= self.switchCD:
            self.hit = False
        
    
    def update(self):
        if self.state:
            self.image = pygame.image.load(path.join('Assets','tiles','switchOn.png'))
        else:
            self.image = pygame.image.load(path.join('Assets','tiles','switchOff.png'))

class ActivatedTile(Tile):
    def __init__(self, pos, surface, imagename, switchesGroup, breakable = False):
        super().__init__(pos, surface, imagename, breakable)
        self.triggeringSwitches = switchesGroup

    def update(self):
        triggers = []
        for switch in self.triggeringSwitches:
            triggers.append(switch.state)
        if all(triggers):
            UNLOCKPASSAGESOUND.play(0)
            self.kill()

         


