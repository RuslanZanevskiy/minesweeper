import random
import time


class Field:
    def __init__(self, w, h, number):
        self.SEED = round(time.time())
        self.W = w
        self.H = h
        self.data = [[0] * w for _ in range(h)]
        #data[i][j] is number from -1 to 8 where 0 is empty, -1 is mine, 1-8 is number of mines nearby
        self.N = number #number of mines 
        self.generate()


    def get_neighbors(self, x, y):
        '''Returns a number of neighbors of cell with x, y coords'''
        w, h = self.W, self.H
        nei = 0
        if x != 0 and self.data[y][x-1] == -1:
            nei += 1
        if x != w-1 and self.data[y][x+1] == -1:
            nei += 1
        if y != 0 and self.data[y-1][x] == -1:
            nei += 1
        if y != h-1 and self.data[y+1][x] == -1:
            nei += 1
        
        if x != 0 and y != 0 and self.data[y-1][x-1] == -1:
            nei += 1
        if x != w-1 and y != 0 and self.data[y-1][x+1] == -1:
            nei += 1
        if x != 0 and y != h-1 and self.data[y+1][x-1] == -1:
            nei += 1
        if x != w-1 and y != h-1 and self.data[y+1][x+1] == -1:
            nei += 1
        return nei


    def generate(self):
        '''Generates mines and blocks with numbers on field'''
        random.seed(self.SEED)
        k = 0 #num of mines
        while k < self.N:
            x, y = random.randint(0, self.W-1), random.randint(0, self.H-1) 
            if self.data[y][x] != -1:
                k += 1
                self.data[y][x] = -1

        #generate blocks with numbers
        for y in range(self.H):
            for x in range(self.W):
                if self.data[y][x] != -1:
                    nei = self.get_neighbors(x, y)
                    self.data[y][x] = nei    
        

class Game:
    def __init__(self, field):
        self.field = field
        self.clicked = []
        self.flaged = []

    def cascade_click(self, x, y):
        '''Run through all empty blocks and click on it'''
        if x < 0 or y < 0 or x >= self.field.W or y >= self.field.H:
            return
        if (x, y) in self.clicked or (x, y) in self.flaged:
            return
        
        point = self.field.data[y][x]

        if point == -1:
            return
        elif point != 0:
            self.clicked.append((x, y))
        else:
            self.clicked.append((x, y))
            self.cascade_click(x+1, y)
            self.cascade_click(x, y+1)
            self.cascade_click(x-1, y)
            self.cascade_click(x, y-1)
        

    def get_vision(self):
        '''Gets a vision for player.'''
        vis = [[0] * self.field.W for _ in range(self.field.H)]

        for x, y in self.clicked:
            vis[y][x] = self.field.data[y][x]

        return vis


    def on_click(self, x, y):
        '''Handles a left click event'''
        if (x, y) in self.flaged:
            return 1
        if self.field.data[y][x] == -1: #if click on mine - game over
            return -1
        elif self.field.data[y][x] != 0:
            self.clicked.append((x, y))
        else:
            self.cascade_click(x, y)
        return 0


    def on_flag(self, x, y):
        '''Handles a right click event(flagging)'''
        if (x, y) in self.flaged:
            self.flaged.remove((x, y))
            return
        if (x, y) not in self.clicked:
            self.flaged.append((x, y))
