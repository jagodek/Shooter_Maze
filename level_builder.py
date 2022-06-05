from http.client import ImproperConnectionState
import pygame as pg
from game_params import MAP_WIDTH,MAP_HEIGHT,WIN_HEIGHT,WIN_WIDTH,WALL_WIDTH
import os

exit_game = False
tiles_row = MAP_WIDTH//WALL_WIDTH
tile_width = WIN_WIDTH//tiles_row
pg.init()
win = pg.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

pth = os.path.join("textures","map_template.jpg")
img = pg.image.load(pth)
img = pg.transform.scale(img,(WIN_WIDTH,WIN_HEIGHT))


def clicked_tile(x,y):
    return x//tile_width,y//tile_width




while not exit_game:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit_game = True
    win.blit(img,(0,0))
    answ = []
    for i in range(0,tiles_row):
        for y in range(0,tiles_row):
            wall = (i*tile_width,y*tile_width)
            cond = False
            for j in range(2,int(tile_width)-2):
                for k in range(2,int(tile_width)-2):
                    check = (i*tile_width+j,y * tile_width+k)
                    col = win.get_at(check)
                    if col == (255,255,255):
                        cond = True
                        answ.append(clicked_tile(*(wall)))
                        break
                if cond: break



        pg.draw.line(win, (255, 0, 0), (0,i * tile_width), (WIN_WIDTH,i * tile_width))
        pg.draw.line(win,(255,0,0),(i*tile_width,0),(i*tile_width,WIN_HEIGHT))
    pg.display.update()

print(answ)