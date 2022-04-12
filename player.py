import pygame, os
from settings import importFolder, playerAcc, playerFric, playerGrav
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
        self.damage = 5
        self.attacking = False
        self.attackCD = 500
        self.attackTime = 0

        

    def importCharacterAssets(self):
        characterPath = os.path.join('Assets','player1')
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'blocking':[],'death':[],'hit':[],'attack':[]}
        
        for animation in self.animations.keys():
            fullPath = os.path.join(characterPath,animation)
            self.animations[animation] = importFolder(fullPath)
    
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
        if self.onGround:
            #self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.canJump = True
            self.secondJump = True
        elif self.onCeilling:
            #self.rect = self.image.get_rect(midtop = self.rect.midtop)
            pass
        else:
            #self.rect = self.image.get_rect(center = self.rect.center)
            pass

    def inputs(self):
        self.acc = vec(0, playerGrav)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.acc.x = playerAcc
            self.facingRight = True
        if keys[pygame.K_a]:
            self.acc.x = -playerAcc
            self.facingRight = False
        #apply friction
        self.acc.x += self.vel.x * playerFric
        #equations of motion
        self.vel += self.acc

        if keys[pygame.K_j] and not self.attacking:
            self.attacking = True
            self.attackTime = pygame.time.get_ticks()
            self.attack()

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
    
    def attack(self):
        pass
    def magic(self):
        pass
    
    def jump(self):
        self.vel.y = -10
    
    def update(self):
        self.getStatus()
        self.inputs()
        self.cooldowns()
        self.animate()