# This is source-code for Battle on Tower game

import json
import math
import os  # Modules for develop
import random
import sys

import pygame as pg


class App:  # Main class for game
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.keys = {"rotate_left": pg.K_a,  # dictionaries with keys
                     "rotate_right": pg.K_d,
                     "shot": pg.K_SPACE,
                     "reload": pg.K_r}

        self.file_dir = os.path.dirname(__file__)  # file load optimization
        self.img_dir = os.path.join(self.file_dir)
        self.json_config_dir = os.path.join(self.file_dir)
        self.fonts_dir = os.path.join(self.file_dir)
        self.sounds_dir = os.path.join(self.file_dir)

        with open(os.path.join(self.json_config_dir,
                               'file_paths.json')) as file_paths:  # load json config with file paths
            self.data = json.load(file_paths)

        self.background_img = pg.image.load(
            os.path.join(self.img_dir,
                         random.choice(self.data["images"]["background"])))  # loading application files
        self.icon_img = pg.image.load(os.path.join(self.img_dir, self.data["images"]["icon"]))
        self.font_file = os.path.join(self.fonts_dir, self.data["fonts"][0])
        self.shot_sound_file = pg.mixer.Sound(os.path.join(self.sounds_dir, self.data["sounds"][0]))
        self.gameplay_sound_file = pg.mixer.Sound(os.path.join(self.sounds_dir, self.data["sounds"][1]))
        self.attack_sound_file = pg.mixer.Sound(os.path.join(self.sounds_dir, self.data["sounds"][2]))
        self.game_over_img = pg.image.load(os.path.join(self.img_dir, self.data["images"]["menu_imgs"]["game_over"]))
        self.button1_img = pg.image.load(os.path.join(self.img_dir, self.data["images"]["buttons"][0]))
        self.button2_img = pg.image.load(os.path.join(self.img_dir, self.data["images"]["buttons"][1]))

        self.gameplay_sound_file.play(-1)
        self.fps = 60  # main game params
        self.height, self.width = 1000, 600
        self.screen = pg.display.set_mode((self.height, self.width))
        pg.display.set_caption("Battle on Tower")
        pg.display.set_icon(self.icon_img)
        self.colors = [(0, 0, 0), (255, 255, 255), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (139, 69, 19)]
        self.clock = pg.time.Clock()

        self.tower_xp = 100  # common game object params
        self.ammo_count = 10
        self.kill_count = 0
        self.arm_angle = 0
        self.ray_x = 120
        self.ray_y = 120
        self.length = 400
        self.ray_angle = 0
        self.is_shoot = True
        self.reloading = False
        self.game_over = False

        self.all_sprites = pg.sprite.Group()  # sprite groups
        self.bullets = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.sprites_init()

        self.game_cycle()

    def game_cycle(self):  # game cycle
        while True:
            self.clock.tick(self.fps)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if self.game_over:
                    self.button_connect(event)
            self.update_screen()
            self.key_pressed()

    def draw_simple_objects(self):  # drawing simple objects
        ground_img = pg.image.load(os.path.join(self.img_dir, self.data["images"]["ground"]))

        image = pg.image.load(os.path.join(self.img_dir, self.data["images"]["player"][1]))
        new_img = pg.transform.rotate(image, self.arm_angle)
        rect = new_img.get_rect(center=image.get_rect(topleft=(95, 150)).center)

        self.screen.blit(ground_img, (0, 500))
        self.screen.blit(new_img, rect)
        pg.draw.circle(self.screen, self.colors[2],
                       (self.ray_x + self.length * math.cos(self.ray_angle * math.pi / 180),
                        self.ray_y + self.length * math.sin(self.ray_angle * math.pi / 180)), 8, 2)

    def key_pressed(self):
        keys = pg.key.get_pressed()
        if keys[self.keys["rotate_right"]]:
            self.arm_angle -= 2
            self.ray_angle += 2
        if keys[self.keys["rotate_left"]]:
            self.arm_angle += 2
            self.ray_angle -= 2

    def sprites_init(self):  # initialisation sprites
        global tower, enemy_on_sky, enemy_on_ground
        player = Player(x=100, y=150, colors=self.colors, screen=self.screen, keys=self.keys,
                        bullets=self.bullets, ammo_count=self.ammo_count, is_shoot=self.is_shoot,
                        reloading=self.reloading, data=self.data, img_dir=self.img_dir, ray_angle=self.ray_angle,
                        enemies=self.enemies, shot_sound_file=self.shot_sound_file)
        tower = Tower(x=50, y=120, colors=self.colors, tower_xp=self.tower_xp, enemies=self.enemies, data=self.data,
                      img_dir=self.img_dir)
        for i in range(3):
            enemy_on_sky = EnemyOnSky(x=5000 + i * 300, y=random.randint(200, 500), colors=self.colors,
                                      bullets=self.bullets,
                                      enemies=self.enemies,
                                      all_sprites=self.all_sprites, data=self.data, img_dir=self.img_dir, anim_count=0,
                                      screen=self.screen, length=200, ray_angle=self.ray_angle, rot_angle=3,
                                      width=self.width)
            self.enemies.add(enemy_on_sky)

        for i in range(3):
            enemy_on_ground = EnemyOnGround(x=2000, y=430, colors=self.colors, bullets=self.bullets,
                                            enemies=self.enemies, all_sprites=self.all_sprites, data=self.data,
                                            img_dir=self.img_dir, anim_count=0)
            self.enemies.add(enemy_on_ground)
        self.all_sprites.add(tower, player)

    def update_screen(self):  # update canvas for screen
        self.screen.blit(self.background_img, (-2, 0))
        if not self.game_over:  # if game lost, objects will be deleted
            self.all_sprites.update()
            self.bullets.update()
            self.enemies.update()
            self.all_sprites.draw(self.screen)
            self.bullets.draw(self.screen)
            self.enemies.draw(self.screen)
            self.draw_simple_objects()
        self.collision_with_tower()
        self.ammo_counter()
        self.lose()
        pg.display.update()

    def text_render(self, text, font, size, color, x, y):  # this method responding rendering text
        font = pg.font.Font(font, size)
        text = font.render(text, True, color)
        self.screen.blit(text, (x, y))

    def collision_with_tower(self):  # collision with tower
        global tower
        self.text_render(f'XP: {str(round(self.tower_xp))}', self.font_file, 40, self.colors[2], 0, 0)
        collide = pg.sprite.spritecollide(tower, self.enemies, False)
        if collide and self.tower_xp > 0:
            self.tower_xp -= 0.05
        if self.tower_xp <= 0:
            self.game_over = True

    def ammo_counter(self):  # quantity counter for ammo, if player shoots, ammo count reduced by one number.
        keys = pg.key.get_pressed()
        self.text_render(f'Ammo: {str(round(self.ammo_count))}', self.font_file, 40, self.colors[-3], 400, 0)
        if keys[self.keys["shot"]] and self.is_shoot and self.ammo_count > 0:
            self.ammo_count -= 1
            self.is_shoot = False
        if not keys[self.keys["shot"]]:
            self.is_shoot = True
        if keys[self.keys["reload"]]:
            self.reloading = True
        if self.reloading and self.ammo_count <= 10:
            self.ammo_count += 0.02
            self.text_render('Reloading...', self.font_file, 60, self.colors[-2], 400, 100)
        if not keys[self.keys["reload"]]:
            self.reloading = False

    def lose(self):
        global btn1_rect, btn2_rect  # if player lost, text "Game Over" will be displayed.
        if self.game_over:
            self.gameplay_sound_file.stop()
            self.screen.blit(self.game_over_img, (0, 0))
            self.text_render("Game Over", self.font_file, 100, self.colors[3], 200, 200)
            btn1_rect = self.button1_img.get_rect(center=self.button1_img.get_rect(topleft=(200, 400)).center)
            btn2_rect = self.button2_img.get_rect(center=self.button2_img.get_rect(topleft=(600, 400)).center)
            self.screen.blit(self.button1_img, btn1_rect)
            self.screen.blit(self.button2_img, btn2_rect)

    def button_connect(self, event):
        global btn1_rect, btn2_rect
        if event.type == pg.MOUSEBUTTONUP:
            mouse_pos = pg.mouse.get_pos()
            if btn1_rect.collidepoint(mouse_pos):
                pg.quit()
                App()
            if btn2_rect.collidepoint(mouse_pos):
                pg.quit()
                sys.exit()


