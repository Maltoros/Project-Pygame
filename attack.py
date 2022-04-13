import pygame, os
from settings import SCREENHEIGHT, SCREENWIDTH
vec = pygame.math.Vector2
SCREENCENTER = (SCREENWIDTH / 2, SCREENHEIGHT / 2)

class Attack(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.player = player
        #self.dmgHitboxes = pygame.sprite.Group()
        self.dmgHitboxes = []
        self.attackAnimationIndex = 0
        self.attackAnimationSpeed = 0.15
        self.attackAnimationsRight = [0, 0, ( (SCREENCENTER + vec(-3, -22) ), (SCREENCENTER + vec(27, -10) ), (SCREENCENTER + vec(27, 0) ), (SCREENCENTER + vec(17, 5) ), (SCREENCENTER + vec(10, 5) ), (SCREENCENTER + vec(5, 5) ) ), ((SCREENCENTER + vec(7, 3) ), (SCREENCENTER + vec(20, -13) ), (SCREENCENTER + vec(24, -6) ), (SCREENCENTER + vec(20, 1) ), (SCREENCENTER + vec(6, 1) ) ), 0, 0 ]
        self.attackAnimationsLeft = [0, 0, ( (SCREENCENTER + vec(3, -22) ), (SCREENCENTER + vec(-27, -10) ), (SCREENCENTER + vec(-27, 0) ), (SCREENCENTER + vec(-17, 5) ), (SCREENCENTER + vec(-10, 5) ) ), ( (SCREENCENTER + vec(-5, 5) ), (SCREENCENTER + vec(-7, 3) ), (SCREENCENTER + vec(-20, -13) ), (SCREENCENTER + vec(-24, -6) ), (SCREENCENTER + vec(-20, 1) ), (SCREENCENTER + vec(-6, 1) ) ), 0, 0]
    
    def attacking(self):
        player = self.player 
        if player.attacking:
            self.attackAnimationIndex += self.attackAnimationSpeed

            if self.attackAnimationIndex >= len(self.attackAnimationsRight):
                self.attackAnimationIndex = 0

            if player.facingRight:
                attackRight = self.attackAnimationsRight[int(self.attackAnimationIndex)]
                if 2 <= int(self.attackAnimationIndex) <= 3 :
                    self.dmgHitboxes.append(pygame.draw.polygon(player.displaySurface, 'red', attackRight))
            else:
                attackLeft = self.attackAnimationsLeft[int(self.attackAnimationIndex)]
                if 2 <= int(self.attackAnimationIndex) <= 3 :
                    self.dmgHitboxes.append(pygame.draw.polygon(player.displaySurface, 'red', attackLeft))
        else:
            self.dmgHitboxes.clear()

    def update(self):
        self.attacking()
