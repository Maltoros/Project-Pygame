import pygame, os
from hitbox import AttackHitbox, MagicHitbox
from settings import *
vec = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface):
        super().__init__()
        #animation
        self.displaySurface = surface
        self.importCharacterAssets()
        self.frameIndex = 0
        self.animationSpeed = 0.15
        self.image = self.animations['idle'][self.frameIndex]
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(pos, (10, 17))

        #dust particles
        self.importDustParticles()
        self.dustFrameIndex = 0
        self.dustAnimSpeed = 0.15

        #playermovement
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.canJump = True
        self.canDoubleJump = True

        #playerstatus
        self.status = 'idle'
        self.facingRight = True
        self.onGround = False
        self.onCeilling = False
        self.onLeft = False
        self.onRight = False

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
    
    def cooldowns(self):
        currentTime = pygame.time.get_ticks()
        if self.attacking:
            if currentTime - self.attackTime >= self.attackCD:
                self.attacking = False
                self.attackHitboxes.empty()
        if self.casting:
            if currentTime - self.castTime >= self.castCD:
                self.casting = False
        if self.hit:
            if currentTime - self.hitTime >= self.iframesCD:
                self.hit = False

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
    
    def loseHP(self, damage):
        if not self.hit and self.alive:
            self.hitTime = pygame.time.get_ticks()
            self.hp -= damage
            if self.hp < 0:
                self.alive = False
            self.hit = True

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