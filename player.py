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
        self.damage = 5
        self.alive = True
        self.iframesCD = 500
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

        if keys[pygame.K_j] and not self.attacking:
            self.attacking = True
            self.attackTime = pygame.time.get_ticks()

    def createAttackHitbox(self):
        if self.attacking:
            self.attackAnimationIndex += self.animationSpeed

            if self.facingRight:
                vec1, vec2, vec3 = vec(0, -14), vec(0, -5), vec(0, 3)
            else:
                vec1, vec2, vec3 = vec(-25,-14), vec(-25, -5), vec(-25, 3)
            attacks = attacksRects[int(self.attackAnimationIndex)]
            if int(self.attackAnimationIndex) == 2:
                attackHitbox = AttackHitbox(pygame.Rect(attacks), self.hitbox.center + vec1)
                self.attackHitboxes.add(attackHitbox)
            elif int(self.attackAnimationIndex) == 3:
                attackHitbox = AttackHitbox(pygame.Rect(attacks), self.hitbox.center + vec2)
                self.attackHitboxes.add(attackHitbox)
            elif int(self.attackAnimationIndex) == 4:
                attackHitbox = AttackHitbox(pygame.Rect(attacks), self.hitbox.center + vec3)
                self.attackHitboxes.add(attackHitbox)
        else:
            self.attackAnimationIndex = 0

    def magic(self):
        if self.magicUnlock:
            self.casting = True
            self.castTime = pygame.time.get_ticks()  
            if self.mana >= 3:
                self.mana -= 3
                magicHitbox = MagicHitbox(self.hitbox.center, self.facingRight)
                self.magicHitboxes.add(magicHitbox)
    
    def jump(self):
        if self.canJump and self.onGround:
            self.vel.y = -10
            self.canJump = False
        elif self.canDoubleJump:
            self.vel.y = -10
            self.canDoubleJump = False

    def update(self):
        if self.alive:
            self.inputs()
        self.getStatus()
        self.animate()
        self.runDustAnimate()
        self.cooldowns()
        self.createAttackHitbox()

        if self.onGround:
            self.canJump, self.canDoubleJump = True, True