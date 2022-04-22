import pygame
from os import path
from settings import importFolder
class AttackHitbox(pygame.sprite.Sprite):
    def __init__(self, rect, attackerPos):
        super().__init__()
        self.rect = rect.move(attackerPos)

class PlayerSpellHitbox(pygame.sprite.Sprite):
    def __init__(self, attackerPos, facingRight, imgName):
        super().__init__()
        self.image = pygame.image.load(path.join('Assets','player',imgName+'.png'))
        if facingRight:
            offsetVec = pygame.math.Vector2(10, 0)
        else:
            offsetVec = pygame.math.Vector2(-10, 0)
        self.rect = self.image.get_rect(center = attackerPos + offsetVec)
        self.goingRight = facingRight
        self.vel = 5

    def drawing(self, surface, scrolling):
        x = int(self.rect.x - scrolling.x)
        y = int(self.rect.y - scrolling.y)
        surface.blit(self.image, (x, y))

    def update(self):
        if self.goingRight:
            self.rect.x += self.vel
        else:
            self.rect.x -= self.vel

class SwarmSpellHitbox(pygame.sprite.Sprite):
    def __init__(self, attackerPos, facingRight, targetCoord):
        super().__init__()
        #animation
        self.importSpellAssets()
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.status = 'idle'

        self.image = self.animations['idle'][self.frameIndex]
        self.goingRight = facingRight

        self.rect = self.image.get_rect(center = attackerPos + pygame.math.Vector2(0, -40))
        self.target = targetCoord

        self.spawnPosition = attackerPos + pygame.math.Vector2(0, -40)
        self.spawnCD = 300
        self.spawnTime = pygame.time.get_ticks()
        self.canMove = False

        self.vel = 4

    def importSpellAssets(self):
        characterPath = path.join('Assets','enemies', 'swarm')
        self.animations = {'idle':[],'moving':[]}
        
        for animation in self.animations.keys():
            fullPath = path.join(characterPath,animation)
            self.animations[animation] = importFolder(fullPath)

    def drawing(self, surface, scrolling):
        x = int(self.rect.x - scrolling.x)
        y = int(self.rect.y - scrolling.y)
        surface.blit(self.image, (x, y))

    def animate(self):
        animation = self.animations[self.status]
        #loop over frame index
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0
        
        image = animation[int(self.frameIndex)]
        if self.goingRight:
            self.image = image
        else:
            flippedImage = pygame.transform.flip(image, True, False)
            self.image = flippedImage
    
    

    def moveTowardPlayer(self):
        if self.goingRight:
            self.rect.x += self.vel
        else:
            self.rect.x -= self.vel

        if self.target[1] == self.rect.y:
            return
        else:
            if self.target[1] < self.rect.y:
                self.rect.y -= self.vel/4
            elif self.target[1] > self.rect.y:
                self.rect.y += self.vel/4
            


    def update(self):
        self.animate()
        currentTime = pygame.time.get_ticks()

        if currentTime - self.spawnTime >= self.spawnCD:
            self.canMove = True
            self.status = 'moving'
        if self.canMove:
            self.moveTowardPlayer()