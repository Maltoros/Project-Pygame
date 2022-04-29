import pygame
from os import path
from settings  import SCREENWIDTH, SCREENHEIGHT, SOUNDTRACK, STAGE, FPS
from level import Level

#ADD DEATH SOUND

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()

        #Display
        self.clock = pygame.time.Clock()
        pygame.display.set_caption('Metroidvania final project')
        self.displayWindow = pygame.display.set_mode((SCREENWIDTH * 2, SCREENHEIGHT * 2))
        self.screen = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))

        #Level Transition
        self.running = True
        self.playing = False
        self.status = 'main menu'
        self.transitionTime = 0
        self.inTransition = False
        self.currentLevel = 0
        self.loadLevel()
        self.playMusicOnce = False
        self.trackMagic = False
        
        #Menu/Out of game overlay Assets
        self.font = pygame.font.Font(path.join('Assets','font','Silver.ttf'), 30)
        self.buttonColor = 'white'
    
    def loadLevel(self):
        pygame.mixer.music.load(SOUNDTRACK[self.currentLevel])
        pygame.mixer.music.set_volume(0.05)
        self.level = Level(self.screen)
        self.level.setupLevel(STAGE[self.currentLevel])

    def runLevel(self): 
        pygame.mouse.set_visible(False)

        if not self.playMusicOnce:
            self.playMusicOnce = True
            pygame.mixer.music.play()

        if self.trackMagic:
            self.level.player.sprite.spellUnlock = self.trackMagic
        else:
            self.trackMagic = self.level.player.sprite.spellUnlock

        self.level.run() 
        self.displayWindow.blit(pygame.transform.scale(self.screen, self.displayWindow.get_size()), (0,0))
        pygame.display.update()

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
        pygame.mouse.set_visible(True)
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
    
    def drawGameOverScreen(self):
        self.currentLevel = 0

        pygame.mouse.set_visible(True)
        pos = list(pygame.mouse.get_pos())
        scaledPos = (pos[0] / 2, pos[1] / 2)

        gameOverRect = pygame.Rect(200, 100, 200, 50)
        newGameButton = pygame.Rect(200, 200, 200, 50)
        quitGameButton = pygame.Rect(200, 300, 200, 50)

        if newGameButton.collidepoint((scaledPos)):
            newGameButtonColor = 'grey'
            if self.click:
                self.loadLevel()
                self.playing = True
        else:
            newGameButtonColor = self.buttonColor
        if quitGameButton.collidepoint((scaledPos)):
            quitGameButtonColor = 'grey'
            if self.click:
                self.running = False
        else:
            quitGameButtonColor = self.buttonColor
            
        pygame.draw.rect(self.screen, 'white', gameOverRect)
        self.drawText('GAME OVER', self.font, 'Black', self.screen, gameOverRect.x + 30, gameOverRect.y + 15)
        pygame.draw.rect(self.screen, newGameButtonColor, newGameButton)
        self.drawText('Try Again', self.font, 'black', self.screen, newGameButton.x + 30, newGameButton.y + 15)
        pygame.draw.rect(self.screen, quitGameButtonColor, quitGameButton)
        self.drawText('Quit Game', self.font, 'black', self.screen, quitGameButton.x + 30, quitGameButton.y + 15)
        self.displayWindow.blit(pygame.transform.scale(self.screen, self.displayWindow.get_size()), (0, 0))
        pygame.display.update()

    def drawTransitionScreen(self):
        self.playMusicOnce = False
        pygame.mixer.music.stop()

        currentTime = pygame.time.get_ticks()
        if currentTime - self.transitionTime >= 1000 and self.inTransition:
            self.currentLevel += 1
            self.loadLevel()
            self.level.player.sprite.completedLevel = False
            self.inTransition = False

        self.screen.fill((0, 0, 0))
        self.drawText('Metroidvania Project', self.font, 'white', self.screen, 200, 100)
        self.drawText('Level Transition', self.font, 'white', self.screen, 200, 300)
        self.displayWindow.blit(pygame.transform.scale(self.screen, self.displayWindow.get_size()), (0, 0))
        pygame.display.update()
    
    def drawVictoryScreen(self):
        pygame.mouse.set_visible(True)
        pos = list(pygame.mouse.get_pos())
        scaledPos = (pos[0] / 2, pos[1] / 2)

        gameOverRect = pygame.Rect(200, 100, 200, 50)
        newGameButton = pygame.Rect(200, 200, 200, 50)
        quitGameButton = pygame.Rect(200, 300, 200, 50)

        if newGameButton.collidepoint((scaledPos)):
            newGameButtonColor = 'grey'
            if self.click:
                self.loadLevel()
                self.playing = True
        else:
            newGameButtonColor = self.buttonColor
        if quitGameButton.collidepoint((scaledPos)):
            quitGameButtonColor = 'grey'
            if self.click:
                self.running = False
        else:
            quitGameButtonColor = self.buttonColor

        pygame.draw.rect(self.screen, 'white', gameOverRect)
        self.drawText('VICTORY', self.font, 'Black', self.screen, gameOverRect.x + 30, gameOverRect.y + 15)
        pygame.draw.rect(self.screen, newGameButtonColor, newGameButton)
        self.drawText('Play Again', self.font, 'black', self.screen, newGameButton.x + 30, newGameButton.y + 15)
        pygame.draw.rect(self.screen, quitGameButtonColor, quitGameButton)
        self.drawText('Quit Game', self.font, 'black', self.screen, quitGameButton.x + 30, quitGameButton.y + 15)
        self.displayWindow.blit(pygame.transform.scale(self.screen, self.displayWindow.get_size()), (0, 0))
        pygame.display.update() 

    def gameStatus(self):
        if not self.playing:
            self.status = 'main menu'
            return self.mainMenu()
        else:
            if self.level.player.sprite.completedLevel:
                self.status = 'transition'
                if not self.inTransition:
                    self.transitionTime = pygame.time.get_ticks()
                    self.inTransition = True
                return self.drawTransitionScreen()
            if self.level.boss:
                if self.level.boss.sprite.defeated:
                    self.status = 'victory screen'
                    return self.drawVictoryScreen()

            if not self.level.player.sprite.gameOver:
                self.status = 'playing' 
                return self.runLevel()
            else:
                self.status = 'game over'
                self.trackMagic = False
                return self.drawGameOverScreen()
            
    def run(self):
        while self.running:
            self.click = False
            self.clock.tick(FPS)
            self.events()
            self.gameStatus()
            
if __name__ == "__main__":
    game = Game()
    game.run()

