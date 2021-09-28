from abc import abstractmethod
from re import M
from genetic_algorithms.helpers.camel_to_snake import camel_to_snake
from typing import Union
from genetic_algorithms.problems.base.model import Model
from genetic_algorithms.problems.base.state import State
from genetic_algorithms.models.next_state_provider import NextStateProvider
from dataclasses import dataclass
from enum import Enum
import operator as op


class OptimizationStrategy(Enum):
    Min = 'min',
    Max = 'max'


@dataclass
class AlgorithmConfig:
    max_steps_without_improvement: int = 10
    optimization_stategy: OptimizationStrategy = OptimizationStrategy.Min


DEFAULT_CONFIG = AlgorithmConfig()


class Algorithm(NextStateProvider):
    """
    Generates next states for the problem based on some logic.
    """
    _algorithms = {}

    def __init__(self, config: AlgorithmConfig = None):
        config = config or DEFAULT_CONFIG
        self.config = config
        self._steps_from_last_state_update = 0
        self._best_cost, self._best_state = float('inf'), None

    def __init_subclass__(cls) -> None:
        Algorithm._algorithms[camel_to_snake(cls.__name__)] = cls

    @abstractmethod
    def _find_next_state(self, model: Model, state: State) -> Union[State, None]:
        """
        Finds next state for model. Returns None in case if state is optimal.
        """

    def next_state(self, model: Model, state: State) -> Union[State, None]:
        next_state = self._find_next_state(model, state)
        if next_state:
            self._update_algorithm_state(model, next_state)
        return next_state

    def _is_cost_better(self, is_better_cost, is_better_than_cost):
        return {
            OptimizationStrategy.Min: op.le,
            OptimizationStrategy.Max: op.ge,
        }[self.config.optimization_stategy](is_better_cost, is_better_than_cost)

    def _update_algorithm_state(self, model: Model, problem_state: State):
        next_state_cost = model.cost_for(problem_state)
        if self._is_cost_better(next_state_cost, self._best_cost):
            self._best_cost, self._best_state = next_state_cost, self._best_state
            self._steps_from_last_state_update = 0
        else:
            self._steps_from_last_state_update += 1

    def _is_optimal_state(self, state_cost: int):
        return self._is_cost_better(state_cost, self._best_cost) and self._steps_from_last_state_update >= self.config.max_steps_without_improvement
