from cmath import inf
from game_params import WIN_WIDTH, MAP_WIDTH, WIN_HEIGHT, MAP_HEIGHT, WALLS_CORDS, WALL_WIDTH
import numpy as np


# returns location on screen based on location of player and location of self
def location_on_screen(x_player, y_player, x_self, y_self):
    if x_player < WIN_WIDTH / 2:
        x = x_self
    elif x_player > MAP_WIDTH - WIN_WIDTH / 2:
        x = WIN_WIDTH - (MAP_WIDTH - x_self)
    else:
        x = WIN_WIDTH / 2 - (x_player - x_self)

    if y_player < WIN_HEIGHT / 2:
        y = y_self
    elif y_player > MAP_HEIGHT - WIN_HEIGHT / 2:
        y = WIN_HEIGHT - (MAP_HEIGHT - y_self)
    else:
        y = WIN_HEIGHT / 2 - (y_player - y_self)
    return x, y


# location on map based on location of player and self position on screen
def location_on_map(x_player, y_player, x_self, y_self):
    if x_player < WIN_WIDTH / 2:
        x = x_self
    elif x_player > MAP_WIDTH - WIN_WIDTH / 2:
        x = x_self + MAP_WIDTH - WIN_WIDTH
    else:
        x = x_self - WIN_WIDTH / 2 + x_player

    if y_player < WIN_HEIGHT / 2:
        y = y_self
    elif y_player > MAP_HEIGHT - WIN_HEIGHT / 2:
        y = y_self + MAP_HEIGHT - WIN_HEIGHT
    else:
        y = y_self - WIN_HEIGHT / 2 + y_player

    return x, y



def is_wall(x, y):
    for i in WALLS_CORDS:
        if i[0]<x <i[0]+WALL_WIDTH and i[1]<y<i[1]+WALL_WIDTH:
            return True
    return False
    
    
                
                
                
    
