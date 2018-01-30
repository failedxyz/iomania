import pygame

import states
from options import OptionsState
from song_select import SongSelectState


class MainMenuState(states.State):
    def __init__(self, game):
        super(MainMenuState, self).__init__(game)

        self.title_font = pygame.freetype.Font(self.game.font_file, 36)
        self.font = pygame.freetype.Font(self.game.font_file, 24)

        self.options = [
            ("play", self.play_handler),
            ("options", self.options_handler),
            ("quit", self.quit_handler)
        ]
        self.current_option = 0

    def keydown(self, key):
        super(MainMenuState, self).keydown(key)

        if key == pygame.K_DOWN and self.current_option < len(self.options) - 1:
            self.current_option += 1
        elif key == pygame.K_UP and self.current_option > 0:
            self.current_option -= 1

        if key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
            text, handler = self.options[self.current_option]
            handler()

    def update(self):
        pass

    def render(self):
        pygame.draw.rect(self.game.screen, (0, 102, 204), (0, 0, self.game.width, self.game.height))

        label_title, rect = self.title_font.render("welcome to iomania", fgcolor=(255, 255, 255))
        self.game.screen.blit(label_title, (50, 100))

        for i, option in enumerate(self.options):
            text, handler = option
            label_option, rect = self.font.render(text, fgcolor=(255, 255, 255) if i == self.current_option else (183, 183, 183))
            self.game.screen.blit(label_option, (90, 180 + 40 * i))

        label_arrow, rect = self.font.render(">", fgcolor=(255, 255, 255))
        self.game.screen.blit(label_arrow, (60, 180 + 40 * self.current_option))

    def play_handler(self):
        self.game.machine.push(SongSelectState(self.game))

    def options_handler(self):
        self.game.machine.push(OptionsState(self.game))

    def quit_handler(self):
        self.game.quit()
