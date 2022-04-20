import pygame
from os import path
from hitbox import MagicHitbox
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
        self.background = pygame.transform.scale(pygame.image.load(path.join('Assets','background','0.png')),(600, 400))

    def setupLevel(self, layout):
        for rowIndex, row in enumerate(layout):
            for colIndex, cell in enumerate(row):
                x = colIndex * TILESIZE
                y = rowIndex * TILESIZE
                if cell == '1':
                    tile = Tile((x, y))
                    self.tiles.add(tile)
                if cell == 'P':
                    playerSprite = Player((x, y), self.displaySurface)
                    self.player.add(playerSprite) 
                if cell == 'G':
                    enemySprite = Enemy((x, y), self.displaySurface, 'greendude', self)
                    self.enemies.add(enemySprite)

    def playerUI(self):
        player = self.player.sprite

        life = pygame.Rect(10, 10, player.hp*7, 10)
        lifeBg = pygame.Rect(9, 9, 72, 12)
        pygame.draw.rect(self.displaySurface, 'black', lifeBg)
        pygame.draw.rect(self.displaySurface, 'red', life)

        mana = pygame.Rect(10, 25, player.mana*7, 10)
        manaBg = pygame.Rect(9, 24, 65, 12)
        pygame.draw.rect(self.displaySurface, 'black', manaBg)
        pygame.draw.rect(self.displaySurface, 'blue', mana)   

    def horizontalMoveCollision(self, entity):
        if abs(entity.vel.x) > 0.5:   
            entity.hitbox.x += entity.vel.x + 0.5 * entity.acc.x

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(entity.hitbox):
                if entity.vel.x < 0:
                    entity.hitbox.left = sprite.rect.right
                elif entity.vel.x > 0:
                    entity.hitbox.right = sprite.rect.left
        
    def verticalMoveCollision(self, entity):
        entity.hitbox.y += entity.vel.y + 0.5 * entity.acc.y

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(entity.hitbox):
                if entity.vel.y > 0:
                    entity.hitbox.bottom = sprite.rect.top
                    entity.vel.y = 0
                    entity.onGround = True
                elif entity.vel.y < 0:
                    entity.hitbox.top = sprite.rect.bottom
                    entity.vel.y = 0 
                    entity.onCeilling = True
 
        if entity.onGround and entity.vel.y < 0 or entity.vel.y > 1:
            entity.onGround = False
        if entity.onCeilling and entity.vel.y > 0:
            entity.OnCeilling = False
    
    def checkCollision(self):
        player = self.player.sprite
        attackHitboxes = player.attackHitboxes
        magicHitboxes = player.magicHitboxes
        if attackHitboxes:
            for attackHitbox in attackHitboxes:
                for enemy in self.enemies:
                    if attackHitbox.rect.colliderect(enemy.hitbox):
                        enemy.loseHP(player.damage)

        if magicHitboxes:
            for magicHitbox in magicHitboxes:
                for enemy in self.enemies:
                    if magicHitbox.rect.colliderect(enemy.hitbox):
                        magicHitbox.kill()
                        enemy.loseHP(player.magicDamage)

        for enemy in self.enemies:
            xOffset = player.hitbox.centerx - enemy.hitbox.centerx
            if enemy.hit == False and enemy.alive:
                if player.hitbox.colliderect(enemy.hitbox):
                    player.loseHP(enemy.damage)
                    if xOffset > 0:
                        player.vel += pygame.math.Vector2(5, -2)
                    else:
                        player.vel += pygame.math.Vector2(-5, -2)
    
    def run(self):
        self.displaySurface.fill((128, 115, 112))
        self.displaySurface.blit(self.background, (0, 0))
        #camera
        self.camera.update(self.player.sprite)

        #level tiles
        for sprite in self.tiles:
            self.displaySurface.blit(sprite.image, self.camera.apply(sprite))
        
        #player
        self.player.update()
        self.displaySurface.blit(self.player.sprite.image, self.camera.apply(self.player.sprite))
        self.horizontalMoveCollision(self.player.sprite)
        self.verticalMoveCollision(self.player.sprite)
        self.checkCollision()
        self.playerUI()

        #magic
        for sprite in self.player.sprite.magicHitboxes:
            sprite.update()
            self.displaySurface.blit(sprite.image, self.camera.apply(sprite))

        #enemies
        for sprite in self.enemies:
            debug(self.displaySurface, sprite.vel, x = 150, y = 70)
            debug(self.displaySurface, sprite.acc, x = 150, y = 150)
            sprite.update()
            self.displaySurface.blit(sprite.image, self.camera.apply(sprite))
            self.horizontalMoveCollision(sprite)
            self.verticalMoveCollision(sprite)

        #debugging

    
        
        
        
        