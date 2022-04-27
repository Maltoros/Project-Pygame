import pygame
from os import path
from tile import ActivatedTile, ExitLevel, Switch, Tile, TrapTile
from boss import Boss
from player import Player
from enemy import Enemy
from item import Item
from settings import SCREENCENTER, TILESIZE, debug

class Level:
    def __init__(self, surface):
        self.displaySurface = surface
        self.tiles = pygame.sprite.Group()
        self.switches = pygame.sprite.Group()
        self.levelExit = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.boss = pygame.sprite.GroupSingle()
        self.scrolling = pygame.math.Vector2(0, 0)
        self.background = pygame.transform.scale(pygame.image.load(path.join('Assets','background','0.png')),(600, 400))

    def setupLevel(self, layout):
        for rowIndex, row in enumerate(layout):
            for colIndex, cell in enumerate(row):
                x = colIndex * TILESIZE
                y = rowIndex * TILESIZE
                if cell == '1':
                    tile = Tile((x, y), self.displaySurface, 'brick')
                    self.tiles.add(tile)
                if cell == '2':
                    tile = Tile((x, y), self.displaySurface, 'wood')
                    self.tiles.add(tile)
                if cell == '3':
                    tile = Tile((x, y), self.displaySurface, 'breakablebrick', True)
                    self.tiles.add(tile)
                if cell == '4':
                    tile = Tile((x, y), self.displaySurface, 'breakablebrick', True)
                    self.tiles.add(tile)
                    itemSprite = Item((x, y), 'Spell Unlock Potion', self.displaySurface)
                    self.items.add(itemSprite)
                if cell == 'T':
                    trap = TrapTile((x, y), self.displaySurface, 'spikeUp')
                    self.traps.add(trap)

                if cell == 'Q':
                    switch = Switch((x, y), self.displaySurface, 'switchOff')
                    self.switches.add(switch)


                if cell in ('L','E'):
                    if cell == 'E':
                        image = 'exitTop'
                    else:
                        image = 'exitBottom'     
                    levelExitTile = ExitLevel((x, y), self.displaySurface, image)
                    self.levelExit.add(levelExitTile)

                if cell == 'A': # To be some kind of door asset
                    activableTile = ActivatedTile((x, y,), self.displaySurface, 'bridge', self.switches)
                    self.tiles.add(activableTile)

                if cell == 'M':
                    itemSprite = Item((x, y), 'Spell Unlock Potion', self.displaySurface)
                    self.items.add(itemSprite)
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
                if cell =='B':
                    bossSprite = Boss((x, y), self.displaySurface, self)
                    self.boss.add(bossSprite)
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

    def bossUI(self):
        boss = self.boss.sprite

        life = pygame.Rect(80, 350, boss.hp * 15, 10)
        lifeBg = pygame.Rect(79, 349, 2+boss.maxHp * 15, 12)
        pygame.draw.rect(self.displaySurface, 'black', lifeBg)
        pygame.draw.rect(self.displaySurface, 'red', life)

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
            tilesHit = pygame.sprite.groupcollide(attackHitboxes, self.tiles, False, False)
            for tileList in tilesHit.values():
                for tile in tileList:
                    if tile.breakable:
                        tile.kill()
            for attackHitbox in attackHitboxes:
                for enemy in self.enemies:
                    if attackHitbox.rect.colliderect(enemy.hitbox) and enemy.alive:
                        enemy.loseHP(player.damage)
                for switch in self.switches:
                    if attackHitbox.rect.colliderect(switch.rect):
                        switch.switchState()
                if self.boss:
                    if attackHitbox.rect.colliderect(self.boss.sprite.hitbox) and self.boss.sprite.alive:
                        self.boss.sprite.loseHP(player.damage)

        if spellHitboxes:
            pygame.sprite.groupcollide(self.tiles, spellHitboxes, False, True)
            for spellHitbox in spellHitboxes:
                for enemy in self.enemies:
                    if spellHitbox.rect.colliderect(enemy.hitbox) and enemy.alive:
                        spellHitbox.kill()
                        enemy.loseHP(player.magicDamage)
            if self.boss:
                    if spellHitbox.rect.colliderect(self.boss.sprite.hitbox) and self.boss.sprite.alive:
                        spellHitbox.kill()
                        self.boss.sprite.loseHP(player.magicDamage)
        if self.items:
            for item in self.items:
                if player.hitbox.colliderect(item.rect):
                    item.pickedUpBy(player)

        #traps
        for trap in self.traps:
            if self.player.sprite.hitbox.colliderect(trap.hitbox):
                self.player.sprite.loseHP(3)

        #exit
        for levelExit in self.levelExit:
            if self.player.sprite.hitbox.colliderect(levelExit.rect):
                self.player.sprite.completedLevel = True

        #enemies colliding with the player
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
                        player.loseHP(enemy.specialDamage)
                        specialAttack.kill()

        if self.boss.sprite.specialAttackHitboxes:
            for specialAttack in self.boss.sprite.specialAttackHitboxes:
                if specialAttack.hitbox.colliderect(player.hitbox):
                    player.loseHP(self.boss.sprite.specialDamage)
                    specialAttack.kill()
    
    def worldscrolling(self):
        self.scrolling.x += int(self.player.sprite.hitbox.centerx - self.scrolling.x - 305)
        self.scrolling.y += int(self.player.sprite.hitbox.centery - self.scrolling.y - 208)
    
    def run(self):
        self.displaySurface.fill((128, 115, 112))
        self.displaySurface.blit(self.background, (0, 0))
        #camera
        self.worldscrolling()

        #items
        for item in self.items:
            item.drawing(self.scrolling)
            item.update()
            if pygame.sprite.spritecollide(item, self.tiles, False):
                item.onGround = True
        #level tiles
        for tile in self.tiles:
            tile.drawing(self.scrolling)
            tile.update()
        
        for trap in self.traps:
            trap.drawing(self.scrolling)

        for switch in self.switches:
            switch.drawing(self.scrolling)
            switch.update()

        for exitTile in self.levelExit:
            exitTile.drawing(self.scrolling)

        #player
        self.player.update()
        self.player.sprite.drawing(self.scrolling)
        self.horizontalMoveCollision(self.player.sprite)
        self.verticalMoveCollision(self.player.sprite)
        self.checkCollision()
        self.playerUI()

        #magic
        for spell in self.player.sprite.spellHitboxes:
            spell.drawing(self.displaySurface, self.scrolling)
            spell.update()


        #enemies
        for enemy in self.enemies:
            enemy.update()
            enemy.drawing(self.scrolling)
            self.horizontalMoveCollision(enemy)
            self.verticalMoveCollision(enemy)

            if enemy.specialAttackHitboxes:
                for spell in enemy.specialAttackHitboxes:
                    spell.drawing(self.displaySurface, self.scrolling)
                    spell.update()
        if self.boss:
            self.boss.update()
            self.boss.sprite.drawing(self.scrolling)
            self.bossUI()
            for spell in self.boss.sprite.specialAttackHitboxes:
                spell.drawing(self.displaySurface, self.scrolling)
                spell.update()

        #debugging


    
        
        
        
        