import pygame as pg
from functions import *
from game_params import WALL_WIDTH,wall_img

class Wall(pg.sprite.Sprite):
    def __init__(self, width, height, pos_x, pos_y):
        super().__init__()
        self.width = width*WALL_WIDTH
        self.height = height*WALL_WIDTH
        self.pos_x = pos_x*WALL_WIDTH
        self.pos_y = pos_y*WALL_WIDTH
        self.rect = pg.rect.Rect(self.pos_x,self.pos_y,self.width,self.height)
        
        self.rect.topleft = list(location_on_screen(0, 0, pos_x, pos_y))
        self.image_src = wall_img
        self.image = pg.surface.Surface((self.width,self.height))
        # self.image_src = pg.transform.scale(self.image_src,(500, 500))
        # repeats the wall img pattern

        for i in range(self.width // self.image_src.get_width() + 1):
            for j in range(self.height // self.image_src.get_height() + 1):
                    self.image.blit(self.image_src,(i*self.image_src.get_width(),j*self.image_src.get_height()))

    def update(self,win,player_x,player_y):
        
        self.rect.topleft = list(location_on_screen(player_x, player_y, self.pos_x, self.pos_y))
        pg.draw.rect(win,(255,0,0),self.rect)



