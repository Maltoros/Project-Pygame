import pygame
from hitbox import AttackHitbox
from tile import Tile
from player import Player
from enemy import Enemy
from settings import SCREENCENTER, TILESIZE, debug
from camera import Camera
rects = [pygame.Rect((0,0),(10, 7)) , pygame.Rect((0,0),(22, 27)) , pygame.Rect((0,0), (19, 15)), pygame.Rect((0,0), (14, 4))]
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
                    enemySprite = Enemy((x, y), self.displaySurface)
                    self.enemies.add(enemySprite)
                    

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
        attackHitboxes = self.player.sprite.attackHitboxes
        if attackHitboxes:
            for attackHitbox in attackHitboxes:
                hitList = pygame.sprite.spritecollide(attackHitbox, self.enemies, False)
                for enemyHit in hitList:
                    enemyHit.kill()
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
            self.horizontalMoveCollision(sprite)
            self.verticalMoveCollision(sprite)

        #player
        self.player.update()
        self.displaySurface.blit(self.player.sprite.image, self.camera.apply(self.player.sprite))
        self.horizontalMoveCollision(self.player.sprite)
        self.verticalMoveCollision(self.player.sprite)
        self.checkCollision()

        #debugging
        pygame.draw.rect(self.displaySurface, 'white', self.player.sprite.hitbox)
        debug(self.displaySurface, self.player.sprite.attackHitboxes)
    
        
        
        
        