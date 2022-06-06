import pygame as pg
import numpy as np
from math import sqrt
from functions import *
import math
from game_params import walking


class Player(pg.sprite.Sprite):
    def __init__(self,width, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.screen_x,self.screen_y = location_on_screen(self.x,self.y,self.y,self.y)

        self.image = walking[0]
        self.rect = self.image.get_rect()
        self.width = width
        self.animation_count = 0
        self.walking = False
        self.health = 10
        self.speed = 1


    def update(self,win):
        self.screen_x, self.screen_y = location_on_screen(self.x, self.y, self.x, self.y)
        if self.health == 0:
            pg.event.set_blocked(pg.KEYDOWN)
            return

        if self.walking:
            self.animation_count += 1
        mouse_x, mouse_y = pg.mouse.get_pos()
        if (WIN_WIDTH / 2 - mouse_y) ** 2 + (WIN_HEIGHT / 2 - mouse_x) ** 2 > 1:
            self.angle = -math.atan2(self.screen_y - mouse_y, self.screen_x - mouse_x) * 180 / math.pi + 90

        rep_frames = 5
        if self.animation_count + 1 >= rep_frames*len(walking):
            self.animation_count = 0

        self.image = pg.transform.rotate(walking[self.animation_count // rep_frames], self.angle)
        # win.blit(img_copy,
        #          (self.screen_x - int(img_copy.get_width() / 2), self.screen_y - int(img_copy.get_height() / 2)))

        newrect = list(location_on_screen(self.x, self.y, self.x, self.y))
        newrect[0] -= int(self.image.get_width() / 2)
        newrect[1] -= int(self.image.get_height() / 2)
        self.rect.topleft = newrect
        # pg.draw.rect(win,(255,0,0),self.rect)

    def set_speed(self, val):
        self.speed = val

    def move(self, vector):
        n = sqrt(sum([i**2 for i in vector]))
        if n != 0:
            vector = [i/n for i in vector]

        self.x += vector[0]*self.speed
        self.y += vector[1]*self.speed