class Player(pg.sprite.Sprite):  # class for player
    def __init__(self, x, y, colors, screen, keys, bullets, ammo_count, is_shoot, reloading, data,
                 img_dir, ray_angle, enemies, shot_sound_file):
        super(Player, self).__init__()
        self.x = x
        self.y = y
        self.colors = colors
        self.screen = screen
        self.keys = keys
        self.bullets = bullets
        self.ammo_count = ammo_count
        self.is_shoot = is_shoot
        self.reloading = reloading
        self.data = data
        self.img_dir = img_dir
        self.ray_angle = ray_angle
        self.enemies = enemies
        self.shot_sound_file = shot_sound_file
        self.image = pg.image.load(os.path.join(self.img_dir, self.data["images"]["player"][0]))
        self.rect = self.image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        self.attack = True  # variable which responsible for limit spawn bullets

    def update(self):  # this method responsible for update frame by frame
        self.key_pressed()
        self.ammo_counter_proc()

    def key_pressed(self):  # key pressing processing
        keys = pg.key.get_pressed()
        if keys[self.keys["shot"]]:
            self.shot()
            self.attack = False
        if not keys[self.keys["shot"]]:
            self.attack = True
        if keys[self.keys["rotate_right"]]:
            self.ray_angle += 2
        if keys[self.keys["rotate_left"]]:
            self.ray_angle -= 2

    def shot(self):  # this method responsible for spawn bullets
        if self.attack and self.ammo_count > 0:
            self.shot_sound_file.play()
            self.shot_sound_file.set_volume(0.5)
            bullet = Bullet(x=self.x, y=self.y, radius=5, colors=self.colors, speed=20, ray_angle=self.ray_angle,
                            keys=self.keys, enemies=self.enemies)
            self.bullets.add(bullet)

    def ammo_counter_proc(self):  # Reducing and reloading ammo
        keys = pg.key.get_pressed()
        if keys[self.keys["shot"]] and self.is_shoot and self.ammo_count > 0:
            self.ammo_count -= 1
            self.is_shoot = False
        if not keys[self.keys["shot"]]:
            self.is_shoot = True
        if keys[self.keys["reload"]]:
            self.reloading = True
        if self.reloading and self.ammo_count <= 10:
            self.ammo_count += 0.05
        if not keys[self.keys["reload"]]:
            self.reloading = False


