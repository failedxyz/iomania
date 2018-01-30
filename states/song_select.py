import os

import pygame

import states
from beatmap.beatmapset import BeatmapSet
from game import GameState


class SongSelectState(states.State):
    def __init__(self, game):
        super(SongSelectState, self).__init__(game)
        self.title_font = pygame.freetype.Font(self.game.font_file, 36)
        self.font = pygame.freetype.Font(self.game.font_file, 24)

        self.load_beatmaps()
        self.index = 0

    def keydown(self, key):
        super(SongSelectState, self).keydown(key)

        if key == pygame.K_DOWN and self.index < len(self.beatmaps) - 1:
            self.index += 1
        elif key == pygame.K_UP and self.index > 0:
            self.index -= 1

        if key == pygame.K_RETURN or key == pygame.K_KP_ENTER:
            beatmap = self.beatmaps[self.index]
            self.game.machine.push(GameState(self.game, beatmap))

    def update(self):
        pass

    def render(self):
        pygame.draw.rect(self.game.screen, (0, 72, 144), (0, 0, self.game.width, self.game.height))
        ind_start = max(0, min(self.index - 2, len(self.beatmaps) - 5))
        ind_end = min(ind_start + 5, len(self.beatmaps))

        label_title, rect = self.title_font.render("song select", fgcolor=(255, 255, 255))
        self.game.screen.blit(label_title, (50, 100))

        for i, beatmap in enumerate(self.beatmaps[ind_start:ind_end]):
            label_option, rect = self.font.render(beatmap.__repr__(), fgcolor=(255, 255, 255) if i == (self.index - ind_start) else (183, 183, 183))
            self.game.screen.blit(label_option, (90, 180 + 40 * i))

    def load_beatmaps(self):
        song_folders = os.listdir(self.game.resource("songs"))
        self.beatmaps = []

        for song_folder in song_folders:
            beatmapset = BeatmapSet.load(os.path.abspath(os.path.join(self.game.resource("songs"), song_folder)))
            for beatmap in beatmapset.beatmaps:
                self.beatmaps.append(beatmap)
