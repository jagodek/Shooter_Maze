import pygame as pg
from game_params import map_width,map_height,win_height,win_width,WALL_WIDTH

exit_game = False
tiles_row = map_width//WALL_WIDTH
tile_width = win_width//tiles_row
pg.init()
win = pg.display.set_mode((win_width,win_height))

img = pg.image.load(r"textures\map_template.jpg")
img = pg.transform.scale(img,(win_width,win_height))


def clicked_tile(x,y):
    return x//tile_width,y//tile_width




while not exit_game:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit_game = True
        if event.type == pg.MOUSEBUTTONDOWN:
            print(clicked_tile(*pg.mouse.get_pos()))
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



        pg.draw.line(win, (255, 0, 0), (0,i * tile_width), (win_width,i * tile_width))
        pg.draw.line(win,(255,0,0),(i*tile_width,0),(i*tile_width,win_height))
    pg.display.update()

print(answ)