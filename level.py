import pygame
from os import path
from tile import Tile
from player import Player
from enemy import Enemy
from settings import TILESIZE, debug

class Level:
    def __init__(self, surface):
        self.displaySurface = surface
        self.tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.scrolling = pygame.math.Vector2(0, 0)
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
                if cell == 'H':
                    enemySprite = Enemy((x, y), self.displaySurface, 'hunter', self)
                    self.enemies.add(enemySprite)
                if cell == 'S':
                    enemySprite = Enemy((x, y), self.displaySurface, 'summoner', self)
                    self.enemies.add(enemySprite)

    def playerUI(self):
        player = self.player.sprite

        life = pygame.Rect(10, 10, player.hp * 7, 10)
        lifeBg = pygame.Rect(9, 9, 2 + player.maxHp * 7, 12)
        pygame.draw.rect(self.displaySurface, 'black', lifeBg)
        pygame.draw.rect(self.displaySurface, 'red', life)
        if player.spellUnlock:
            mana = pygame.Rect(10, 25, player.mana * 7, 10)
            manaBg = pygame.Rect(9, 24, 2 + player.maxMana * 7, 12)
            pygame.draw.rect(self.displaySurface, 'black', manaBg)
            pygame.draw.rect(self.displaySurface, 'blue', mana)   

    def horizontalMoveCollision(self, entity):
        if abs(entity.vel.x) > 0.5:   
            entity.hitbox.x += int(entity.vel.x + 0.5 * entity.acc.x)

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(entity.hitbox):
                if entity.vel.x < 0:
                    entity.hitbox.left = sprite.rect.right
                    entity.onLeft = True
                elif entity.vel.x > 0:
                    entity.hitbox.right = sprite.rect.left
                    entity.onRight = True
        if entity.onLeft and entity.vel.x != 0:
            entity.onLeft = False
        if entity.onRight and entity.vel.x != 0:
            entity.onRight = False
        
    def verticalMoveCollision(self, entity):
        entity.hitbox.y += int(entity.vel.y + 0.5 * entity.acc.y)

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
        spellHitboxes = player.spellHitboxes

        if attackHitboxes:
            for attackHitbox in attackHitboxes:
                for enemy in self.enemies:
                    if attackHitbox.rect.colliderect(enemy.hitbox) and enemy.alive:
                        enemy.loseHP(player.damage)

        if spellHitboxes:
            for spellHitbox in spellHitboxes:
                for enemy in self.enemies:
                    if spellHitbox.rect.colliderect(enemy.hitbox) and enemy.alive:
                        spellHitbox.kill()
                        enemy.loseHP(player.magicDamage)

        #enemies hitting the player
        for enemy in self.enemies:
            xOffset = player.hitbox.centerx - enemy.hitbox.centerx
            if enemy.hit == False and enemy.alive:
                if player.hitbox.colliderect(enemy.hitbox):
                    player.loseHP(enemy.damage)
                    if xOffset > 0:
                        player.vel += pygame.math.Vector2(5, -2)
                    else:
                        player.vel += pygame.math.Vector2(-5, -2)

            if enemy.attackHitboxes:
                for attack in enemy.attackHitboxes:
                    if attack.rect.colliderect(player.hitbox):
                        player.loseHP(enemy.damage)

            if enemy.specialAttackHitboxes:
                pygame.sprite.groupcollide(self.tiles, enemy.specialAttackHitboxes, False, True)

                for specialAttack in enemy.specialAttackHitboxes:
                    if specialAttack.rect.colliderect(player.hitbox):
                        player.loseHP(enemy.damage)
                        specialAttack.kill()

    
    def worldscrolling(self):
        self.scrolling.x += int(self.player.sprite.hitbox.centerx - self.scrolling.x - 305)
        self.scrolling.y += int(self.player.sprite.hitbox.centery - self.scrolling.y - 208)
    
    def run(self):
        self.displaySurface.fill((128, 115, 112))
        self.displaySurface.blit(self.background, (0, 0))
        #camera
        self.worldscrolling()

        #level tiles
        for sprite in self.tiles:
            sprite.drawing(self.displaySurface, self.scrolling)
        
        #player
        self.player.update()
        self.player.sprite.drawing(self.displaySurface, self.scrolling)
        self.horizontalMoveCollision(self.player.sprite)
        self.verticalMoveCollision(self.player.sprite)
        self.checkCollision()
        self.playerUI()

        #magic
        for sprite in self.player.sprite.spellHitboxes:
            sprite.update()
            sprite.drawing(self.displaySurface, self.scrolling)

        #enemies
        for sprite in self.enemies:
            debug(self.displaySurface, sprite.rect.y, x=150, y = 30)
            sprite.update()
            sprite.drawing(self.displaySurface, self.scrolling)
            self.horizontalMoveCollision(sprite)
            self.verticalMoveCollision(sprite)
            if sprite.specialAttackHitboxes:
                for spell in sprite.specialAttackHitboxes:
                    spell.drawing(self.displaySurface, self.scrolling)
                    spell.update()

                    debug(self.displaySurface, spell.rect.y, x = 150, y = 0)
        #debugging


    
        
        
        
        