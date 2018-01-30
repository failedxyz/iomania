import getpass
import os

import pygame
import pygame.freetype
import yaml
from pygame import Color

from states import StateMachine
from states.main_menu import MainMenuState


class Game(object):
    def __init__(self):
        pygame.init()

        self.width, self.height = 1280, 720
        self.screen = pygame.display.set_mode((self.width, self.height))

        self.conf_file = self.resource("%s.cfg" % getpass.getuser())
        self.load_configuration()
        self.load_skin()

        self.font_file = self.resource("lato.ttf")
        self.debug_font = pygame.freetype.Font(self.font_file, 12)
        self._keys = {}

        self.machine = StateMachine()
        self.machine.push(MainMenuState(self))

        self.running = True

    def key(self, code, value=None):
        if not value:
            return self._keys.get(code, False)
        self._keys[code] = value

    def update(self):
        if self.machine.empty():
            self.quit()
            return
        current = self.machine.top()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if getattr(current, "keydown", None) and not self._keys.get(event.key):
                    current.keydown(event.key)
                self._keys[event.key] = True
            elif event.type == pygame.KEYUP:
                if getattr(current, "keyup", None) and self._keys.get(event.key):
                    current.keyup(event.key)
                self._keys[event.key] = False

        current.update()

    def render(self):
        if self.machine.empty():
            self.quit()
            return
        current = self.machine.top()
        current.render()

        label_current_state, rect = self.debug_font.render("current state: %s" % repr(current), Color(255, 255, 255))
        self.screen.blit(label_current_state, (10, 10))
        pygame.display.flip()

    def resource(self, file):
        return os.path.join("resources", file)

    def graphic(self, graphic):
        return self.resource(os.path.join("skins", self.options["skin"], graphic))

    def load_configuration(self):
        configuration = {
            "4K_1": pygame.K_d,
            "4K_2": pygame.K_f,
            "4K_3": pygame.K_j,
            "4K_4": pygame.K_k,
            "5K_1": pygame.K_d,
            "5K_2": pygame.K_f,
            "5K_3": pygame.K_SPACE,
            "5K_4": pygame.K_j,
            "5K_5": pygame.K_k,
            "skin": "o2jam"
        }
        if os.path.exists(self.conf_file):
            loaded_configuration = yaml.load(open(self.conf_file, "r"))
            for key in loaded_configuration:
                configuration[key] = loaded_configuration[key]
        self.options = configuration
        print self.options

    def load_skin(self):
        self.graphics = {}

        # TODO check skin folder exists
        folder = self.resource(os.path.join("skins", self.options["skin"]))
        files = sorted(os.listdir(folder))
        for filename in files:
            file = os.path.abspath(os.path.join(folder, filename))
            if os.path.isdir(file) or not file.endswith(".png"):
                continue
            graphicname = filename.replace(".png", "").replace("@2x", "")
            self.graphics[graphicname] = pygame.image.load(file)
        print sorted(self.graphics.keys())

    def quit(self):
        yaml.dump(self.options, open(self.conf_file, "w"), default_flow_style=False)
        self.running = False
