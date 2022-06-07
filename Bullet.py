import pygame as pg
from functions import *
import math
from game_params import gun_sound



class Bullet(pg.sprite.Sprite):
    base_speed = 50

    def __init__(self, x, y,mouse_x, mouse_y, source):
        super().__init__()
        self.image = pg.Surface((10,10))
        self.image.fill((255,255,0))
        self.rect = self.image.get_rect()
        self.source = source
        self.x = x
        self.y = y
        self.player_x = 0
        self.player_y = 0
        # locate the end of a gun
        self.x_screen, self.y_screen = location_on_screen(self.player_x, self.player_y, self.x, self.y)
        if type(source).__name__ == 'Player':
            weap_len = 15
            half_width = 40
            some_angle = -(math.pi / 2 - math.atan(weap_len / half_width)) * 180 / math.pi
            self.x = x + math.cos((self.source.angle - some_angle) * math.pi / 180) * math.sqrt(weap_len ** 2 + half_width ** 2)
            self.y = y - math.sin((self.source.angle - some_angle) * math.pi / 180) * math.sqrt(weap_len ** 2 + half_width ** 2)
            self.x_screen, self.y_screen = location_on_screen(self.source.x, self.source.y, self.x, self.y)

        self.rect.center = (self.x_screen, self.y_screen)
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
        self.speed = 100
        self.angle = math.atan2(y - mouse_y, x - mouse_x)
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        if type(source).__name__ == 'Enemy':
            self.x -= int(self.x_vel)
            self.y -= int(self.y_vel)

        # gun_sound.play()
        # print(self.angle,self.x_vel,self.y_vel)

    def update(self, win, vel, player_x, player_y):
        self.player_x, self.player_y = player_x, player_y
        self.speed = Bullet.base_speed * vel    
        self.x_vel = math.cos(self.angle) * self.speed
        self.y_vel = math.sin(self.angle) * self.speed
        self.x -= int(self.x_vel)/30
        self.y -= int(self.y_vel)/30
        self.x_screen, self.y_screen = location_on_screen(self.player_x, self.player_y, self.x, self.y)
        self.rect.center = list((self.x_screen, self.y_screen))
        pg.draw.rect(win,(0,255,255),self.rect)

    
