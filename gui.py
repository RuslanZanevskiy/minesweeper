import pygame as pg
import minesweeper as ms_core
import time

pg.init()


class App:
    def __init__(self):
        self.WIDTH, self.HEIGHT = (400, 600)
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.FPS = 60
        self.clock = pg.time.Clock()
        self.TILE_SIZE = 40
        self.W_TILES, self.H_TILES = self.WIDTH // self.TILE_SIZE, self.HEIGHT // self.TILE_SIZE
        print('app created')
        self.pressed = False
        self.first_click = 0

    def check_action(self):
        x, y = pg.mouse.get_pos()
        x //= self.TILE_SIZE 
        y //= self.TILE_SIZE

        if pg.mouse.get_pressed()[0]:
            if self.pressed:
                return
            r = self.game.on_click(x, y)
            if r == -1:
                self.is_running = False
                self.win = -1
            self.pressed = True
        elif pg.mouse.get_pressed()[2]:
            if self.pressed:
                return
            self.game.on_flag(x, y)
            self.pressed = True
        else:
            self.pressed = False
        
        if self.pressed and self.first_click == 0:
            self.first_click = time.time()


    def render_frame(self):
        self.screen.fill((200, 200, 200))

        for i in range(self.WIDTH):
            pg.draw.line(self.screen, (0, 0, 0), (i * self.TILE_SIZE, 0), (i * self.TILE_SIZE, self.HEIGHT))
        for i in range(self.HEIGHT):
            pg.draw.line(self.screen, (0, 0, 0), (0, i * self.TILE_SIZE), (self.WIDTH, i * self.TILE_SIZE))

        hts = self.TILE_SIZE // 2
        ts10 = self.TILE_SIZE // 10
        font = pg.font.SysFont('arial', round(self.TILE_SIZE / 1.5))
        for y, row in enumerate(self.game.get_vision()):
            for x, col in enumerate(row):
                if col != 0 or (x, y) in self.game.clicked or (x, y) in self.game.flaged:
                    pg.draw.rect(self.screen, (230, 230, 230), (x * self.TILE_SIZE+1, y * self.TILE_SIZE+1, self.TILE_SIZE-1, self.TILE_SIZE-1))
                if (x, y) in self.game.flaged:
                    tmp = self.TILE_SIZE // 3
                    pg.draw.rect(self.screen, (0, 0, 0), (x * self.TILE_SIZE + tmp, y * self.TILE_SIZE + tmp, tmp, tmp))
                elif col == -1:
                    pg.draw.circle(self.screen, (0, 0, 0), (x * self.TILE_SIZE + hts, y * self.TILE_SIZE + hts), hts // 1.5)
                elif col != 0:
                    text = font.render(str(col), True, (0, 0, 0))
                    self.screen.blit(text, (x * self.TILE_SIZE + hts - ts10 , y * self.TILE_SIZE + ts10))
                    
        pg.display.update()

    def run(self):
        print('running...')
        self.is_running = True
        self.win = 0

        self.field = ms_core.Field(self.W_TILES, self.H_TILES, round(self.W_TILES * self.H_TILES * 0.15))
        self.game = ms_core.Game(self.field)
        
        for row in self.field.data:
            for col in row:
                sym = ' ' if col == 0 else '*' if col == -1 else str(col)
                print(sym, end='')
            print()

        while self.is_running:
            self.clock.tick(self.FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.is_running = False

            self.check_action()
            self.render_frame()

            if len(self.game.flaged) == self.field.N and len(self.game.clicked) == self.field.H * self.field.W - self.field.N:
                self.win = 1
                self.is_running = False

        if self.win == 1:
            print('win')
        elif self.win == -1:
            print('lose')

        record = time.time() - self.first_click
        m, s = int(record // 60), round(record % 60)
        print()
        print(f'Time - {m}:{(str(0) + str(s)) if s < 10 else s}')


        #shows all mines and blocks
        self.game.clicked = []
        for x in range(self.field.W):
            for y in range(self.field.H):
                if (x, y) not in self.game.flaged:
                    self.game.clicked.append((x, y))
                else:
                    if self.field.data[y][x] != -1:
                        self.game.flaged.remove((x, y))
                        self.game.clicked.append((x, y))

        while 1:
            self.clock.tick(self.FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 0
            self.render_frame()


if __name__ == '__main__':
    app = App()
    app.run()
    