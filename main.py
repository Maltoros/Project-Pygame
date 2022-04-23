import pygame
from os import path
from settings  import SCREENWIDTH, SCREENHEIGHT, STAGE, FPS
from level import Level

#ADD % DROPS TO POTIONS ON ENEMIES
#Maybe add gravity to the potions
#Polish restart mechanic
#Configure level transition
#Make 1-2 more levels
#Make boss fight (?)
#Add Music and sound effects


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Metroidvania final project')
        self.displayWindow = pygame.display.set_mode((SCREENWIDTH * 2, SCREENHEIGHT * 2))
        self.screen = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
        self.running = True
        self.playing = False
        self.level = Level(self.screen)
        self.level.setupLevel(STAGE[0])
        self.font = pygame.font.Font(path.join('Assets','font','Silver.ttf'), 30)
        self.buttonColor = 'white'
    
    def newLevel(self):
        self.level = Level(self.screen)
        self.level.setupLevel(STAGE[0])
    def runLevel(self): 
        self.level.run() 
        self.drawLevel()

    def events(self):
        player = self.level.player.sprite
        self.click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True
            if self.playing:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        player.jump()
                elif event.type == pygame.KEYUP:        
                    if event.key == pygame.K_j:
                        if not player.attacking and not player.casting:
                            player.attack()
                    elif event.key == pygame.K_k:
                        if not player.attacking and not player.casting:              
                            player.magic()   
                

    def drawText(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def mainMenu(self):
        pos = list(pygame.mouse.get_pos())
        scaledPos = (pos[0] / 2, pos[1] / 2)


        self.screen.fill((0, 0, 0))
        self.drawText('Metroidvania Project', self.font, 'white', self.screen, 200, 100)


        newGameButton = pygame.Rect(200, 200, 200, 50)
        quitGameButton = pygame.Rect(200, 300, 200, 50)
        if newGameButton.collidepoint((scaledPos)):
            newGameButtonColor = 'grey'
            if self.click:
                self.playing = True
        else:
            newGameButtonColor = self.buttonColor
        if quitGameButton.collidepoint((scaledPos)):
            quitGameButtonColor = 'grey'
            if self.click:
                self.running = False
        else:
            quitGameButtonColor = self.buttonColor

        pygame.draw.rect(self.screen, newGameButtonColor, newGameButton)
        self.drawText('New Game', self.font, 'black', self.screen, newGameButton.x + 30, newGameButton.y + 15)
        pygame.draw.rect(self.screen, quitGameButtonColor, quitGameButton)
        self.drawText('Quit Game', self.font, 'black', self.screen, quitGameButton.x + 30, quitGameButton.y + 15)

        self.drawText('KEYBINDS :', self.font, 'white', self.screen, 420, 200)
        self.drawText('LEFT/RIGHT :A/D', self.font, 'white', self.screen, 420, 220)
        self.drawText('ATTACK : J', self.font, 'white', self.screen, 420, 240)
        self.drawText('SPELL : K', self.font, 'white', self.screen, 420, 260)
        self.drawText('JUMP : SPACEBAR', self.font, 'white', self.screen, 420, 280)

        self.displayWindow.blit(pygame.transform.scale(self.screen, self.displayWindow.get_size()), (0,0))
        pygame.display.update()

        

    def drawLevel(self):
        self.displayWindow.blit(pygame.transform.scale(self.screen, self.displayWindow.get_size()), (0,0))
        pygame.display.update()
    
    def drawGameOverScreen(self):
        pos = list(pygame.mouse.get_pos())
        scaledPos = (pos[0] / 2, pos[1] / 2)

        newGameButton = pygame.Rect(200, 200, 200, 50)
        quitGameButton = pygame.Rect(200, 300, 200, 50)
        if newGameButton.collidepoint((scaledPos)):
            newGameButtonColor = 'grey'
            if self.click:
                self.newLevel()
                self.playing = True
        else:
            newGameButtonColor = self.buttonColor
        if quitGameButton.collidepoint((scaledPos)):
            quitGameButtonColor = 'grey'
            if self.click:
                self.running = False
        else:
            quitGameButtonColor = self.buttonColor

        pygame.draw.rect(self.screen, newGameButtonColor, newGameButton)
        self.drawText('New Game', self.font, 'black', self.screen, newGameButton.x + 30, newGameButton.y + 15)
        pygame.draw.rect(self.screen, quitGameButtonColor, quitGameButton)
        self.drawText('Quit Game', self.font, 'black', self.screen, quitGameButton.x + 30, quitGameButton.y + 15)
        self.displayWindow.blit(pygame.transform.scale(self.screen, self.displayWindow.get_size()), (0, 0))
        pygame.display.update()

    def run(self):
        while self.running:
            self.click = False
            self.clock.tick(FPS)
            self.events()
            if not self.playing:
                self.mainMenu()
            elif not self.level.player.sprite.gameOver:
                pygame.mouse.set_visible(False)
                self.runLevel()
            else:
                pygame.mouse.set_visible(True)
                self.drawGameOverScreen()


if __name__ == "__main__":
    game = Game()
    game.run()

