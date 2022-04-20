import pygame
vec = pygame.math.Vector2
class Entity(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        #animation
        self.displaySurface = surface
        self.frameIndex = 0
        self.animationSpeed = 0.15

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

    def loseHP(self, damage):
        if not self.hit and self.alive:
            self.hitTime = pygame.time.get_ticks()
            self.hp -= damage
            if self.hp < 0:
                self.alive = False
            self.hit = True
