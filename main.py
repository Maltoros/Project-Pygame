import pygame
from settings  import SCREENWIDTH, SCREENHEIGHT, STAGE, FPS
from level import Level


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Metroidvania final project')
        self.displayWindow = pygame.display.set_mode((SCREENWIDTH * 2, SCREENHEIGHT * 2))
        self.screen = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
        self.running = True
        self.level = Level(self.screen)
        self.level.setupLevel(STAGE[0])


    def new(self):
        self.run()

    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.draw()

    def events(self):
        player = self.level.player.sprite
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()
            elif event.type == pygame.KEYUP:        
                if event.key == pygame.K_j:
                    if not player.attacking and not player.casting:
                        player.attack()
                elif event.key == pygame.K_k:
                    if not player.attacking and not player.casting:              
                        player.magic()   
            

    def draw(self):
        self.level.run() 
        self.displayWindow.blit(pygame.transform.scale(self.screen, self.displayWindow.get_size()), (0,0))
        pygame.display.update()

    def showStartScreen(self):
        pass

    def showGameOverScreen(self):
        pass

if __name__ == "__main__":
    game = Game()
    game.showStartScreen()
    while game.running:
        game.new()
        game.showGameOverScreen()
