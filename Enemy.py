from functions import location_on_screen
import numpy as np
from cmath import inf
from game_params import WIN_WIDTH,WIN_HEIGHT,walking,WALLS_CORDS,WALL_WIDTH, MAP_HEIGHT, MAP_WIDTH, POSSIBLE_SQUARES, EDGES
import pygame
from Bullet import Bullet
import math
from queue import PriorityQueue

MAX_INT = 1000000



def locate_square(x, y):
    return x//WALL_WIDTH,y//WALL_WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, bullets_group):
        super().__init__()
        self.x = x
        self.y = y
        self.bullets_group = bullets_group
        self.screen_x, self.screen_y = location_on_screen(0,0,self.x,self.y)
        self.image = walking[0]
        self.rect = self.image.get_rect()
        self.width = walking[0].get_width()
        self.animation_count = 0
        self.walking = False
        self.health = 10
        self.shot_wait = 0
        self.shot_fire = 12
        self.speed = 1
        self.base_speed = 0.8
        self.dijkstra_ctr = 0
        self.path = []
        self.info = 0
        self.square_to_go = (0,0)
        self.player_x = -1
        self.player_y = -1
        self.seen = False
        self.shoot = False
        
    def update(self, win, player_x, player_y, playerBullets, vel):
        if vel < 10:
            self.speed = vel*self.base_speed
        # print(self.x,self.y)
        
        self.player_x, self.player_y = player_x ,player_y
        
        self.screen_x, self.screen_y = location_on_screen(
            self.player_x, self.player_y, self.x+self.width/2, self.y) 

                

        # walks toward player
        
        
        # self.x_vel = math.cos(angle) * self.speed
        # self.y_vel = math.sin(angle) * self.speed
        y_dist = self.y - self.player_y
        x_dist = self.x - self.player_x
        dist = math.hypot(y_dist, x_dist)
       
        
        if dist > WALL_WIDTH and dist < 1000:
            
            self.walking = True
            self.dijkstra_ctr %= 60
            if self.dijkstra_ctr == 0:
                self.path = self.find_path(locate_square(self.player_x,self.player_y))
            self.dijkstra_ctr += 1
            curr_sqr = locate_square(self.x+self.width, self.y+self.width)
            f = False
            if self.path != None:
                vector=(0,0)
                for i in self.path[::-1]:
                    if i == curr_sqr:
                        f = True
                    if i != curr_sqr and f:
                        vector = list(np.array([i[0]*WALL_WIDTH - WALL_WIDTH/2,i[1]*WALL_WIDTH - WALL_WIDTH/2])-np.array([self.x,self.y]))
                        self.move(vector)
                        break
                self.angle = math.atan2(vector[1], vector[0])
            else:
                self.walking = False
        else:
            self.walking = False
 
        

        # walking animation
        if self.walking:
            self.animation_count += 1
        
      
        if self.animation_count + 1 >= 24:
            self.animation_count = 0
        self.image = pygame.transform.rotate(
            walking[self.animation_count // 3], -self.angle*180/math.pi-90) 
        self.image.set_colorkey((0, 0, 0))
        self.rect.topleft = self.screen_x,self.screen_y

        # shooting
        self.shot_wait += 1
        if self.shot_wait == self.shot_fire:
            self.shot_wait = 0
            new_bullet = Bullet(self.x, self.y, self.player_x, self.player_y, self)
            playerBullets.append(new_bullet)
            self.bullets_group.add(new_bullet)
        pygame.draw.rect(win,(255,0,0),pygame.Rect(self.screen_x,self.screen_y,self.health*10,10))
        if self.health <=0:
            self.kill
            
                        
    def move(self, vector):
        n  = math.sqrt(sum([i**2 for i in vector]))
        if n != 0:
            vector = [i/n for i in vector]

        self.x += vector[0]*self.speed
        self.y += vector[1]*self.speed
    

    def find_path(self,v):
        start_v = locate_square(self.x+self.width,self.y+self.width)
        # if start_v not in POSSIBLE_SQUARES:
        #     start_v = locate_square(self.x+self.width,self.y+self.width)
        if v == start_v:
            return
        n = len(POSSIBLE_SQUARES)
        d = {}
        q = PriorityQueue()
        prev = {}
        visited = [start_v]
        for i in POSSIBLE_SQUARES:
            d[i] = MAX_INT
        
        try:
            for i in EDGES[start_v]:
                q.put(i,-1)
                d[i] = 1
                prev[i] = start_v
        except KeyError:
            print("sprite alignment fault")
        
        while not q.empty():
            curr = q.get()
            if curr == v:
                break
            visited.append(curr)
            neigh = EDGES[curr]
            for j in neigh:
                if j not in visited and d[j] > d[curr] + 1:
                    d[j] = d[curr] + 1
                    prev[j] = curr
                    q.put(j,-d[j])
        
        vtmp = v
        path = [v]
        try:
            while vtmp!= start_v:
                vtmp = prev[vtmp]
                path.append(vtmp)
        except KeyError:
            print("sprite alignment fault")
        return(path)
    
    def see_player(self):
        xtmp = self.x 
        ytmp = self.y
        x = self.player_x
        y = self.player_y
        
    def get_position(self):
        return self.x,self.y
    
    def set_seen(self, seen):
        self.seen = seen
    
    def take_damage(self):
        self.health -= 1