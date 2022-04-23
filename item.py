import pygame
from os import path
from settings import items

class Item(pygame.sprite.Sprite):
    def __init__(self, pos, itemType, surface):
        super().__init__()
        self.displaySurface = surface
        self.itemType = itemType
        self.spawnTime = pygame.time.get_ticks()
        self.lifeTime = items[self.itemType]['lifetime']
        self.image = pygame.image.load(path.join('Assets','potions', items[itemType]['image']+'.png')).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
    
    def pickedUpBy(self, player):
        print('acquired')
        if self.itemType == 'Big Life Potion':
            player.hp = player.maxHp
        if self.itemType == 'Medium Life Potion':
            if player.hp + int(0.5*player.maxHp) <= player.maxHp:
                player.hp += int(0.5*player.maxHp)
            else:
                player.hp = player.maxHp
        if self.itemType == 'Small Life Potion':
            if player.hp + int(0.25*player.maxHp) <= player.maxHp:
                player.hp += int(0.25*player.maxHp)
            else:
                player.hp = player.maxHp
        
        if self.itemType == 'Big Mana Potion':
            player.mana = player.maxMana
        elif self.itemType == 'Medium Mana Potion':
            if player.mana + int(0.5*player.maxMana) <= player.maxMana:
                player.mana += int(0.5*player.maxMana)
            else:
                player.mana = player.maxMana
        elif self.itemType == 'Small Mana Potion':
            if player.mana + int(0.25*player.maxMana) <= player.maxMana:
                player.mana += int(0.25*player.maxMana)
            else:
                player.mana = player.maxMana
        
        if self.itemType == 'Spell Unlock Potion':
            player.spellUnlock = True
        
        self.kill()

    def drawing(self, scrolling):
        x = int(self.rect.x - scrolling.x)
        y = int(self.rect.y - scrolling.y)
        self.displaySurface.blit(self.image, (x, y))

    def update(self):
        currentTime = pygame.time.get_ticks()
        if self.lifeTime:
            if currentTime - self.spawnTime >= self.lifeTime:
                self.kill()