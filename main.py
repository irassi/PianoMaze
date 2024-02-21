import pygame as pg
import random
import numpy as np

pg.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAY_AREA_WIDTH = 800
PLAY_AREA_HEIGHT = 450

screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Testing")

tile_size = 25
play_area = pg.Rect(0, 0, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT)
player = pg.Rect(0, 0, tile_size, tile_size)

maze = []
maze = np.zeros((np.int8(PLAY_AREA_WIDTH/tile_size), np.int8(PLAY_AREA_HEIGHT/tile_size)), dtype=np.int8)
for idx, x in enumerate(maze):
    for idy, y in enumerate(x):
        maze[idx, idy] = np.int8(random.randint(0,3)/3)
    
# for x in maze:
#     print(x)
            
print(maze)

obstacles = []
for idx, x in enumerate(maze):
    for idy, y in enumerate(x):
        if y == 1:
            obstacle = pg.Rect(idx*tile_size, idy*tile_size, tile_size, tile_size)
            obstacles.append(obstacle)
    
wkeys = []
bkeys = []

keys_start_w = 275
keys_start_h = 470

for i in range(7):
    wkey_w = keys_start_w + i*33
    wkey_h = keys_start_h
    wkey = pg.Rect(wkey_w, wkey_h, 30, 90)
    wkeys.append(wkey)

    bkey_w = keys_start_w + i*33 + 21
    bkey_h = keys_start_h

    if i != 2 and i != 6:
        bkey = pg.Rect(bkey_w, bkey_h, 20, 60)
        bkeys.append(bkey)


#COLORS
BG = (50, 50, 50)
GREEN = (10, 215, 10)
RED = (215, 10, 10)
BLUE = (10, 10, 215)
WHITE = (244, 244, 244)
BLACK = (10, 10, 10)

key_bindings = np.zeros(7)
key_bindings[0] = pg.K_d
key_bindings[1] = pg.K_f
key_bindings[2] = pg.K_g
key_bindings[3] = pg.K_h
key_bindings[4] = pg.K_j
key_bindings[5] = pg.K_k
key_bindings[6] = pg.K_l
piano_keys_pressed = np.zeros(7)

uptick = 0


def checkCollision():
    if player.collidelist(obstacles) >=0 :
        return True
    return False

run = True
while run:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.KEYDOWN:
            for i, key in enumerate(key_bindings):
                if event.key == key:
                    piano_keys_pressed[i] = 1
        
        if event.type == pg.KEYUP:
            for i, key in enumerate(key_bindings):
                if event.key == key:
                    piano_keys_pressed[i] = 0

    screen.fill(BG)
    pg.draw.rect(screen, BG, play_area)
    pg.draw.line(screen, WHITE, (0,PLAY_AREA_HEIGHT+2), (WINDOW_WIDTH,PLAY_AREA_HEIGHT+2), 3)

    #draw player
    # pg.draw.rect(screen, GREEN, player)

    player.clamp_ip(play_area)

    #draw obstacles
    for obstacle in obstacles:
        pg.draw.rect(screen, BLUE, obstacle)

    #draw pianokeys
    for i, wkey in enumerate(wkeys):
        if piano_keys_pressed[i] == 1:
            pg.draw.rect(screen, GREEN, wkey)
        else:
            pg.draw.rect(screen, WHITE, wkey)

    for bkey in bkeys:
        pg.draw.rect(screen, BLACK, bkey)    

    # pg.key.set_repeat(100)
    key = pg.key.get_pressed()

    if key[pg.K_LEFT] == True:
        player.move_ip(-1, 0)
        if checkCollision():
            player.move_ip(1, 0)

    
    if key[pg.K_RIGHT] == True:
        player.move_ip(1, 0)
        if checkCollision():
            player.move_ip(-1, 0)
    
    if key[pg.K_UP] == True:

        if uptick == 0:
            player.move_ip(0, -1)
            if checkCollision():
                player.move_ip(0, 1) 
        uptick += 1
        if uptick >= 10:
            uptick = 0

    if key[pg.K_DOWN] == True:
        player.move_ip(0, 1)
        if checkCollision():
            player.move_ip(0, -1)

    pg.draw.rect(screen, GREEN, player)    
    pg.display.update()
    print("Uptick: {}".format(uptick))

pg.quit()