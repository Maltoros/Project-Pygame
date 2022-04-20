import pygame, os
from hitbox import AttackHitbox, MagicHitbox
from settings import *
from entity import Entity
vec = pygame.math.Vector2


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
        self.damage = 3
        self.magicDamage = 9
        self.alive = True
        self.hasIFrames = False
        self.iFramesCD = 500
        self.hitTime = 0
        self.hit = False

    def importCharacterAssets(self):
        characterPath = os.path.join('Assets','player')
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'casting':[],'death':[],'hit':[],'attack':[]}
        
        for animation in self.animations.keys():
            fullPath = os.path.join(characterPath,animation)
            self.animations[animation] = importFolder(fullPath)

    def importDustParticles(self):
        self.dustRunParticles = importFolder(os.path.join('Assets','player','dust_particles', 'run'))

    def runDustAnimate(self):
        if self.status == 'run' and self.onGround:
            #loop over frame index
            self.dustFrameIndex += self.dustAnimSpeed
            if self.dustFrameIndex >= len(self.dustRunParticles):
                self.dustFrameIndex = 0
            
            dustParticle = self.dustRunParticles[int(self.dustFrameIndex)]
            if self.facingRight:
                self.displaySurface.blit(pygame.transform.scale(dustParticle, (5,5)), (SCREENCENTER + vec(-10, 3)))
            else:
                flippedImage = pygame.transform.flip(dustParticle, True, False)
                self.displaySurface.blit(pygame.transform.scale(flippedImage , (5, 5)), (SCREENCENTER + vec(5, 3)))

    def inputs(self):
        #apply gravity
        self.acc = vec(0, GRAVITY)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.acc.x = ACC
            self.facingRight = True
        elif keys[pygame.K_a]:
            self.acc.x = -ACC
            self.facingRight = False
        else:
            self.acc.x = 0
            
        #apply friction
        self.acc.x += self.vel.x * FRICTION
        #equations of motion
        self.vel += self.acc

        if keys[pygame.K_j] and not self.attacking and not self.hit:
            self.attacking = True
            if self.facingRight:
                vec1 = vec(25, -28)
            else:
                vec1 = vec(-25, -28)
            attackHitbox = AttackHitbox(pygame.Rect((0, 0), (20, 28)), self.hitbox.midbottom + vec1)
            self.attackHitboxes.add(attackHitbox)
            self.attackTime = pygame.time.get_ticks()

    def magic(self):
        if self.magicUnlock:
            self.casting = True
            self.castTime = pygame.time.get_ticks()  
            if self.mana >= 3:
                self.mana -= 3
                magicHitbox = MagicHitbox(self.hitbox.center, self.facingRight)
                self.magicHitboxes.add(magicHitbox)
    
    def getStatus(self):
        if self.attacking:
            self.status = 'attack'
        elif self.casting:
            self.status = 'casting'
        elif self.hit:
            self.status = 'hit'
        elif not self.alive:
            self.status = 'death'
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
        if self.alive:
            self.inputs()
        self.getStatus()
        self.animate()
        self.runDustAnimate()
        self.cooldowns()

        if self.onGround:
            self.canJump, self.canDoubleJump = True, True