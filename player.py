from ctypes.wintypes import MAX_PATH
import pygame
from os import path
from hitbox import AttackHitbox, PlayerSpellHitbox
from settings import GRAVITY, ACC, FRICTION, SCREENCENTER, importFolder
from entity import Entity

class Player(Entity):
    def __init__(self, pos, surface):
        super().__init__(surface)
        
        #animation
        self.importCharacterAssets()
        self.image = self.animations['idle'][self.frameIndex]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(pos, (10, 17))

        #dust particles
        self.importDustParticles()
        self.dustFrameIndex = 0
        self.dustAnimSpeed = 0.15

        #playerattack
        self.attackHitboxes = pygame.sprite.Group()
        self.canAttack = True
        self.attacking = False
        self.attackDuration = 500
        self.attackCD = 1000
        self.attackTime = 0
        #playermagic
        self.canCast = True
        self.casting = False
        self.castDuration = 200
        self.castCD = 1000
        self.castTime = 0
        self.spellHitboxes = pygame.sprite.Group()

        #playerstats
        self.maxHp = 10
        self.hp = self.maxHp
        self.maxMana = 9
        self.mana = self.maxMana
        self.spellUnlock = False
        self.damage = 3
        self.magicDamage = 9

    def importCharacterAssets(self):
        characterPath = path.join('Assets','player')
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'casting':[],'death':[],'hit':[],'attack':[]}
        
        for animation in self.animations.keys():
            fullPath = path.join(characterPath,animation)
            self.animations[animation] = importFolder(fullPath)

    def importDustParticles(self):
        self.dustRunParticles = importFolder(path.join('Assets','player','dust_particles', 'run'))

    def runDustAnimate(self):
        if self.status == 'run' and self.onGround:
            #loop over frame index
            self.dustFrameIndex += self.dustAnimSpeed
            if self.dustFrameIndex >= len(self.dustRunParticles):
                self.dustFrameIndex = 0
            
            dustParticle = self.dustRunParticles[int(self.dustFrameIndex)]
            if self.facingRight:
                self.displaySurface.blit(pygame.transform.scale(dustParticle, (5,5)), (SCREENCENTER + pygame.math.Vector2(-7, 11)))
            else:
                flippedImage = pygame.transform.flip(dustParticle, True, False)
                self.displaySurface.blit(pygame.transform.scale(flippedImage , (5, 5)), (SCREENCENTER + pygame.math.Vector2(12, 11)))

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

        if self.casting:
            self.canCast = False
            if currentTime - self.castTime >= self.castDuration:
                self.casting = False

        if not self.canCast:
            if currentTime - self.castTime >= self.castCD:
                self.canCast = True
    

        if self.hasIFrames:
            self.hit = False
            if currentTime - self.hitTime >= self.iFramesCD:
                self.hasIFrames = False
    

    def inputs(self):
        #apply gravity
        self.acc = pygame.math.Vector2(0, GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            if not self.attacking and not self.casting:
                self.acc.x = ACC
                self.facingRight = True
            else:
                self.acc.x = ACC/2
        elif keys[pygame.K_a]:
            if not self.attacking and not self.casting:
                self.acc.x = -ACC
                self.facingRight = False
            else:
                self.acc.x = -ACC/2
        else:    
            self.acc.x = 0
            
        #apply friction
        self.acc.x += self.vel.x * FRICTION
        #equations of motion
        self.vel += self.acc

    def attack(self):
        self.attacking = True
        self.attackTime = pygame.time.get_ticks()
        if self.facingRight:
            vec1 = pygame.math.Vector2(5, -28)
        else:
            vec1 = pygame.math.Vector2(-25, -28)
        #creating attackhitboxes
        attackHitbox = AttackHitbox(pygame.Rect((0, 0), (20, 28)), self.hitbox.midbottom + vec1)
        self.attackHitboxes.add(attackHitbox)

    def magic(self):
        if self.spellUnlock and self.mana >= 3:
            self.casting = True
            self.castTime = pygame.time.get_ticks()  
            self.mana -= 3
            spellHitbox = PlayerSpellHitbox(self.hitbox.center, self.facingRight, 'LaserBall')
            self.spellHitboxes.add(spellHitbox)
    
    def getStatus(self):
        if not self.alive:
            self.status = 'death'
        elif self.hit:
            self.status = 'hit'
        elif self.attacking:
            self.status = 'attack'
        elif self.casting:
            self.status = 'casting'
            #morecode to end the game?
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

    def update(self):
        self.inputs()
        self.getStatus()
        self.animate()
        self.runDustAnimate()
        self.cooldowns()

        if self.onGround:
            self.canJump, self.canDoubleJump = True, True