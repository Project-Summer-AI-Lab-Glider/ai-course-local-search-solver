from typing import Tuple
from genetic_algorithms.algorithm_wrappers.visualizations.visualization_wrapper import VisualizationSubscriber
from genetic_algorithms.problems.graph_coloring_problem.problem_model import GraphColoringProblem
from genetic_algorithms.problems.graph_coloring_problem.state import GraphColoringState
from random import randint
from math import sqrt
import pygame

EDGE_COLOR = (0, 0, 0)


class GraphColoringVisualization(VisualizationSubscriber):

    def __init__(self,model: GraphColoringProblem, **kwargs):
        super().__init__(**kwargs)
        self._available_colors = None
        self.coords = self._generate_coords(model)

    @staticmethod
    def get_corresponding_problem():
        return GraphColoringProblem

    def _draw_state(self, screen, model: GraphColoringProblem, state: GraphColoringState):
        """
        Draws state
        """
        self._draw_lines(screen, model)
        self._draw_vertices(screen, model, state)

    def _draw_lines(self, screen, model: GraphColoringProblem):
        graph = [list(model.graph[i]) for i in range(model.n_vertices)]
        extremes = self._find_extremes()

        for i in range(len(graph)):
            for j in range(len(graph[i])):
                pygame.draw.line(screen, EDGE_COLOR,
                                 self._scale(self.coords[i], screen, extremes),
                                 self._scale(
                                     self.coords[graph[i][j]], screen, extremes),
                                 3)

    def _find_extremes(self):
        min_x = min(vertex[0] for vertex in self.coords)
        max_x = max(vertex[0] for vertex in self.coords)
        min_y = min(vertex[1] for vertex in self.coords)
        max_y = max(vertex[1] for vertex in self.coords)
        return min_x, max_x, min_y, max_y

    def _draw_vertices(self, screen, model: GraphColoringProblem, state: GraphColoringState):
        extremes = self._find_extremes()
        colors = self._get_colors(model)
        for i in range(len(self.coords)):
            x, y = self._scale(self.coords[i], screen, extremes)
            pygame.draw.circle(
                screen, colors[state.coloring[i].color], (x, y), 10)
            pygame.draw.circle(screen, (0, 0, 0), (x, y), 10, 2)

    def _generate_coords(self, model: GraphColoringProblem):
        coord = []
        x, y = 1, 1
        for _ in range(model.n_vertices):
            while (x, y) in coord:
                x, y = randint(0, model.n_vertices), randint(
                    0, model.n_vertices)
            coord.append((x, y))

        return coord

    def _get_colors(self, model: GraphColoringProblem):
        if not self._available_colors:
            self._available_colors = self._generate_random_colors(
                model.n_vertices)
        return self._available_colors

    def euclidean_distance(self,v1,v2):
        d = 0

        for i in range(len(v1)):
            d += (v1[i] - v2[i])**2

        return sqrt(d)

    def check_similar(self,new_color,colors):
        for color in colors:
            self.euclidean_distance(new_color, color)
            if self.euclidean_distance(new_color, color) < 20:
                return False
        return True

    def _generate_random_colors(self, n, except_colors=None):
        colors = []

        def random_color():
            new_color = (randint(0, 255), randint(0, 255), randint(0, 255))

            while not self.check_similar(new_color,colors):
                new_color = (randint(0, 255), randint(0, 255), randint(0, 255))

            return new_color

        color = random_color()
        except_colors = except_colors or []
        for _ in range(n):
            while color in colors or color in except_colors:
                color = random_color()
            colors.append(color)
        return colors

    def _scale(self, point: Tuple[int, int], screen, extremes: Tuple[int, int, int, int]):
        min_x, max_x, min_y, max_y = extremes
        x, y = point
        x -= min_x
        y -= min_y
        x = x * (screen.get_width() / max((max_x - min_x), 1))
        y = y * (screen.get_height() / max((max_y - min_y), 1))
        if x == 0:
            x += 40
        if y == 0:
            y += 40
        if x == screen.get_width():
            x -= 40
        if y == screen.get_height():
            y -= 40
        return x, y