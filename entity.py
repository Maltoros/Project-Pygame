import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, surface):
        super().__init__()
        #animation
        self.displaySurface = surface
        self.frameIndex = 0
        self.animationSpeed = 0.15

        #movement
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.canJump = True
        self.canDoubleJump = True

        #status-animations
        self.status = 'idle'
        self.facingRight = True
        self.onGround = False
        self.onCeilling = False
        self.onLeft = False
        self.onRight = False

        #status-gameplay
        self.alive = True
        self.hasIFrames = False
        self.iFramesCD = 500
        self.hitTime = 0
        self.hit = False

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
    
    def jump(self):
        if self.canJump and self.onGround:
            self.vel.y = -10
            self.canJump = False
        elif self.canDoubleJump:
            self.vel.y = -10
            self.canDoubleJump = False

    def cooldowns(self):
        self.hit = False
        currentTime = pygame.time.get_ticks()
        if self.attacking:
            if currentTime - self.attackTime >= self.attackCD:
                self.attacking = False
                self.attackHitboxes.empty()
        if self.casting:
            if currentTime - self.castTime >= self.castCD:
                self.casting = False
        if self.hasIFrames:
            self.hit = False
            if currentTime - self.hitTime >= self.iFramesCD:
                self.hasIFrames = False


    def loseHP(self, damage):
        if not self.hasIFrames and self.alive:
            self.hit = True 
            self.hasIFrames = True
            self.hitTime = pygame.time.get_ticks()
            self.hp -= damage
            if self.hp <= 0:
                self.alive = False

    def drawing(self, surface, scrolling):
        x = int(self.rect.x - scrolling.x)
        y = int(self.rect.y - scrolling.y)
        surface.blit(self.image, (x, y))