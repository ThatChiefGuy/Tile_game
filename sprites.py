import pygame
import snipets
import math
import random


class SpriteSheet:
    def __init__(self, sheet):
        self.sheet = pygame.image.load(sheet).convert_alpha()

    def get_sprite(self, frame, row, width, height, scale, color):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), (row * height), width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image


class Player(pygame.sprite.Sprite):
    def __init__(self, size, player_group, x, y, game):
        super().__init__()
        self.game = game
        self.size = size

        self.image = self.game.player_sheet.get_sprite(0, 0, 33, 36, self.size, (0, 0, 0))
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.rect.width = snipets.tile_size_x
        self.rect.height = snipets.tile_size_y

        self.x_change = 0
        self.y_change = 0
        self.facing = 0

        self.animation_index = 0
        self.animation_speed = 0.1

        player_group.add(self)

    def update(self):
        self.movement()
        self.collide_coins()
        self.collide_room()

        self.rect.x += self.x_change
        self.collide_blocks("x")
        self.rect.y += self.y_change
        self.collide_blocks("y")

        self.x_change = 0
        self.y_change = 0
        self.image = self.game.player_sheet.get_sprite(math.floor(self.animation_index),
                                                       self.facing, 33, 36, self.size, (0, 0, 0))

    def movement(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[ord("a")]:
            self.x_change -= snipets.player_speed
            self.facing = 3
            self.animation_index += self.animation_speed

        if keys_pressed[ord("d")]:
            self.x_change += snipets.player_speed
            self.facing = 1
            self.animation_index += self.animation_speed

        if keys_pressed[ord("w")]:
            self.y_change -= snipets.player_speed
            self.facing = 0
            self.animation_index += self.animation_speed

        if keys_pressed[ord("s")]:
            self.y_change += snipets.player_speed
            self.facing = 2
            self.animation_index += self.animation_speed

        if self.y_change == 0 and self.x_change == 0:
            self.animation_index = 1

        if self.animation_index >= 3:
            self.animation_index = 0

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.rock_group, False)
            if hits:
                if self.x_change > 0:
                    self.rect.right = hits[0].rect.left
                if self.x_change < 0:
                    self.rect.left = hits[0].rect.right

        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.rock_group, False)
            if hits:
                if self.y_change > 0:
                    self.rect.bottom = hits[0].rect.top
                if self.y_change < 0:
                    self.rect.top = hits[0].rect.bottom

    def collide_coins(self):
        if pygame.sprite.spritecollide(self, self.game.coin_group, True):
            self.game.score += snipets.score_per_coin

    def collide_room(self):
        if self.game.room == snipets.room1:
            if self.rect.top < 0:
                self.game.room = snipets.room2
                self.game.kill_all()
                self.game.create_map()
                self.rect.bottom = self.game.screen_y

        if self.game.room == snipets.room2:
            if self.rect.bottom > self.game.screen_y:
                self.game.room = snipets.room1
                self.game.kill_all()
                self.game.create_map()
                self.rect.top = 0


class Rock(pygame.sprite.Sprite):
    def __init__(self, size, rock_group, x, y):
        super().__init__()
        self.image = pygame.image.load("wall_block_tall.png")
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()

        self.rect.x = x * snipets.tile_size_x
        self.rect.y = y * snipets.tile_size_y
        self.rect.width = snipets.tile_size_x
        self.rect.height = snipets.tile_size_y

        rock_group.add(self)


class Coin(pygame.sprite.Sprite):
    def __init__(self, game, x, y, coin_group, size):
        super().__init__()
        self.game = game

        self.size = size
        self.image = self.game.coin_sheet.get_sprite(0, 0, 32, 30, self.size, (0, 0, 0))
        self.rect = self.image.get_rect()

        self.rect.x = x * snipets.tile_size_x
        self.rect.y = y * snipets.tile_size_y

        self.animation_index = 0
        self.animation_speed = 0.2
        self.images_in_sheet = 6

        coin_group.add(self)

    def update(self):
        self.animation_loop()

    def animation_loop(self):
        self.animation_index += self.animation_speed
        if self.animation_index >= self.images_in_sheet:
            self.animation_index = 0
        self.image = self.game.coin_sheet.get_sprite(math.floor(self.animation_index), 0, 32, 30, self.size, (0, 0, 0))


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y, enemy_group, size):
        super().__init__()
        self.game = game

        self.size = size
        self.image = self.game.enemy_sheet.get_sprite(0, 1, 60, 64, self.size, (0, 0, 0))
        self.rect = self.image.get_rect()

        self.rect.x = x * snipets.tile_size_x
        self.rect.y = y * snipets.tile_size_y

        self.animation_index = 0
        self.animation_row = 0
        self.animation_speed = 0.08

        self.movement_speed = snipets.enemy_speed
        self.facing = random.choice(["left", "right"])
        self.steps = random.randint(50, 100)
        self.movement_loop = 0
        self.x_change = 0
        self.y_change = 0

        enemy_group.add(self)

    def update(self):
        self.animation_loop()
        self.movement()
        self.rect.x += self.x_change
        self.rect.y += self.y_change
        self.image = self.game.enemy_sheet.get_sprite(math.floor(self.animation_index), self.animation_row, 60, 64,
                                                      self.size, (0, 0, 0))
        self.x_change = 0
        self.y_change = 0

    def movement(self):
        if self.facing == "left":
            self.animation_row = 1
            self.x_change -= self.movement_speed
            self.movement_loop -= 1
            if self.movement_loop <= -self.steps:
                self.facing = "right"

        if self.facing == "right":
            self.animation_row = 2
            self.x_change += self.movement_speed
            self.movement_loop += 1
            if self.movement_loop >= self.steps:
                self.facing = "left"

        hits = pygame.sprite.spritecollide(self, self.game.rock_group, False)

        if hits:
            if self.facing == "left":
                self.x_change += 2
                self.facing = "right"
            else:
                self.x_change -= 2
                self.facing = "left"

    def animation_loop(self):
        self.animation_index += self.animation_speed

        if self.animation_index >= 4:
            self.animation_index = 0
