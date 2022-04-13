import pygame
from tile import Tile
from player import Player
from settings import TILESIZE, SCREENWIDTH, SCREENHEIGHT
from camera import Camera

class Level:
    def __init__(self, stage, surface):
        self.displaySurface = surface
        self.stage = stage
        self.tiles = pygame.sprite.Group()
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
                elif player.vel.y < 0:
                    player.hitbox.top = sprite.rect.bottom
                    player.vel.y = 0 
                    player.onCeilling = True
 
        if player.onGround and player.vel.y < 0 or player.vel.y > 0:
            player.onGround = False
        if player.onCeilling and player.vel.y > 0:
            player.OnCeilling = False

    def debug(self, info,y = 10, x = 10):
        font = pygame.font.Font(None, 30)
        debug_surf = font.render(str(info),True, 'White')
        debug_rect = debug_surf.get_rect(topleft = (x, y))
        pygame.draw.rect(self.displaySurface, 'Black', debug_rect)
        self.displaySurface.blit(debug_surf, debug_rect)

    def run(self):
        #camera
        self.camera.update(self.player.sprite)

        #level tiles
        for sprite in self.tiles:
            self.displaySurface.blit(sprite.image, self.camera.apply(sprite))

        #player
        #self.createAttackHitbox()
        self.player.update()
        self.displaySurface.blit(self.player.sprite.image, self.camera.apply(self.player.sprite))
        self.horizontalMoveCollision()
        self.verticalMoveCollision()
        self.debug(self.player.sprite.hitbox.x)


