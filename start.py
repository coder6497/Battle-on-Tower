import json
import os

import pygame as pg

from about import About
from game import App


class Menu:
    def __init__(self):
        pg.init()
        pg.mixer.init()

        self.file_dir = os.path.dirname(__file__)
        self.json_conf_dir = os.path.join(self.file_dir)
        self.font_dir = os.path.join(self.file_dir)
        self.img_dir = os.path.join(self.file_dir)

        with open(os.path.join(self.json_conf_dir, "file_paths.json")) as file_paths:
            self.data = json.load(file_paths)

        self.font_file = os.path.join(self.font_dir, self.data["fonts"][1])
        self.background_img = pg.image.load(os.path.join(self.img_dir, self.data["images"]["menu_imgs"]["background"]))
        self.logo_img = pg.image.load(os.path.join(self.img_dir, self.data["images"]["icon"]))
        self.play_btn = pg.image.load(os.path.join(self.img_dir, self.data["images"]["menu_imgs"]["buttons"][0]))
        self.quit_btn = pg.image.load(os.path.join(self.img_dir, self.data["images"]["menu_imgs"]["buttons"][1]))
        self.about_btn = pg.image.load(os.path.join(self.img_dir, self.data["images"]["menu_imgs"]["buttons"][2]))

        self.height, self.width = 1000, 600
        self.screen = pg.display.set_mode((self.height, self.width))
        pg.display.set_caption("Battle on Tower {MENU}")
        pg.display.set_icon(self.logo_img)
        self.colors = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255)]
        self.menu = True
        self.menu_cycle()

    def menu_cycle(self):
        while self.menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.menu = False
                self.button_press_event(event)
                self.update_screen()

    def text_render(self, text, font, size, color, x, y):
        font = pg.font.Font(font, size)
        text = font.render(text, True, color)
        self.screen.blit(text, (x, y))

    def draw_buttons(self):
        global play_btn_rect, quit_btn_rect, about_btn_rect
        play_btn_rect = self.play_btn.get_rect(center=self.play_btn.get_rect(topleft=(400, 200)).center)
        quit_btn_rect = self.play_btn.get_rect(center=self.play_btn.get_rect(topleft=(400, 300)).center)
        about_btn_rect = self.play_btn.get_rect(center=self.play_btn.get_rect(topleft=(400, 400)).center)
        self.screen.blit(self.play_btn, play_btn_rect)
        self.screen.blit(self.quit_btn, quit_btn_rect)
        self.screen.blit(self.about_btn, about_btn_rect)

    def button_press_event(self, event):
        global play_btn_rect, quit_btn_rect, about_btn_rect
        if event.type == pg.MOUSEBUTTONUP:
            mouse_pos = pg.mouse.get_pos()
            if play_btn_rect.collidepoint(mouse_pos):
                App()
                self.menu = False
            if quit_btn_rect.collidepoint(mouse_pos):
                self.menu = False
            if about_btn_rect.collidepoint(mouse_pos):
                About()
                self.menu = False

    def update_screen(self):
        self.screen.blit(self.background_img, (0, 0))
        self.draw_buttons()
        pg.display.update()


if __name__ == "__main__":
    menu = Menu()
