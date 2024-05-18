import pygame
from math import sin

class Entity(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()

    def move(self, speed):  # 1. we check if our vector has any length
        if self.direction.magnitude() != 0:  # magnitude = length of the vector
            self.direction = self.direction.normalize()  # 2. Then we are setting the length to 1
        self.hitbox.x += self.direction.x * speed
        self.check_collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.check_collision('vertical')
        self.rect.center = self.hitbox.center


    def check_collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):  # object-player collide
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left  # bounce back to the other side
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):  # object-player collide
                    if self.direction.y > 0:  # moving right
                        self.hitbox.bottom = sprite.hitbox.top  # bounce back to the other side
                    if self.direction.y < 0:  # moving left
                        self.hitbox.top = sprite.hitbox.bottom


    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0
