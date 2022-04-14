import pygame, os
from hitbox import AttackHitbox
from settings import SCREENCENTER, importFolder, playerAcc, playerFric, playerGrav, attackAnimationsLeft, attackAnimationsRight
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
        self.hitbox = pygame.Rect(pos - vec(25, -21), (10, 17))

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

        #playerstats
        self.hpMax = 10
        self.currHp = self.hpMax
        

        #playerattack
        self.attackAnimationIndex = 0
        self.attackHitboxes = pygame.sprite.Group()
        self.attacking = False
        self.attackCD = 500
        self.attackTime = 0

    def importCharacterAssets(self):
        characterPath = os.path.join('Assets','player')
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'blocking':[],'death':[],'hit':[],'attack':[]}
        
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
        self.acc = vec(0, playerGrav)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.acc.x = playerAcc
            self.facingRight = True
        elif keys[pygame.K_a]:
            self.acc.x = -playerAcc
            self.facingRight = False
        else:
            self.acc.x = 0
        #apply friction
        self.acc.x += self.vel.x * playerFric
        #equations of motion
        self.vel += self.acc

        if keys[pygame.K_j] and not self.attacking:
            self.attacking = True
            self.attackTime = pygame.time.get_ticks()

        if keys[pygame.K_k] and not self.attacking:
            self.magic()                    

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
    
    def cooldowns(self):
        currentTime = pygame.time.get_ticks()
        if self.attacking:
            if currentTime - self.attackTime >= self.attackCD:
                self.attacking = False
                self.attackHitboxes.empty()

    def createAttackHitbox(self):
        attackAnimationsRight = [0, 0, ( (SCREENCENTER + vec(-3, -22) ), (SCREENCENTER + vec(27, -10) ), (SCREENCENTER + vec(27, 0) ), (SCREENCENTER + vec(17, 5) ), (SCREENCENTER + vec(10, 5) ), (SCREENCENTER + vec(5, 5) ) ), ((SCREENCENTER + vec(7, 3) ), (SCREENCENTER + vec(20, -13) ), (SCREENCENTER + vec(24, -6) ), (SCREENCENTER + vec(20, 1) ), (SCREENCENTER + vec(6, 1) ) ), 0, 0 ]
        attackAnimationsLeft = [0, 0, ( (SCREENCENTER + vec(3, -22) ), (SCREENCENTER + vec(-27, -10) ), (SCREENCENTER + vec(-27, 0) ), (SCREENCENTER + vec(-17, 5) ), (SCREENCENTER + vec(-10, 5) ) ), ( (SCREENCENTER + vec(-5, 5) ), (SCREENCENTER + vec(-7, 3) ), (SCREENCENTER + vec(-20, -13) ), (SCREENCENTER + vec(-24, -6) ), (SCREENCENTER + vec(-20, 1) ), (SCREENCENTER + vec(-6, 1) ) ), 0, 0]
        
        if self.attacking:
            self.attackAnimationIndex += self.animationSpeed

            if self.facingRight:
                attackRight = attackAnimationsRight[int(self.attackAnimationIndex)]
                if 2 <= int(self.attackAnimationIndex) <= 3 :
                    attackHitbox = AttackHitbox(pygame.draw.polygon(self.displaySurface, 'grey', attackRight))
                    self.attackHitboxes.add(attackHitbox)
            else:
                attackLeft = attackAnimationsLeft[int(self.attackAnimationIndex)]
                if 2 <= int(self.attackAnimationIndex) <= 3 :
                    attackHitbox = AttackHitbox(pygame.draw.polygon(self.displaySurface, 'grey', attackLeft))
                    self.attackHitboxes.add(attackHitbox)
        else:
            self.attackAnimationIndex = 0


    def magic(self):
        pass
    
    def jump(self):
        if self.canJump and self.onGround:
            self.vel.y = -10
            self.canJump = False
        elif self.canDoubleJump:
            self.vel.y = -10
            self.canDoubleJump = False
    
    def update(self):
        self.inputs()
        self.getStatus()
        self.animate()
        self.runDustAnimate()
        self.cooldowns()
        self.createAttackHitbox()

