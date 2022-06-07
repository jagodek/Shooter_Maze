import pygame as pg
import numpy as np
from Enemy import Enemy

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
        self.enemies = []
        self.wait_damage = 60
        self.dmg_ctr = 0
        self.no_harm = False


    def update(self,win):
        self.screen_x, self.screen_y = location_on_screen(self.x, self.y, self.x, self.y)
        if self.health == 0:
            pg.event.set_blocked(pg.KEYDOWN)
            return

        if self.no_harm:
            self.dmg_ctr += 1
            if self.dmg_ctr == self.wait_damage:
                self.dmg_ctr = 0
                self.no_harm = False
        
        
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
        self.in_sight()
        # pg.draw.rect(win,(255,0,0),self.rect)

    def set_speed(self, val):
        self.speed = val

    def move(self, vector):
        if not self.health <= 0:
            n = math.sqrt(sum([i**2 for i in vector]))
            if n != 0:
                vector = [i/n for i in vector]  

            self.x += int(vector[0]*self.speed)
            self.y += int(vector[1]*self.speed)
        
    def take_damage(self):
        if not self.no_harm:
            self.health -=1
            self.no_harm = True
        
        
    
    def add_enenmy(self,enemy):
        self.enemies.append(enemy)
    
    def in_sight(self):
        for e in self.enemies:
            xe,ye = e.get_position()
            x,y = self.x, self.y
            x_diff = xe - x
            y_diff = ye - y
            r = int(max(x_diff,y_diff))
            seen = True
            for i in range(r):
                if is_wall(x + int(i/r),y + int(i/r)):
                    seen = False
                    break
            e.set_seen(seen)
            
                
                
            