import pygame as pg
import minesweeper as ms_core

pg.init()


class App:
    def __init__(self):
        self.WIDTH, self.HEIGHT = (800, 600)
        self.screen = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        self.FPS = 60
        self.clock = pg.time.Clock()
        self.TILE_SIZE = 40
        self.W_TILES, self.H_TILES = self.WIDTH // self.TILE_SIZE, self.HEIGHT // self.TILE_SIZE

    def check_input(self):
        pass

    def update_state(self):
        pass

    def render_frame(self):
        pass

    def run(self):
        is_running = True

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
    