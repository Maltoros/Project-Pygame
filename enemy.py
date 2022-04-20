import pygame, os
from settings import *
from entity import Entity
information = {'greendude':[(20, 31), 5, 0, 0.2], }#hitboxsize, hp, damage, speed
class Enemy(Entity):
    def __init__(self, pos, surface, monsterType, level):#groups => sprite group it should be part of
        super().__init__(surface)
        self.level = level
        self.aggro = False

        #animation
        self.archetype = monsterType
        self.importCharacterAssets()
        self.image = self.animations['idle'][self.frameIndex]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(pos, information[self.archetype][0])

        #movement
        self.speed = information[self.archetype][3]

        #attack
        self.attackHitboxes = pygame.sprite.Group()
        self.attackAnimationIndex = 0
        self.attacking = False
        self.attackCD = 500
        self.attackTime = 0
        self.casting = False
        self.castCD = 200
        self.castTime = 0

        #playerstats
        self.hp = information[self.archetype][1]
        self.mana = 0
        self.magicUnlock = False
        self.damage = information[self.archetype][2]
        self.alive = True
        self.hasIFrames = False
        self.iFramesCD = 500
        self.hitTime = 0
        self.hit = False

    def importCharacterAssets(self):
        characterPath = os.path.join('Assets','enemies', self.archetype)
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'death':[],'attack':[]}
        
        for animation in self.animations.keys():
            fullPath = os.path.join(characterPath,animation)
            self.animations[animation] = importFolder(fullPath)

    def animate(self):
        animation = self.animations[self.status]
        #loop over frame index
        self.frameIndex += self.animationSpeed
        if self.frameIndex >= len(animation):
            if not self.alive:
                self.kill()
                return
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
        elif not self.alive:
            self.status = 'death'
        else:
            if self.vel.y < 0:
                self.status = 'jump'
            elif self.vel.y > 1:
                self.status = 'fall'
            else:
                if abs(self.vel.x) > 0.2:
                    self.status = 'run'
                else:
                    self.status = 'idle'

    def moving(self):
        #apply gravity
        self.acc = vec(0, GRAVITY)
        player = self.level.player.sprite
        xOffset = player.hitbox.centerx - self.hitbox.centerx
        yOffset = player.hitbox.centery - self.hitbox.centery
        
        if self.alive:
            if abs(xOffset) <= 200 and abs(yOffset) <= 200:
                self.aggro = True
            else:
                self.aggro = False

            if self.aggro and not self.hasIFrames:
                if xOffset > 0:
                    self.facingRight = True
                    self.acc.x = self.speed
                    if xOffset < 25:
                        self.attacking = True
                    elif xOffset < 15:
                        self.acc.x = 0
                if xOffset < 0 and not self.attacking:
                    self.facingRight = False
                    self.acc.x = -self.speed
                    if xOffset > - 25:
                        self.attacking = True
                    elif xOffset > -15:
                        self.acc.x = 0

                    
            
            if self.hit:
                if xOffset > 0:
                    self.vel.x = -3
                if xOffset < 0:
                    self.vel.x = 3
                self.vel.y = -4

        #apply friction
        self.acc.x += self.vel.x * FRICTION
        #equations of motion
        self.vel += self.acc
  
    def update(self):
        self.moving()
        self.getStatus()
        self.animate()
        self.cooldowns()