from os import walk
import os, pygame
vec = pygame.math.Vector2
#Debugging
def debug(surface, info , x = 10, y = 10):
            font = pygame.font.Font(None, 30)
            debug_surf = font.render(str(info),True, 'White')
            debug_rect = debug_surf.get_rect(topleft = (x, y))
            pygame.draw.rect(surface, 'Black', debug_rect)
            surface.blit(debug_surf, debug_rect)

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
SCREENWIDTH = 600
SCREENHEIGHT = 400
SCREENCENTER = (SCREENWIDTH / 2, SCREENHEIGHT / 2)
#Player Attributes
playerAcc = 0.5
playerFric = - 0.12
playerGrav = 0.5
#PolygonAttacks
attackAnimationsRight = [0, 0, ( (SCREENCENTER + vec(-3, -22) ), (SCREENCENTER + vec(27, -10) ), (SCREENCENTER + vec(27, 0) ), (SCREENCENTER + vec(17, 5) ), (SCREENCENTER + vec(10, 5) ), (SCREENCENTER + vec(5, 5) ) ), ((SCREENCENTER + vec(7, 3) ), (SCREENCENTER + vec(20, -13) ), (SCREENCENTER + vec(24, -6) ), (SCREENCENTER + vec(20, 1) ), (SCREENCENTER + vec(6, 1) ) ), 0, 0 ]
attackAnimationsLeft = [0, 0, ( (SCREENCENTER + vec(3, -22) ), (SCREENCENTER + vec(-27, -10) ), (SCREENCENTER + vec(-27, 0) ), (SCREENCENTER + vec(-17, 5) ), (SCREENCENTER + vec(-10, 5) ) ), ( (SCREENCENTER + vec(-5, 5) ), (SCREENCENTER + vec(-7, 3) ), (SCREENCENTER + vec(-20, -13) ), (SCREENCENTER + vec(-24, -6) ), (SCREENCENTER + vec(-20, 1) ), (SCREENCENTER + vec(-6, 1) ) ), 0, 0]

newAtkAnimRight = [0, 0, ((-3, -22), (27, -10), (27,0), (17,5), (10,5), (5,5)), ((7,3), (20,-13),(24, -6),(20, 1), (6, 1)), 0, 0]

#RectAttacks
attacksRects = [0, 0, ((0,0),(20, 24)) ,((0,0), (20, 15)), ((0,0), (20, 4)), 0]
