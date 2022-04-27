from turtle import pos, position
import pygame
from settings import importFolder, bossPositions
from random import randint
from os import path

class Boss(pygame.sprite.Sprite):
    def __init__(self, pos, surface, level):
        super().__init__()
        #animation
        self.displaySurface = surface
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.status = 'idle'
        self.importCharacterAssets()
        self.image = self.animations['idle'][self.frameIndex]
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = pygame.Rect(pos, (60, 60))
        
        self.level = level

        #stats
        self.maxHp = 30
        self.hp = self.maxHp
        self.specialDamage = 2

        #status-gameplay
        self.facingRight = False
        self.alive = True
        self.hasIFrames = False
        self.iFramesCD = 500
        self.hitTime = 0
        self.hit = False
        self.location = 2

        #bossmagic
        self.specialAttackHitboxes = pygame.sprite.Group()
        self.canSpecialAttack = True
        self.specialAttack = False
        self.specialAttackDuration = 600
        self.specialAttackCD = 5000
        self.specialAttackTime = 0
    
        #bossTeleport
        self.teleporting = False
        self.canTeleport = False
        self.teleportTime = 0
        self.teleportDuration = 500
        self.teleportCD = 5000
 
    def importCharacterAssets(self):
        characterPath = path.join('Assets','enemies','boss')
        self.animations = {'idle':[],'attack':[],'death':[],'idle':[],'skill':[],'summon':[]}
        
        for animation in self.animations.keys():
            fullPath = path.join(characterPath,animation)
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
        self.hitbox.center = self.rect.center  

    def cooldowns(self):
        self.hit = False
        currentTime = pygame.time.get_ticks()

        if self.specialAttack:
            self.canSpecialAttack = False
            if currentTime - self.specialAttackTime >= self.specialAttackDuration:
                self.specialAttack = False

        if not self.canSpecialAttack:
            if currentTime - self.specialAttackTime >= self.specialAttackCD:
                self.canSpecialAttack = True

        if self.teleporting:
            self.canTeleport = False
            if currentTime - self.teleportTime >= self.teleportDuration:
                self.teleporting = False
        
        if not self.canTeleport:
            if currentTime - self.teleportTime >= self.teleportCD:
                self.canTeleport = True

        if self.hasIFrames:
            self.hit = False
            if currentTime - self.hitTime >= self.iFramesCD:
                self.hasIFrames = False

    def getStatus(self):
        if not self.alive:
            self.status = 'death'
        elif self.teleporting:
            self.status = 'skill'
        elif self.specialAttack:
            self.status = 'summon'
        else:
            self.status = 'idle'

    def createSpecialAttackHitbox(self):
        self.specialAttack = True
        self.specialAttackTime = pygame.time.get_ticks()
        summon1 = BossSummon((160, 176), self.level.player.sprite.hitbox.center)
        summon2 = BossSummon((160, 304), self.level.player.sprite.hitbox.center)
        summon3 = BossSummon((656, 176), self.level.player.sprite.hitbox.center)
        summon4 = BossSummon((656, 304), self.level.player.sprite.hitbox.center)
        self.specialAttackHitboxes.add(summon1)
        self.specialAttackHitboxes.add(summon2)
        self.specialAttackHitboxes.add(summon3)
        self.specialAttackHitboxes.add(summon4)

    def loseHP(self, damage):
        if not self.hasIFrames and self.alive:
            self.hit = True 
            self.hasIFrames = True
            self.hitTime = pygame.time.get_ticks()
            self.hp -= damage
            if self.hp <= 0:
                self.alive = False

    def changePosition(self):
        if self.canTeleport:
            self.teleportTime = pygame.time.get_ticks()
            self.teleporting = True
            newPosIndex = randint(0,4)
            if self.location == bossPositions[newPosIndex]:
                if newPosIndex == 4:
                    newPosIndex = 0
                else:
                    newPosIndex += 1
            if newPosIndex in (0,3,2):
                self.facingRight = True
            else:
                self.facingRight = False
            self.rect.center = bossPositions[newPosIndex]

    def drawing(self, scrolling):
        x = int(self.rect.x - scrolling.x)
        y = int(self.rect.y - scrolling.y)
        self.displaySurface.blit(self.image, (x, y))
    
    def update(self):
        self.getStatus()
        self.animate()
        self.changePosition()
        self.cooldowns()
        if self.canSpecialAttack:
            self.createSpecialAttackHitbox()

class BossSummon(pygame.sprite.Sprite):
    def __init__(self, spawnPosition, target):
        super().__init__()
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.status = 'idle'
        self.importSpellAssets()
        self.image = self.animations['idle'][self.frameIndex]
        self.rect = self.image.get_rect(center = spawnPosition)
        self.hitbox = pygame.Rect(0, 0, 11, 23)
        self.target = target
        self.spawnPosition = spawnPosition
        self.spawnTime = pygame.time.get_ticks()
        self.startMove = 1000
        self.endLife = 5000
        self.speed = 4
        if self.target[0] - spawnPosition[0] > 0:
            self.goingRight = False
        else:
            self.goingRight = True

    def importSpellAssets(self):
        characterPath = path.join('Assets','enemies','bossSummon')
        self.animations = {'idle':[],'moving':[]}
        
        for animation in self.animations.keys():
            fullPath = path.join(characterPath,animation)
            self.animations[animation] = importFolder(fullPath)

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
        
        self.hitbox.center = self.rect.center
    
    def moveTowardTarget(self):
        projectileVector = pygame.math.Vector2(self.spawnPosition)
        targetVector = pygame.math.Vector2(self.target)
        towards = (targetVector - projectileVector).normalize() * self.speed
        self.rect.x += towards.x
        self.rect.y += towards.y

    def drawing(self, surface, scrolling):
        x = int(self.rect.x - scrolling.x)
        y = int(self.rect.y - scrolling.y)
        surface.blit(self.image, (x, y))

    def update(self):
        self.animate()
        currentTime = pygame.time.get_ticks()
        if currentTime - self.spawnTime >= self.startMove:
            self.status = 'moving'
            self.moveTowardTarget()
        elif currentTime - self.spawnTime >= self.endLife:
            self.kill()