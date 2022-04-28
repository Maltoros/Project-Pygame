import pygame
from os import path
from item import Item
from random import randint
from settings import ENEMYHITSOUND, importFolder, GRAVITY, FRICTION, enemyInformation
from entity import Entity
from hitbox import AttackHitbox, ProjectileSpellHitbox

class Enemy(Entity):
    def __init__(self, pos, surface, monsterType, level):#groups => sprite group it should be part of
        super().__init__(surface)
        self.level = level

        #animation
        self.archetype = monsterType
        self.importCharacterAssets()
        self.image = self.animations['idle'][self.frameIndex]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(pos, enemyInformation[self.archetype]['size'])

        #movement
        self.monsterAcc = enemyInformation[self.archetype]['speed']

        #attack
        self.attackHitboxes = pygame.sprite.Group()
        self.canAttack = True
        self.attacking = False
        self.attackDuration = 200
        self.attackCD = 500
        self.attackTime = 0
        #special attack/magic
        self.specialAttackHitboxes = pygame.sprite.Group()
        self.canSpecialAttack = True
        self.specialAttack = False
        self.specialAttackDuration = 600
        self.specialAttackCD = 2000
        self.specialAttackTime = 0

        #stats
        self.aggro = False
        self.maxHp = enemyInformation[self.archetype]['hp']
        self.hp = self.maxHp
        self.maxMana = enemyInformation[self.archetype]['mana']
        self.mana = self.maxMana
        self.damage = enemyInformation[self.archetype]['damage']
        self.specialDamage = self.damage*2

        #drops
        self.rewardDropped = False

    def importCharacterAssets(self):
        characterPath = path.join('Assets','enemies', self.archetype)
        self.animations = enemyInformation[self.archetype]['animations']
        
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
        self.rect.midbottom = self.hitbox.midbottom    

    def moving(self):
        #apply gravity
        self.acc = pygame.math.Vector2(0, GRAVITY)
        player = self.level.player.sprite
        xOffset = int(player.hitbox.centerx - self.hitbox.centerx)
        yOffset = int(player.hitbox.centery - self.hitbox.centery)
        
        if self.alive:
            self.aggro = abs(xOffset) <= 200 and abs(yOffset) <= 100
            
            #movement if player in range
            if self.aggro and not self.hasIFrames:
                #separate melee enemies behaviours
                if yOffset < 15:
                    if self.archetype in ('hunter', 'greendude'):
                        if xOffset > 0:
                            self.facingRight = True
                            self.acc.x = self.monsterAcc
                        elif xOffset < 0:
                            self.facingRight = False
                            self.acc.x = -self.monsterAcc

                        #hunter 
                        if self.archetype == 'hunter':
                            #attacking and creating hitbox when in 30pixels
                            if abs(xOffset) < 30:
                                self.acc.x = 0
                            if abs(xOffset) < 40 and self.canAttack:
                                self.attackTime = pygame.time.get_ticks()
                                self.attacking = True
                                if self.facingRight:
                                    vec1 = pygame.math.Vector2(8, -30)
                                else:
                                    vec1 = pygame.math.Vector2(-25, -30)
                                attackHitbox = AttackHitbox(pygame.Rect((0, 0), (24, 30)), self.hitbox.midbottom + vec1)
                                self.attackHitboxes.add(attackHitbox)

                        elif self.archetype == 'greendude':
                            #uses colliding hitbox to damage the enemy
                            if abs(xOffset) < 30 and self.canAttack:
                                self.attacking = True
                            elif abs(xOffset) < 15 and abs(yOffset) < 15:
                                self.acc.x = 0

                                
                    elif self.archetype == 'summoner':
                            if xOffset > 0:
                                self.facingRight = True
                            else:
                                self.facingRight = False
                        
                            if 100 > xOffset > 0 and not self.onRight:
                                    self.vel.x += -0.2

                            elif -100 <= xOffset < 0 and not self.onLeft:
                                    self.vel.x += 0.2

                            if 300 > abs(xOffset) > 40 and self.canSpecialAttack:
                                self.createSpecialAttackHitbox(player.hitbox.midtop)
                                

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

    def createSpecialAttackHitbox(self, target):
        self.specialAttack = True
        self.specialAttackTime = pygame.time.get_ticks()
        specialAttack = ProjectileSpellHitbox(self.hitbox.center, self.facingRight, target, 'swarm')
        self.specialAttackHitboxes.add(specialAttack)

    def getStatus(self):
        if not self.alive:
            self.status = 'death'
        elif self.attacking:
            self.status = 'attack'
        elif self.specialAttack:
            if self.archetype == 'summoner':
                self.status = 'casting'
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

    def cooldowns(self):
        self.hit = False
        currentTime = pygame.time.get_ticks()

        if self.attacking:
            self.canAttack = False
            if currentTime - self.attackTime >= self.attackDuration:
                self.attacking = False
                self.attackHitboxes.empty()
        
        if not self.canAttack:
            if currentTime - self.attackTime >= self.attackCD:
                self.canAttack = True

        if self.specialAttack:
            self.canSpecialAttack = False
            if currentTime - self.specialAttackTime >= self.specialAttackDuration:
                self.specialAttack = False

        if not self.canSpecialAttack:
            if currentTime - self.specialAttackTime >= self.specialAttackCD:
                self.canSpecialAttack = True
    

        if self.hasIFrames:
            self.hit = False
            if currentTime - self.hitTime >= self.iFramesCD:
                self.hasIFrames = False

    def dropReward(self):
        if not self.rewardDropped:
            self.rewardDropped = True
            chance = randint(1,10)
            if chance in enemyInformation[self.archetype]['chance']:
                dropTable = ['Life Potion','Life Potion']
                if self.level.player.sprite.spellUnlock and self.level.player.sprite.mana != self.level.player.sprite.maxMana:
                    dropTable[1] = 'Mana Potion'
                if chance == 10:
                    reward = 'Big '
                elif chance == 9:
                    reward = 'Medium '
                else:
                    reward = 'Small '
                reward += dropTable[randint(0,1)]
                itemSprite = Item((self.rect.centerx, self.rect.centery), reward, self.displaySurface)
                self.level.items.add(itemSprite)

    def loseHP(self, damage):
        if not self.hasIFrames and self.alive:
            self.hit = True 
            self.hasIFrames = True
            self.hitTime = pygame.time.get_ticks()
            self.hp -= damage
            ENEMYHITSOUND.play(0)
            if self.hp <= 0:
                self.alive = False
                self.dropReward()

    def update(self):
        self.moving()
        self.getStatus()
        self.animate()
        self.cooldowns()