class Bullet(pg.sprite.Sprite):  # class for bullets
    def __init__(self, x, y, speed, radius, colors, ray_angle, keys, enemies):
        super(Bullet, self).__init__()
        self.x = x
        self.y = y
        self.speed = speed
        self.colors = colors
        self.radius = radius
        self.ray_angle = ray_angle
        self.keys = keys
        self.enemies = enemies
        self.image = pg.Surface((self.radius * 2, self.radius * 2))
        self.image.set_colorkey(self.colors[0], False)
        pg.draw.circle(self.image, self.colors[-1], (self.radius, self.radius), self.radius)
        self.rect = pg.Rect(self.x, self.y, self.radius, self.radius)
        self.attack = True

    def update(self):
        self.force()
        self.key_pressed()

    def key_pressed(self):
        keys = pg.key.get_pressed()
        if keys[self.keys["rotate_right"]] and self.attack:
            self.ray_angle += 2
        if keys[self.keys["rotate_left"]] and self.attack:
            self.ray_angle -= 2

    def force(self):  # movement for ray direction
        self.rect.x += self.speed * math.cos(self.ray_angle * math.pi / 180)
        self.rect.y += self.speed * math.sin(self.ray_angle * math.pi / 180)
        self.attack = False


class EnemyOnGround(pg.sprite.Sprite):  # class for enemies(on ground)
    def __init__(self, x, y, colors, bullets, enemies, all_sprites, data, img_dir, anim_count):
        super(EnemyOnGround, self).__init__()
        self.x = x
        self.y = y
        self.colors = colors
        self.bullets = bullets
        self.enemies = enemies
        self.all_sprites = all_sprites
        self.data = data
        self.img_dir = img_dir
        self.anim_count = anim_count
        self.rand_keys = ["enemy", "enemy3"]
        self.rand = random.choice(self.rand_keys)
        self.image = pg.image.load(
            os.path.join(self.img_dir, self.data["images"][self.rand][0][0])).convert_alpha()
        self.rect = self.image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        self.isRunning = True
        self.isPunched = False
        self.isDead = False
        self.enemy1 = False
        self.enemy2 = False
        self.speed = random.randint(2, 5)

    def update(self):
        self.run()
        self.collision()
        self.animation()
        self.enemy_select()

    def enemy_select(self):
        match self.rand:
            case "enemy":
                self.enemy1 = True
            case "enemy3":
                self.enemy2 = True

    def run(self):
        if self.rect.x <= 150:  # movement
            self.isRunning = False
        if self.isRunning and not self.isDead:
            self.rect.x -= self.speed

    def collision(self):  # collision with bullets and spawn for initial position
        collide1 = pg.sprite.spritecollide(self, self.bullets, False)
        collide2 = pg.sprite.spritecollide(self, self.all_sprites, False)
        if collide1 or self.rect.x < 0:
            self.isDead = True
            list(map(lambda x: x.kill(), self.bullets))
        if self.isDead and self.anim_count < 3:
            self.kill()
            enemy_on_ground = EnemyOnGround(x=2000, y=430, colors=self.colors, bullets=self.bullets,
                                            enemies=self.enemies, all_sprites=self.all_sprites, img_dir=self.img_dir,
                                            data=self.data, anim_count=0)
            self.enemies.add(enemy_on_ground)
        if collide2:
            self.isPunched = True

    def anim_count_increment(self, n=1):
        self.anim_count += n
        self.anim_count %= 60

    def animation(self):
        if self.enemy1:
            if self.isRunning:
                self.image = pg.image.load(
                    os.path.join(self.img_dir, self.data["images"]["enemy"][0][self.anim_count // 10])).convert_alpha()
                self.anim_count_increment(1)
            if self.isPunched:
                self.image = pg.image.load(
                    os.path.join(self.img_dir, self.data["images"]["enemy"][1][self.anim_count // 12])).convert_alpha()
                self.anim_count_increment(2)
            if self.isDead:
                self.image = pg.image.load(
                    os.path.join(self.img_dir, self.data["images"]["enemy"][2][self.anim_count // 20])).convert_alpha()
                self.anim_count_increment(1)
                self.rect.y = 450
        if self.enemy2:
            if self.isRunning:
                self.image = pg.image.load(
                    os.path.join(self.img_dir, self.data["images"]["enemy3"][1][self.anim_count // 15])).convert_alpha()
                self.anim_count_increment(1)
            if self.isPunched:
                self.image = pg.image.load(
                    os.path.join(self.img_dir, self.data["images"]["enemy3"][0][self.anim_count // 6])).convert_alpha()
                self.anim_count_increment(1)
            if self.isDead:
                self.image = pg.image.load(
                    os.path.join(self.img_dir, self.data["images"]["enemy3"][2][self.anim_count // 20])).convert_alpha()
                self.anim_count_increment(1)
                self.rect.y = 450


class EnemyOnSky(pg.sprite.Sprite):
    def __init__(self, x, y, colors, bullets, enemies, all_sprites, data, img_dir, anim_count, screen, length,
                 ray_angle, rot_angle, width):
        super(EnemyOnSky, self).__init__()
        self.x = x
        self.y = y
        self.y = y
        self.colors = colors
        self.bullets = bullets
        self.enemies = enemies
        self.all_sprites = all_sprites
        self.data = data
        self.img_dir = img_dir
        self.anim_count = anim_count
        self.screen = screen
        self.length = length
        self.ray_angle = ray_angle
        self.rot_angle = rot_angle
        self.width = width
        self.image = pg.image.load(os.path.join(self.img_dir, self.data["images"]["enemy2"][1][0])).convert_alpha()
        self.rect = self.image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
        self.speed = random.randint(2, 5)
        self.isFly = True
        self.isDead = False
        self.isAttack = False

    def update(self):
        self.fly()
        self.animation()
        self.collision()

    def fly(self):
        if self.isFly and not self.isAttack:
            self.ray_angle -= self.rot_angle
            if self.ray_angle < -60 or self.ray_angle > 60:
                self.rot_angle = -self.rot_angle
            self.rect.x -= self.speed * math.cos(self.ray_angle * math.pi / 180)
            self.rect.y -= self.speed * math.sin(self.ray_angle * math.pi / 180)
        if self.isDead:
            self.rect.y += 10

    def anim_count_increment(self, n=1):
        self.anim_count += n
        self.anim_count %= 60

    def animation(self):
        if self.isFly:
            self.image = pg.image.load(
                os.path.join(self.img_dir, self.data["images"]["enemy2"][1][self.anim_count // 15]))
            self.anim_count_increment(2)
        if self.isDead:
            self.image = pg.image.load(os.path.join(self.img_dir, self.data["images"]["enemy2"][0]))

    def collision(self):
        collide1 = pg.sprite.spritecollide(self, self.bullets, False)
        collide2 = pg.sprite.spritecollide(self, self.all_sprites, False)
        if collide1:
            self.isDead = True
            list(map(lambda x: x.kill(), self.bullets))
        if self.rect.y > 500 or self.rect.x < 0:
            self.kill()
            enemy_on_sky = EnemyOnSky(x=5000, y=random.randint(200, 500), colors=self.colors, bullets=self.bullets,
                                      enemies=self.enemies,
                                      all_sprites=self.all_sprites, data=self.data, img_dir=self.img_dir, anim_count=0,
                                      screen=self.screen, length=200, ray_angle=self.ray_angle, rot_angle=3,
                                      width=self.width)
            self.enemies.add(enemy_on_sky)
        if collide2:
            self.isAttack = True


class Tower(pg.sprite.Sprite):  # class for tower
    def __init__(self, x, y, colors, tower_xp, enemies, data, img_dir):
        super(Tower, self).__init__()
        self.x = x
        self.y = y
        self.colors = colors
        self.tower_xp = tower_xp
        self.enemies = enemies
        self.data = data
        self.img_dir = img_dir
        self.image = pg.image.load(os.path.join(self.img_dir, self.data["images"]["tower"]))
        self.rect = self.image.get_rect(center=self.image.get_rect(topleft=(self.x, self.y)).center)
