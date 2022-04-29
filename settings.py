from os import walk
import pygame, os
pygame.mixer.init()

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
STAGE.append(loadMap(os.path.join('Assets','levels','second_stage')))
STAGE.append(loadMap(os.path.join('Assets','levels','third_stage')))


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
enemyInformation = {
    'greendude':{'size':(20, 31), 'hp':5, 'damage':3, 'speed':0.2,'mana':0,'chance':(8,9,10), 'animations': {'idle':[],'run':[],'jump':[],'fall':[],'death':[],'attack':[]}},
    'hunter':{'size':(17, 29), 'hp':3, 'damage':3, 'speed':0.25,'mana':0, 'chance':(7,8,9,10), 'animations': {'idle':[],'run':[],'jump':[],'fall':[],'death':[],'attack':[]}},
    'summoner':{'size':(17, 29), 'hp':3, 'damage':2, 'speed':0.25,'mana':9, 'chance':(6,7,8,9,10), 'animations': {'idle':[],'run':[],'jump':[],'fall':[],'death':[],'casting':[]}},
    'swarm':{'size':(17, 16), 'hp':3, 'damage':2, 'speed':0.2,'mana':0, 'animations': {'idle':[], 'moving':[]}},
      }#hitboxsize, hp, damage, speed

#Items
items = {
    'Big Life Potion':{
        'image':'bigLifePotion',
        'lifetime': 5000
        },
    'Medium Life Potion':{
        'image':'mediumLifePotion',
        'lifetime': 5000
        },
    'Small Life Potion':{
        'image':'smallLifePotion',
        'lifetime': 5000
        },
    'Big Mana Potion':{
        'image':'bigManaPotion',
        'lifetime': 5000
        },
    'Medium Mana Potion':{
        'image':'mediumManaPotion',
        'lifetime': 5000
        },
    'Small Mana Potion':{
        'image':'smallManaPotion',
        'lifetime': 5000
        },
    'Spell Unlock Potion':{
        'image':'spellUnlockPotion',
        'lifetime': False
        },
}
#Boss possible positions
bossPositions = [(160, 176),(656,176),(400,240),(160,304),(656,304)]#TOPLEFT, TOPRIGHT, CENTER, BOTTOMLEFT, BOTTOMRIGHT

#Soundeffects
ENEMYHITSOUND = pygame.mixer.Sound(os.path.join('Assets','sound','sfx','enemyHit.wav'))
ENEMYHITSOUND.set_volume(0.01)

JUMPSOUND = pygame.mixer.Sound(os.path.join('Assets','sound','sfx','jumpSound.wav'))
JUMPSOUND.set_volume(0.01)

LASERBALLSOUND = pygame.mixer.Sound(os.path.join('Assets','sound','sfx','laserBallSound.wav'))
LASERBALLSOUND.set_volume(0.1)

PICKUPPOTIONSOUND = pygame.mixer.Sound(os.path.join('Assets','sound','sfx','pickUpPotion.wav'))
PICKUPPOTIONSOUND.set_volume(0.2)

PLAYERHITSOUND = pygame.mixer.Sound(os.path.join('Assets','sound','sfx','playerHit.wav'))
PLAYERHITSOUND.set_volume(0.01)

PLAYERDYINGSOUND = pygame.mixer.Sound(os.path.join('Assets','sound','sfx','playerDying.wav'))
PLAYERDYINGSOUND.set_volume(0.01)

SWITCHSTATESOUND = pygame.mixer.Sound(os.path.join('Assets','sound','sfx', 'switchState.wav'))
SWITCHSTATESOUND.set_volume(0.02)

UNLOCKPASSAGESOUND = pygame.mixer.Sound(os.path.join('Assets','sound','sfx','unlockPassage.wav'))
UNLOCKPASSAGESOUND.set_volume(0.02)

BOSSTELEPORTINGSOUND = pygame.mixer.Sound(os.path.join('Assets','sound','sfx','bossTeleporting.wav'))
BOSSTELEPORTINGSOUND.set_volume(0.02)

#Music
FIRSTLEVEL = os.path.join('Assets','sound','music','firstlevel.wav')
SECONDLEVEL = os.path.join('Assets','sound','music','secondlevel.wav')
THIRDLEVEL = os.path.join('Assets','sound','music','thirdlevel.wav')
SOUNDTRACK = [FIRSTLEVEL, SECONDLEVEL, THIRDLEVEL]