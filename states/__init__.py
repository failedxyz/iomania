import pygame


class StateMachine(object):
    def __init__(self):
        self._stack = []

    def empty(self):
        return len(self._stack) == 0

    def top(self):
        if self.empty():
            raise ValueError("State stack is empty.")
        return self._stack[-1]

    def push(self, state):
        if not isinstance(state, State):
            raise ValueError("state must be a State.")
        self._stack.append(state)

    def pop(self):
        self._stack.pop()


class State(object):
    def __init__(self, game):
        self.game = game

    def keydown(self, key):
        if key == pygame.K_ESCAPE:
            self.game.machine.pop()

    def keyup(self, key):
        pass

    def update(self):
        raise NotImplementedError("%s.update has not been implemented." % self.__class__.__name__)

    def render(self):
        raise NotImplementedError("%s.render has not been implemented." % self.__class__.__name__)

    def __repr__(self):
        return self.__class__.__name__
