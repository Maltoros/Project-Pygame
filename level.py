import pygame
from hitbox import AttackHitbox
from tile import Tile
from player import Player
from enemy import Enemy
from settings import TILESIZE, debug
from camera import Camera

class Level:
    def __init__(self, stage, surface):
        self.displaySurface = surface
        self.stage = stage
        self.tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.worldShift = pygame.math.Vector2(0, 0)
        self.camera = Camera(len(self.stage[0])*TILESIZE, len(self.stage)*TILESIZE)

    def setupLevel(self, layout):
        for rowIndex, row in enumerate(layout):
            for colIndex, cell in enumerate(row):
                x = colIndex * TILESIZE
                y = rowIndex * TILESIZE
                if cell == '1':
                    tile = Tile((x, y), TILESIZE)
                    self.tiles.add(tile)
                if cell == 'P':
                    playerSprite = Player((x, y), self.displaySurface)
                    self.player.add(playerSprite) 
                if cell == 'D':
                    enemySprite = Enemy((x, y))
                    self.enemies.add(enemySprite)
                    

    def horizontalMoveCollision(self):
        player = self.player.sprite
        if abs(player.vel.x) > 0.5:   
            player.hitbox.x += player.vel.x + 0.5 * player.acc.x

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.hitbox):
                if player.vel.x < 0:
                    player.hitbox.left = sprite.rect.right
                elif player.vel.x > 0:
                    player.hitbox.right = sprite.rect.left
        
    def verticalMoveCollision(self):
        player = self.player.sprite
        player.hitbox.y += player.vel.y + 0.5 * player.acc.y

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.hitbox):
                if player.vel.y > 0:
                    player.hitbox.bottom = sprite.rect.top
                    player.vel.y = 0
                    player.onGround = True
                    player.canJump, player.canDoubleJump = True, True
                elif player.vel.y < 0:
                    player.hitbox.top = sprite.rect.bottom
                    player.vel.y = 0 
                    player.onCeilling = True
 
        if player.onGround and player.vel.y < 0 or player.vel.y > 1:
            player.onGround = False
        if player.onCeilling and player.vel.y > 0:
            player.OnCeilling = False
    
    def checkCollision(self):
        attackHitboxes = self.player.sprite.attackHitboxes
        if attackHitboxes:
            for attackHitbox in attackHitboxes:
                collisionSprite = pygame.sprite.spritecollide(attackHitbox, self.enemies, False)
                print(collisionSprite)
                if collisionSprite:
                    for targetSprite in collisionSprite:
                        targetSprite.kill()

    def run(self):
        self.displaySurface.fill((128, 115, 112))
        #camera
        self.camera.update(self.player.sprite)

        #level tiles
        for sprite in self.tiles:
            self.displaySurface.blit(sprite.image, self.camera.apply(sprite))
        
        #enemies
        for sprite in self.enemies:
            self.displaySurface.blit(sprite.image, self.camera.apply(sprite))

        #player
        self.player.update()
        self.displaySurface.blit(self.player.sprite.image, self.camera.apply(self.player.sprite))
        self.horizontalMoveCollision()
        self.verticalMoveCollision()
        self.checkCollision()
        debug(self.displaySurface, self.player.sprite.attackHitboxes)
        debug(self.displaySurface, self.player.sprite.rect.midbottom, 10, 30)
        