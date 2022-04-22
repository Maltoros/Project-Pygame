from os import walk
import pygame, os

#Debugging
def debug(surface, info , x = 10, y = 40):
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
STAGE.append(loadMap(os.path.join('Assets','levels','first_stage')))


#Screen Attributes
FPS = 60
TILESIZE = 16
SCREENWIDTH = 600
SCREENHEIGHT = 400
SCREENCENTER = (SCREENWIDTH / 2, SCREENHEIGHT / 2)
#Player Attributes
ACC = 0.5
FRICTION = - 0.12
GRAVITY = 0.5

#enemies
information = {
    'greendude':{'size':(20, 31), 'hp':5, 'damage':3, 'speed':0.2,'mana':0, 'animations': {'idle':[],'run':[],'jump':[],'fall':[],'death':[],'attack':[]}},
    'hunter':{'size':(17, 29), 'hp':3, 'damage':0, 'speed':0.25,'mana':0, 'animations': {'idle':[],'run':[],'jump':[],'fall':[],'death':[],'attack':[]}},
    'summoner':{'size':(17, 29), 'hp':3, 'damage':2, 'speed':0.25,'mana':9, 'animations': {'idle':[],'run':[],'jump':[],'fall':[],'death':[],'casting':[]}},
    'swarm':{'size':(17, 16), 'hp':3, 'damage':2, 'speed':0.2,'mana':0, 'animations': {'idle':[], 'moving':[]}},
      }#hitboxsize, hp, damage, speed

