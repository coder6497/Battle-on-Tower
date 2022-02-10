import sys

import pygame as pg
import json
import os


class About:
    def __init__(self):
        pg.init()

        self.file_dir = os.path.dirname(__file__)
        self.json_conf_dir = os.path.join(self.file_dir)
        self.font_dir = os.path.join(self.file_dir)
        self.img_dir = os.path.join(self.file_dir)

        with open(os.path.join(self.json_conf_dir, "file_paths.json")) as file_paths:
            self.data = json.load(file_paths)

        self.font_file1 = os.path.join(self.font_dir, self.data["fonts"][1])
        self.font_file2 = os.path.join(self.font_dir, self.data["fonts"][0])
        self.background_img = pg.image.load(os.path.join(self.img_dir, self.data["images"]["menu_imgs"]["background"]))
        self.logo_img = pg.image.load(os.path.join(self.img_dir, self.data["images"]["icon"]))

        self.height, self.width = 1000, 600
        self.screen = pg.display.set_mode((self.height, self.width))
        self.colors = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
        pg.display.set_caption("Battle on Tower {ABOUT}")
        self.cycle()

    def cycle(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
            self.update_screen()

    def text_render(self, text, font, size, color, x, y):
        font = pg.font.Font(font, size)
        text = font.render(text, True, color)
        self.screen.blit(text, (x, y))

    def draw_message(self):
        pg.draw.rect(self.screen, self.colors[1],  (100, 100, 800, 400), 3)
        self.text_render("Battle on Tower 2.0 beta", self.font_file1, 50, self.colors[2], 100, 120)

    def update_screen(self):
        self.screen.blit(self.background_img, (0, 0))
        self.draw_message()
        pg.display.update()
