from os import walk
import os, pygame
#Importing files
def importFolder(path):
    surfaceList = []
    for _, __, imgFiles in walk(path):
        for image in imgFiles:
            fullpath = os.path.join(path,image)
            imageSurface = pygame.image.load(fullpath).convert_alpha()
            surfaceList.append(imageSurface)
    return surfaceList

#Loading Stages
def loadMap(path):
    f = open(path + '.txt', 'r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map
STAGE = []
STAGE.append(loadMap(os.path.join('Assets','first_stage')))
#Screen Attributes
FPS = 60 
TILESIZE = 48 
SCREENWIDTH = 500
SCREENHEIGHT = 500
#Player Attributes
playerAcc = 0.5
playerFric = - 0.12
playerGrav = 0.5