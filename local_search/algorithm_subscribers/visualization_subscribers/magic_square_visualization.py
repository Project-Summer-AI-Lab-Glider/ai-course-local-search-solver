from local_search.algorithm_subscribers.visualization_subscribers.visualization_subscriber import StateDrawer, VisualizationSubcriberConfig, VisualizationSubscriber
from local_search.problems.magic_square.problem_model import MagicSquareProblem
from local_search.problems.magic_square.state import MagicSquareState

import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class MagicSquareVisualization(VisualizationSubscriber):

    @staticmethod
    def get_corresponding_problem():
        return MagicSquareProblem

    @classmethod
    def create_state_drawer(cls, model: MagicSquareProblem = None):
        if model is None:
            return None
        return MagicSquareStateDrawer(model)


class MagicSquareStateDrawer(StateDrawer):
    def __init__(self, model: MagicSquareProblem):
        self._available_colors = None
        self.coords = self._generate_coords(model)

    def draw_state(self, screen, model: MagicSquareProblem, state: MagicSquareState):
        """
        Draws state
        """
        screen.fill(WHITE)
        self._draw_lines(screen, state)
        self._draw_numbers(screen, model, state)

    @staticmethod
    def _draw_lines(self, screen, state: MagicSquareState):
        size = len(state.numbers)
        for i in range(size-1):
            pygame.draw.line(screen, BLACK, (0, (i+1) * screen.get_height / size), (screen.get_width(), (i+1) * screen.get_height / size))
            pygame.draw.line(screen, BLACK, ((i+1) * screen.get_width() / size, 0), ((i+1) * screen.get_width() / size, screen.get_height))

    def _draw_numbers(self, screen, model: MagicSquareProblem, state: MagicSquareState):
        """ TODO - We've got lines and how to put numbers in tiles"""
        pass


