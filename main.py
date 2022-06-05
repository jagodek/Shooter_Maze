import pygame
import os
import numpy as np
import math
import sys
from pathlib import Path
from Player import Player
from Bullet import Bullet
from Wall import Wall
from Button import Button
from functions import *

from game_params import WIN_WIDTH, WIN_HEIGHT, walking, bg, MAP_WIDTH, MAP_HEIGHT, WALLS_CORDS


BG = pygame.image.load(Path("textures/assets/Background.png"))


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(Path("textures/assets/font.ttf"), size)

class Enemy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.screen_x = None
        self.screen_y = None
        self.width = walking[0].get_width()
        self.height = walking[0].get_height()
        self.animation_count = 0
        self.walking = False
        self.health = 10
        self.hitbox = None
        self.shot_wait = 0
        self.shot_fire = 12
        self.speed = 9

    def main(self, win):
        self.screen_x, self.screen_y = location_on_screen(
            player.x, player.y, self.x, self.y)

        self.hitbox = pygame.Rect(self.screen_x, self.screen_y, 0, 0).inflate(
            self.width / 2, self.height / 2)

        pygame.draw.rect(win, (255, 0, 0), (self.screen_x,
                     self.screen_y + 20, 20 * self.health, 20))

        # walks toward player
        angle = math.atan2(self.y - player.y, self.x - player.x)
        self.x_vel = math.cos(angle) * self.speed
        self.y_vel = math.sin(angle) * self.speed
        y_dist = self.y - player.y
        x_dist = self.x - player.x
        dist = math.hypot(y_dist, x_dist)
        if dist > 10 and dist < 1000:
            self.walking = True
            self.x -= int(self.x_vel)
            self.y -= int(self.y_vel)
        else:
            self.walking = False

        # walking animation
        if self.walking:
            self.animation_count += 1
        aim_x, aim_y = player.screen_x, player.screen_y
        if (WIN_WIDTH / 2 - aim_y) ** 2 + (WIN_HEIGHT / 2 - aim_x) ** 2 > 1:
            self.angle = -math.atan2(self.screen_y - aim_y,
                                     self.screen_x - aim_x) * 180 / math.pi + 90
        if self.animation_count + 1 >= 24:
            self.animation_count = 0
        img_copy = pygame.transform.rotate(
            walking[self.animation_count // 3], self.angle)
        img_copy.set_colorkey((0, 0, 0))
        win.blit(img_copy,
                 (self.screen_x - int(img_copy.get_width() / 2), self.screen_y - int(img_copy.get_height() / 2)))

        # shooting
        self.shot_wait += 1
        if self.shot_wait == self.shot_fire:
            self.shot_wait = 0
            playerBullets.append(
                Bullet(self.x, self.y, player.x, player.y, self))


class Backgrounds:
    def __init__(self):
        self.positions = []
        for i in range(MAP_WIDTH // bg.get_size()[0] + 1):
            for j in range(MAP_HEIGHT // bg.get_size()[1] + 1):
                self.positions += [(i * bg.get_size()[0],
                                    j * bg.get_size()[1])]

    def main(self, win):
        for i in self.positions:
            screen_x, screen_y = location_on_screen(
                player.x, player.y, i[0], i[1])
            win.blit(bg, (screen_x, screen_y))



    


def redrawGameWindow(win):
    backgrounds.main(win)
    walls_group.update(win, player.x, player.y)
    walls_group.draw(win)
    player_group.update(win)
    player_group.draw(win)
    bullets_group.update(win)
    bullets_group.draw(win)
    for enemy in enemies:
        enemy.main(win)

    pygame.draw.rect(win, (255, 0, 0), (player.screen_x, player.screen_y, 4, 4))
    pygame.draw.rect(win, (255, 0, 0), (60, 30, 20 * player.health, 20))

    pygame.display.update()


def handle_bullet(bullets_group, vel):
    pygame.sprite.groupcollide(bullets_group, walls_group, True, False)
    for bullet in bullets_group:
        if not (-MAP_WIDTH < bullet.rect.topleft[0] < MAP_WIDTH and -MAP_HEIGHT < bullet.rect.topleft[1] < MAP_HEIGHT):
            bullets_group.remove(bullet)
        bullet.set_speed(vel)


def detect_collision(walls_group, vel):
    barrier_adj = 5 + player.width/3
    right_block = False
    left_block = False
    down_block = False
    up_block = False
    for w in walls_group:
        if w.rect.collidepoint(player.screen_x+vel+barrier_adj, player.screen_y-player.width/3) or \
                w.rect.collidepoint(player.screen_x+vel+barrier_adj, player.screen_y+player.width/3):
            right_block = True
        if w.rect.collidepoint(player.screen_x-vel-barrier_adj, player.screen_y-player.width/3) or \
                w.rect.collidepoint(player.screen_x-vel-barrier_adj, player.screen_y+player.width/3):
            left_block = True
        if w.rect.collidepoint(player.screen_x-player.width/3, player.screen_y+vel+barrier_adj) or \
                w.rect.collidepoint(player.screen_x+player.width/3, player.screen_y+vel+barrier_adj):
            down_block = True
        if w.rect.collidepoint(player.screen_x-player.width/3, player.screen_y-vel-barrier_adj) or \
                w.rect.collidepoint(player.screen_x+player.width/3, player.screen_y-vel-barrier_adj):
            up_block = True
    return (right_block, left_block, down_block, up_block)


def handle_keys(vel,right_block, left_block, down_block, up_block):
    keys = pygame.key.get_pressed()
    k_pressed = False
    player_move_vector = [0, 0]
    if keys[pygame.K_a] and player.x > vel and not left_block:
        k_pressed = True
        player_move_vector = np.add(player_move_vector, [-1, 0]).tolist()
        player.walking = True

    if keys[pygame.K_d] and player.x + 1 < MAP_WIDTH - vel - player.width / 2 and not right_block:
        k_pressed = True
        player_move_vector = np.add(player_move_vector, [1, 0]).tolist()
        player.walking = True

    if keys[pygame.K_w] and player.y - 1 > vel and not up_block:
        k_pressed = True
        player_move_vector = np.add(player_move_vector, [0, -1]).tolist()
        player.walking = True

    if keys[pygame.K_s] and player.y + 1 < MAP_HEIGHT - vel - player.width / 2 and not down_block:
        k_pressed = True
        player_move_vector = np.add(player_move_vector, [0, 1]).tolist()
        player.walking = True

    if not k_pressed:
        player.walking = False

    player.move(player_move_vector)


def play_game(WIN):
    WIN.fill("black")
    while True:
        time_passed = clock.tick(50)
        print(time_passed)
        time_passed /= 1000
        print(time_passed)
        vel = base_vel*time_passed
        player.set_speed(vel)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        map_mouse_x, map_mouse_y = location_on_map(
            player.x, player.y, mouse_x, mouse_y)  # position of mouse on map

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    bullets_group.add(
                        Bullet(player.x, player.y, map_mouse_x, map_mouse_y, player))

        
        # for i in playerBullets:
        #     point = i.x_screen, i.y_screen
            #     if i.source != player and player.health > 0:
        #         player.health -= 1
        #     for e in enemies:
        #         if i.source == player and e.hitbox.collidepoint(point):
        #             e.health -= 1

        # removes bullet outside the map
        handle_bullet(bullets_group, vel)

        

        # detect collision
        right_block, left_block, down_block, up_block = detect_collision(walls_group, vel)

        handle_keys(vel,right_block, left_block, down_block, up_block)
    
        
        redrawGameWindow(WIN)
        
def main_menu(WIN,exitgame):
    
    WIN.fill("black")
    while True:
        WIN.blit(BG, (0,0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIN_WIDTH//2, WIN_HEIGHT//5))

        PLAY_BUTTON = Button(image=pygame.image.load(Path("textures/assets/Play Rect.png")), pos=(WIN_WIDTH//2, WIN_HEIGHT//5*2), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load(Path("textures/assets/Options Rect.png")), pos=(WIN_WIDTH//2, WIN_HEIGHT//5*3), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load(Path("textures/assets/Quit Rect.png")), pos=(WIN_WIDTH//2, WIN_HEIGHT//5*4), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play_game(WIN)
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pass
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        
    

def main():
    pygame.init()
    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Shooter_Maze")
    exitgame = False
    main_menu(WIN,exitgame)
    

    


if __name__ == '__main__':
    base_vel = 300
    player_size = (walking[0].get_width() + walking[0].get_height())/2
    player_group = pygame.sprite.Group()
    player = Player(player_size, WIN_WIDTH / 4 * 3, WIN_HEIGHT / 3 * 4)
    player_group.add(player)
    clock = pygame.time.Clock()
    bullets_group = pygame.sprite.Group()
    playerBullets = []
    enemies = []  # Enemy(10,10)]
    walls_group = pygame.sprite.Group()
    for wall in WALLS_CORDS:
        walls_group.add(Wall(1, 1, wall[0], wall[1]))

    backgrounds = Backgrounds()
    main()
