import pygame as pg
import minesweeper as ms_core

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

    def check_input(self):
        pass

    def update_state(self):
        pass

    def render_frame(self):
        self.screen.fill((200, 200, 200))

        for i in range(self.WIDTH):
            pg.draw.line(self.screen, (0, 0, 0), (i * self.TILE_SIZE, 0), (i * self.TILE_SIZE, self.HEIGHT))
        for i in range(self.HEIGHT):
            pg.draw.line(self.screen, (0, 0, 0), (0, i * self.TILE_SIZE), (self.WIDTH, i * self.TILE_SIZE))

        hts = self.TILE_SIZE // 2
        ts10 = self.TILE_SIZE // 10
        font = pg.font.SysFont('arial', round(self.TILE_SIZE / 1.5))
        for y, row in enumerate(self.field.data):
            for x, col in enumerate(row):
                if col == -1:
                    pg.draw.circle(self.screen, (0, 0, 0), (x * self.TILE_SIZE + hts, y * self.TILE_SIZE + hts), hts // 1.5)
                elif col != 0:
                    text = font.render(str(col), True, (0, 0, 0))
                    self.screen.blit(text, (x * self.TILE_SIZE + hts - ts10 , y * self.TILE_SIZE + ts10))
        pg.display.update()

    def run(self):
        print('running...')
        is_running = True


        self.field = ms_core.Field(self.W_TILES, self.H_TILES, round(self.W_TILES * self.H_TILES * 0.15))
        for row in self.field.data:
            for col in row:
                sym = ' ' if col == 0 else '*' if col == -1 else str(col)
                print(sym, end='')
            print()
        

        while is_running:
            self.clock.tick(self.FPS)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    is_running = False

            self.check_input()
            self.update_state()
            self.render_frame()


if __name__ == '__main__':
    app = App()
    app.run()
    