import random
import time

from typing import List, Tuple


class Field:
    def __init__(self, width: int, height: int, number_of_mines: int):
        self.SEED: int = round(time.time())
        self.WIDTH: int = width
        self.HEIGHT: int = height
        self.data: List[List[int]] = [[0] * width for _ in range(height)]
        #data[i][j] is number from -1 to 8 where 0 is empty, -1 is mine, 1-8 is number of mines nearby
        self.NUMBER_OF_MINES: int = number_of_mines #number of mines 
        
        self.generate()


    def get_neighbors(self, x: int, y: int) -> int:
        '''Returns a number of neighbors of cell with x, y coords'''
        w, h = self.WIDTH, self.HEIGHT
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
        k = 0 # mines counter
        while k < self.NUMBER_OF_MINES:
            x = random.randint(0, self.WIDTH-1)
            y = random.randint(0, self.HEIGHT-1) 
            if self.data[y][x] != -1:
                k += 1
                self.data[y][x] = -1

        #generate blocks with numbers
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if self.data[y][x] != -1:
                    nei = self.get_neighbors(x, y)
                    self.data[y][x] = nei    
        

class Game:
    def __init__(self, field: Field):
        self.field = field
        self.clicked: List[Tuple[int, int]] = []
        self.flaged: List[Tuple[int, int]] = []

    def cascade_click(self, x: int, y: int):
        '''Run through all empty blocks and click on it'''
        if x < 0 or y < 0 or x >= self.field.WIDTH or y >= self.field.HEIGHT:
            return
        if (x, y) in self.clicked or (x, y) in self.flaged:
            return
        
        point: int = self.field.data[y][x]

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
        

    def get_vision(self) -> List[List[int]]:
        '''Gets a vision for player.'''
        vis = [[0] * self.field.WIDTH for _ in range(self.field.HEIGHT)]

        for x, y in self.clicked:
            vis[y][x] = self.field.data[y][x]

        return vis


    def on_click(self, x: int, y: int) -> int:
        '''
        Handles a left click event
        returns 1 if clicked on flaged cell
        return -1 if clicked on mine(game over)
        return 0 if clicked on basic cell
        '''
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
