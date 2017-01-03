import pygame

import states


class GameState(states.State):
    def __init__(self, game, beatmap):
        super(GameState, self).__init__(game)
        self.beatmap = beatmap

    def update(self):
        pass

    def render(self):
        pygame.draw.rect(self.game.screen, (0, 0, 0), (0, 0, self.game.width, self.game.height))
