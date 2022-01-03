
from typing import Tuple

import pygame

from settings import TILE_SIZE
from utils import load_images


class Player(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int, int]):

        pygame.sprite.Sprite.__init__(self)
        self.import_character_assets()
        self.image_frame_index = 0
        self.direction = 'move_down'
        # 'image' is the current image of the animation.
        self.image = self.animations[self.direction][self.image_frame_index]

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect(center=position)
        self.velocity = pygame.math.Vector2(0, 0)

        self.move_step = 3
        self.animation_speed = 0.10
        self.is_animating = False

    def import_character_assets(self):
        character_path = 'assets/player/'
        self.animations = {'move_right': [], 'move_left': [], 'move_up': [], 'move_down': []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = load_images(full_path)

    def animate(self):
        animation = self.animations[self.direction]

        self.image_frame_index += self.animation_speed
        if self.image_frame_index >= len(animation):
            self.image_frame_index = 0

        self.image = animation[int(self.image_frame_index)]

    def get_input(self):
        keys = pygame.key.get_pressed()

        self.is_animating = True
        if keys[pygame.K_RIGHT]:
            self.velocity.x = self.move_step
            self.direction = 'move_left'
        elif keys[pygame.K_LEFT]:
            self.velocity.x = -self.move_step
            self.direction = 'move_right'
        elif keys[pygame.K_DOWN]:
            self.velocity.y = self.move_step
            self.direction = 'move_down'
        elif keys[pygame.K_UP]:
            self.velocity.y = -self.move_step
            self.direction = 'move_up'
        else:
            self.velocity.y = 0
            self.velocity.x = 0
            self.is_animating = False

    def update(self):
        self.get_input()
        if self.is_animating:
            self.animate()


class Box(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)

        full_image = pygame.image.load('assets/crates/crate_07.png').convert_alpha()
        self.image = pygame.transform.scale(full_image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(center=position)
        self.velocity = pygame.math.Vector2(0, 0)


class BoxPlace(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)

        full_image = pygame.image.load('assets/environment/environment_10.png').convert_alpha()
        self.image = pygame.transform.scale(full_image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(center=position)


class Wall(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)

        full_image = pygame.image.load('assets/crates/crate_11.png').convert_alpha()
        self.image = pygame.transform.scale(full_image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(center=position)


class Floor(pygame.sprite.Sprite):
    def __init__(self, position: Tuple[int, int]):
        pygame.sprite.Sprite.__init__(self)

        full_image = pygame.image.load('assets/ground/ground_04.png').convert_alpha()
        self.image = pygame.transform.scale(full_image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(center=position)
