import pygame

import states

LAYOUT = {
    4: ["1", "2", "2", "1"],
    5: ["1", "2", "S", "2", "1"],
    6: ["1", "2", "1", "1", "2", "1"],
    7: ["1", "2", "1", "S", "1", "2", "1"]
}


class GameState(states.State):
    def __init__(self, game, beatmap):
        super(GameState, self).__init__(game)
        self.beatmap = beatmap

    def update(self):
        pass

    def render(self):
        pygame.draw.rect(self.game.screen, (0, 0, 0), (0, 0, self.game.width, self.game.height))

        x = 0
        _x, _y, _w, _h = self.game.graphics["mania-stage-left"].get_rect()
        scale = 1.0 * self.game.height / _h
        w = int(_w * scale)
        self.game.screen.blit(pygame.transform.scale(self.game.graphics["mania-stage-left"], (w, self.game.height)),
                              (x, 0))
        x += w

        # ============
        # draw columns
        for column in range(self.beatmap.columns):
            key = LAYOUT[self.beatmap.columns][column]
            keyboard = "%sK_%s" % (self.beatmap.columns, column + 1)
            pressed = self.game._keys.get(self.game.options.get(keyboard))
            if pressed:
                print "%s pressed!" % (column + 1)
            print self.game._keys, keyboard, self.game.options.get(keyboard)
            _x, _y, _w, _h = self.game.graphics["mania-key%s%s" % (key, "D" if pressed else "")].get_rect()
            w, h = int(_w * scale), int(_h * scale)
            y = self.game.height - h
            self.game.screen.blit(
                pygame.transform.scale(self.game.graphics["mania-key%s%s" % (key, "D" if pressed else "")], (w, h)),
                (x, y))
            _x, _y, _w, _h = self.game.graphics["mania-stage-hint"].get_rect()
            h = int(_h * scale)
            y -= h
            self.game.screen.blit(pygame.transform.scale(self.game.graphics["mania-stage-hint"], (w, h)), (x, y))
            if pressed:
                _x, _y, _w, _h = self.game.graphics["mania-stage-light"].get_rect()
                h = int(_h * scale)
                y -= h
                self.game.screen.blit(pygame.transform.scale(self.game.graphics["mania-stage-light"], (w, h)), (x, y))
            x += w

        _x, _y, _w, _h = self.game.graphics["mania-stage-right"].get_rect()
        w = int(_w * scale)
        self.game.screen.blit(pygame.transform.scale(self.game.graphics["mania-stage-right"], (w, self.game.height)),
                              (x, 0))
