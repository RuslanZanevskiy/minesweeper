import random


class Field:
    def __init__(self, w, h, number):
        self.W = w
        self.H = h
        self.data = [[0] * w for _ in range(h)]
        self.N = number
        self.generate()
        print('field created')

    def get_neighbors(self, x, y):
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
        print('start generating field')
        k = 0
        while k < self.N:
            x, y = random.randint(0, self.W-1), random.randint(0, self.H-1) 
            if self.data[y][x] != -1:
                k += 1
                self.data[y][x] = -1
        print('mines generated')

        for y in range(self.H):
            for x in range(self.W):
                if self.data[y][x] != -1:
                    nei = self.get_neighbors(x, y)
                    self.data[y][x] = nei    
        print('number blocks generated')
        

class Game:
    def __init__(self, field):
        self.field = field
        self.clicked = []
        self.flaged = []

    def dfs(self, x, y, vis):
        if [x, y] in self.flaged:
            return
        if self.field.data[y][x] == -1:
            pass
        

    def get_vision(self):
        vis = [[False] * self.field.W for _ in range(self.field.H)]

        for x, y in self.clicked:
            self.dfs(x, y, vis)

    
