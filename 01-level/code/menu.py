import pygame
from settings import *

class Menu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.deactivation = True
        self.game_over_font = pygame.font.Font(UI_FONT, 150)
        self.continue_font = pygame.font.Font(UI_FONT, 20)
        self.logo = pygame.image.load('../graphics/logo/Wildventure.png').convert_alpha()
        # Define game settings
        self.game_settings = [
            ("W", "Move Up"),
            ("  A", "Move Left"),
            ("   D", "Move Right"),
            ("  S", "Move Down"),
            ("   SPACE", "Attack"),
            ("      Z", "Switch Weapon"),
            ("   M", "Cast Spell"),
            ("     N", "Switch Spell"),
            ("      Q", "Player Skills"),

            # Add more settings as needed
        ]


    def input(self, deactivate):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            deactivate = False
        return deactivate
    def display(self, game_over_menu):
        pygame.draw.rect(self.display_surface, 'black', self.display_surface.get_rect())


        if game_over_menu:
            # Render text surfaces
            game_over_text = self.game_over_font.render("GAME OVER", False, '#D2B48C')
            try_again_text = self.continue_font.render("Press button 'p' to try again", False,
                                                '#D2B48C')

            # Get text rectangles
            game_over_rect = game_over_text.get_rect(
                center=(WIDTH // 2, HEIGTH // 6))
            try_again_rect = try_again_text.get_rect(center=(
                WIDTH // 2, HEIGTH // 2))

            # Blit text surfaces onto display surface
            self.display_surface.blit(game_over_text, game_over_rect)
            self.display_surface.blit(try_again_text, try_again_rect)
        else:
            game_logo = pygame.transform.scale(self.logo, (800, 800))  # overwrite the initial surface
            game_logo_rect = game_logo.get_rect(center=(WIDTH // 2, HEIGTH // 4))
            start_text = self.continue_font.render("Press button 'p' to start", False, '#D2B48C')
            start_text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGTH - 300))
            game_settings_text = self.continue_font.render("GAME SETTINGS:", False, '#D2B48C')
            game_settings_rect = game_settings_text.get_rect(center=(WIDTH - 1160, HEIGTH - 350))

            self.display_surface.blit(game_logo, game_logo_rect)
            self.display_surface.blit(start_text, start_text_rect)
            self.display_surface.blit(game_settings_text, game_settings_rect)

            # Calculate maximum width of key and description strings
            max_key_width = max(len(key) for key, _ in self.game_settings) * 10
            max_desc_width = max(len(desc) for _, desc in self.game_settings) * 10

            # Render game settings
            settings_y = HEIGTH - 300
            for key, description in self.game_settings:
                settings_text = self.continue_font.render(f"{key} = {description}", False, '#D2B48C')
                settings_rect = settings_text.get_rect(center=(WIDTH - 1200 + max_key_width // 2, settings_y))
                self.display_surface.blit(settings_text, settings_rect)
                settings_y += 30  # Adjust vertical spacing between settings

        input = self.input(self.deactivation)
        return input

