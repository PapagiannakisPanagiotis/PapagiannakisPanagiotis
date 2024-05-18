import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))): # flexibility (many Sprites)
        super().__init__(groups) # initialize the inhereted class
        self.sprite_type = sprite_type
        y_offset = HITBOX_OFFSET[sprite_type]
        self.image = surface
        if sprite_type == 'object': # we wanna move those obj little up
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1] - TILESIZE)) # our tiles are twice larger(128px) than the other ones
        else:
            self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, y_offset) # changes the size of the rectangle