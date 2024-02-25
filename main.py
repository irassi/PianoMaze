import pygame as pg
import random
import numpy as np

pg.init()
pg.mixer.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PLAY_AREA_WIDTH = 800
PLAY_AREA_HEIGHT = 450

#Colors
BG = (50, 50, 50)
GREEN = (10, 215, 10)
RED = (215, 10, 10)
BLUE = (10, 10, 215)
WHITE = (244, 244, 244)
BLACK = (10, 10, 10)
DARKNESS = (0, 0, 20)

clock = pg.time.Clock()

screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


pg.display.set_caption("PianoMaze")

tile_size = 25
play_bg = pg.Rect(0, 0, PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT)
play_area = pg.Surface((PLAY_AREA_WIDTH, PLAY_AREA_HEIGHT))
ui_area = pg.Surface((WINDOW_WIDTH, WINDOW_HEIGHT - PLAY_AREA_HEIGHT))
player = pg.Rect(0, 0, tile_size, tile_size)

#light and darkness
radius = 50
cover_surf = pg.Surface((radius*2, radius*2))
cover_surf.fill(DARKNESS)
cover_surf.set_colorkey((255, 255, 255))
pg.draw.circle(cover_surf, (255, 255, 255), (radius, radius), radius)

maze = []
maze = np.zeros((np.int8(PLAY_AREA_WIDTH/tile_size), np.int8(PLAY_AREA_HEIGHT/tile_size)), dtype=np.int8)
for idx, x in enumerate(maze):
    for idy, y in enumerate(x):
        maze[idx, idy] = np.int8(random.randint(0,3)/3)
    
obstacles = []
for idx, x in enumerate(maze):
    for idy, y in enumerate(x):
        if y == 1:
            obstacle = pg.Rect(idx*tile_size, idy*tile_size, tile_size, tile_size)
            obstacles.append(obstacle)
    
# Draw the piano keys
wkeys = []
bkeys = []
keys_amount = 7
keys_width = 30
keys_height = 90

keys_start_w = WINDOW_WIDTH / 2 - keys_amount * 33 / 2
keys_start_h = ui_area.get_height() / 2 - keys_height / 2

for i in range(keys_amount):
    wkey_w = keys_start_w + i*(keys_width+2)
    wkey_h = keys_start_h
    wkey = pg.Rect(wkey_w, wkey_h, keys_width, keys_height)
    wkeys.append(wkey)

    bkey_w = wkey_w + round(keys_width * 0.667)
    bkey_h = wkey_h

    # add black keys, not optimized for more than 7 white keys
    if i != 2 and i != 6:
        bkey = pg.Rect(bkey_w, bkey_h, round(keys_width * 0.667), round(keys_height * 0.667))
        bkeys.append(bkey)


#Keyboard
#TODO: Maybe I should divide "keysAmount" to 12 key sets and store wkey and bkeys in the same list?
key_bindings = np.zeros(7)
key_bindings[0] = pg.K_d
key_bindings[1] = pg.K_f
key_bindings[2] = pg.K_g
key_bindings[3] = pg.K_h
key_bindings[4] = pg.K_j
key_bindings[5] = pg.K_k
key_bindings[6] = pg.K_l
piano_keys_pressed = np.zeros(7)

sounds=[]
soundStart = 40
for i in range(keys_amount):
    soundID = soundStart + i
    #for white keys
    if soundID  not in [1, 3, 6, 8, 10]:
        soundPath = r"C:\Projects\PianoMaze\Sounds\piano-ff-0{}.wav".format(soundID)
        sounds.append(soundPath)



def handle_movement(direction):
    
    move_speed = 1

    if direction == "up":
        player.move_ip(0, -move_speed)
        if check_collision():
            player.move_ip(0, move_speed)

    elif direction == "down":
         player.move_ip(0, move_speed)
         if check_collision():
            player.move_ip(0, -move_speed)
        
    elif direction == "left":
        player.move_ip(-move_speed, 0)
        if check_collision():
            player.move_ip(move_speed, 0)
        
    elif direction == "right":
        player.move_ip(move_speed, 0)
        if check_collision():
            player.move_ip(-move_speed, 0)
        


def check_collision():
    if player.collidelist(obstacles) >=0 :
        return True
    return False

run = True

while run:

    clock.tick(60)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.KEYDOWN:
            for i, key in enumerate(key_bindings):
                if event.key == key:
                    piano_keys_pressed[i] = 1
                    sound = pg.mixer.Sound(sounds[i])  # Load the sound
                    sound.play()  # Play the sound
        
        if event.type == pg.KEYUP:
            for i, key in enumerate(key_bindings):
                if event.key == key:
                    piano_keys_pressed[i] = 0

    screen.fill(BG)

    #draw play area
    play_area.fill(DARKNESS)
    clip_center = player.center
    clip_rect = pg.Rect(clip_center[0] - radius, clip_center[1] - radius, radius*2, radius*2)
    # screen.set_clip(clip_rect)
    play_area.set_clip(clip_rect)

    # pg.draw.rect(screen, BG, play_area)
    pg.draw.rect(play_area, BG, play_bg)

    #draw player
    pg.draw.rect(play_area, GREEN, player)

    player.clamp_ip(play_bg)

    #draw obstacles
    for obstacle in obstacles:
        pg.draw.rect(play_area, BLUE, obstacle)

    #draw UI

    ui_area.fill(BG)
    pg.draw.line(ui_area, WHITE, (0,0), (WINDOW_WIDTH,0), 3)

    #draw pianokeys
    for i, wkey in enumerate(wkeys):
        if piano_keys_pressed[i] == 1:
            pg.draw.rect(ui_area, GREEN, wkey)
        else:
            pg.draw.rect(ui_area, WHITE, wkey)

    for bkey in bkeys:
        pg.draw.rect(ui_area, BLACK, bkey)    

    # pg.key.set_repeat(100)
    key = pg.key.get_pressed()

    if key[pg.K_LEFT] == True:
        handle_movement("left")
    
    if key[pg.K_RIGHT] == True:
        handle_movement("right")
    
    if key[pg.K_UP] == True:
        handle_movement("up")

    if key[pg.K_DOWN] == True:
        handle_movement("down")


    play_area.blit(cover_surf, clip_rect)

    screen.blit(play_area, (0, 0))
    screen.blit(ui_area, (0, PLAY_AREA_HEIGHT))

    pg.display.flip()

pg.quit()
