import pygame, os
from settings import *
from entity import Entity
dimensions = {'greendude':(20, 31)}
class Enemy(Entity):
    def __init__(self, pos, surface, monsterType):#groups => sprite group it should be part of
        super().__init__(surface)

        #animation
        self.archetype = monsterType
        self.importCharacterAssets()
        self.image = self.animations['idle'][self.frameIndex]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(pos, dimensions[self.archetype])
 
        #attack
        self.attackAnimationIndex = 0
        self.attackHitboxes = pygame.sprite.Group()
        self.attacking = False
        self.attackCD = 500
        self.attackTime = 0
        self.casting = False
        self.castCD = 200
        self.castTime = 0
        self.magicHitboxes = pygame.sprite.Group()

        #playerstats
        self.hp = 10
        self.mana = 9
        self.magicUnlock = True
        self.damage = 5
        self.alive = True
        self.iframesCD = 500
        self.hitTime = 0
        self.hit = False

    def importCharacterAssets(self):
        characterPath = os.path.join('Assets','enemies', self.archetype)
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'death':[],'attack':[]}
        
        for animation in self.animations.keys():
            fullPath = os.path.join(characterPath,animation)
            self.animations[animation] = importFolder(fullPath)

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