import pygame

import states


class OptionsState(states.State):
    def update(self):
        pass

    def render(self):
        pygame.draw.rect(self.game.screen, (0, 124, 248), (0, 0, self.game.width, self.game.height))
