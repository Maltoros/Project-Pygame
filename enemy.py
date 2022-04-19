import pygame, os
from settings import *
dimensions = {'greendude':(20, 31)}
class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, surface, monsterType):#groups => sprite group it should be part of
        super().__init__()
        self.displaySurface = surface
        self.type = monsterType
        self.importCharacterAssets()
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.image = self.animations['idle'][self.frameIndex]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(pos, dimensions[self.type])
        self.mask = pygame.mask.from_surface(self.image)
        #movement
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.canJump = True
        self.canDoubleJump = True

        #status
        self.status = 'idle'
        self.facingRight = True
        self.onGround = False
        self.onCeilling = False
        self.onLeft = False
        self.onRight = False

        #attack
        self.attackAnimationIndex = 0
        self.attackHitboxes = pygame.sprite.Group()
        self.attacking = False
        self.attackCD = 500
        self.attackTime = 0

    def importCharacterAssets(self):
        characterPath = os.path.join('Assets','enemies',self.type)
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'death':[],'attack':[]}
        
        for animation in self.animations.keys():
            fullPath = os.path.join(characterPath,animation)
            self.animations[animation] = importFolder(fullPath)

    def animate(self):
        animation = self.animations[self.status]
        #loop over frame index
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            self.frameIndex = 0
        
        image = animation[int(self.frameIndex)]
        if self.facingRight:
            self.image = image
        else:
            flippedImage = pygame.transform.flip(image, True, False)
            self.image = flippedImage

        #set the rect
        self.rect.midbottom = self.hitbox.midbottom

    def getStatus(self):
        if self.attacking:
            self.status = 'attack'
        else:
            if self.vel.y < 0:
                self.status = 'jump'
            elif self.vel.y > 1:
                self.status = 'fall'
            else:
                if self.vel.x > 1 or self.vel.x < - 1:
                    self.status = 'run'
                else:
                    self.status = 'idle'

    def moving(self):
        pass
    def update(self):
        #apply gravity
        self.acc = vec(0, GRAVITY)
         #apply friction
        self.acc.x += self.vel.x * FRICTION
        #equations of motion
        self.vel += self.acc

        self.getStatus()
        self.animate()