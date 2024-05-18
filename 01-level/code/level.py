import pygame
from settings import *
from tile import Tile
from player import Player
from debug import debug
from support import *
from random import choice, randint
from weapon import Weapon
from ui import UI
from enemy import Enemy
from particles import  AnimationPlayer
from magic import MagicPlayer
from upgrade import Upgrade
from upgrade import Item
from menu import Menu


class Level:
    def __init__(self):
        #get the display surface from anywhere in our code
        self.display_surface = pygame.display.get_surface()
        self.game_paused = False
        self.menu_pause = True
        self.spawn = True
        self.game_over_menu = False
        self.enemies_exist = False


        #sprite group setup
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        # attack sprites
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        #sprite setup
        self.create_map()

        # user interface
        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        self.menu = Menu()

        # particles
        self.animation_player = AnimationPlayer()
        self.magic_player = MagicPlayer(self.animation_player)

    def create_map(self):

        layouts = {
            'boundary': import_csv_layout('../map/map_FloorBlocks.csv'),
            'grass': import_csv_layout('../map/map_Grass.csv'),
            'object': import_csv_layout('../map/map_LargeObjects.csv'),
            'entities': import_csv_layout('../map/map_Entities.csv')
        }
        if self.spawn:
            graphics = {
                'grass': import_folder('../graphics/Grass'),
                'objects': import_folder('../graphics/objects')
            }
        for style, layout in layouts.items(): # style = boundary, layout = import_csv_layout
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites], 'invisible')
                        if self.spawn:
                            if style == 'grass':
                                random_grass_image = choice(graphics['grass'])
                                Tile((x,y),
                                     [self.visible_sprites,
                                      self.attackable_sprites],
                                     'grass', random_grass_image)
                            if style == 'object':
                                surf = graphics['objects'][int(col)]
                                Tile((x,y), [self.visible_sprites, self.obstacle_sprites],'object',surf) # every object has the right index
                            # create object tile
                        if style == 'entities':
                            if col == '394': # player index inside the list (tile map)
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic)
                            else:

                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name = 'raccoon'
                                else: monster_name = 'squid'
                                self.enemy = Enemy(monster_name, (x,y),
                                      [self.visible_sprites,
                                      self.attackable_sprites],
                                      self.obstacle_sprites,
                                      self.damage_player,
                                      self.trigger_death_particles,
                                      self.add_xp)



    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style,strength, cost):
        if style == 'heal':
            self.magic_player.heal( self.player, strength, cost, [self.visible_sprites])

        if style == 'flame':
            self.magic_player.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])



    def destroy_attack(self):
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprites in self.attack_sprites:
                # returns a list of all sprites that had been collided
                collision_sprites = pygame.sprite.spritecollide(attack_sprites, self.attackable_sprites, False) # destroy attackable sprites = False (we dont want enemy destruction)
                if collision_sprites:
                    # we want the sprites that has been colliding with our weapon
                    for target_sprite in collision_sprites:
                        if target_sprite.sprite_type == 'grass':
                            pos = target_sprite.rect.center
                            offset = pygame.math.Vector2(0,75) # just to look fancier
                            for leaf in range(randint(3,6)):
                                self.animation_player.create_grass_particles(pos - offset, [self.visible_sprites])
                            target_sprite.kill()
                        else:
                            target_sprite.get_damage(self.player, attack_sprites.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.health <= 0:
            if self.current_attack:
                self.current_attack.kill()
            self.game_over_menu = True
            restart = self.menu.display(self.game_over_menu)
            self.menu_pause = restart
            self.spawn = False
            self.upgrade.display()
            for enemy in self.attackable_sprites:
                if isinstance(enemy, Enemy):
                    enemy.kill()
            self.player.kill()
            for index in range(len(self.player.stats)):
                attribute = self.upgrade.attribute_names[index]
                self.player.stats[attribute] = self.player.initial_stats[attribute]
                self.player.upgrade_cost[attribute] = self.player.initial_upgrade_cost[attribute]

            self.create_map()
            self.player.stats['health'] = self.player.initial_stats['health']
            self.player.stats['energy'] = self.player.initial_stats['energy']
            self.player.stats['speed'] = self.player.initial_stats['speed']
            self.player.health = self.player.stats['health']
            self.player.energy = self.player.stats['energy']
            self.player.speed = self.player.stats['speed']
            self.player.exp = 0
        else:
            if self.player.vulnerable:
                self.player.health -= amount
                self.player.vulnerable = False
                self.player.hurt_time = pygame.time.get_ticks()
                self.animation_player.create_particles(attack_type, self.player.rect.center, [self.visible_sprites])



    def trigger_death_particles(self, pos, particle_type):
        self.animation_player.create_particles(particle_type, pos, [self.visible_sprites])

    def add_xp(self, amount):
        self.player.exp += amount

    def toggle_menu(self):

        self.game_paused = not self.game_paused




    def run(self):
        if self.menu_pause:
            activation = self.menu.display(self.game_over_menu)
            self.menu_pause = activation
        else:
            self.visible_sprites.custom_draw(self.player)
            self.ui.display(self.player)
            if self.game_paused:
                self.upgrade.display()
            else:
                # run the game
                self.visible_sprites.update()
                self.visible_sprites.enemy_update(self.player)
                self.player_attack_logic()







class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        # general setup
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2 # get_size returns (x,y)
        self.offset = pygame.math.Vector2()
        # creating the floor
        self.floor_surf = pygame.image.load("../graphics/tilemap/ground.png").convert_alpha()
        self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))
    def custom_draw(self, player): # camera
        # getting the offset
        self.offset.x = player.rect.centerx - self.half_width # It calculates the offset by finding the difference
        self.offset.y = player.rect.centery - self.half_height # between the player's center coordinates and half the width and height of the display surface.

        floor_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surf, floor_pos)

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery): # sorting them based on their y-coordinate position relative to the player.
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)


    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
