from typing import List

import pytest

from local_search.algorithms.hill_climbing.best_choice_hill_climbing import BestChoiceHillClimbing
from local_search.algorithms.hill_climbing.random_choice_hill_climbing import RandomChoiceHillClimbing
from local_search.algorithms.hill_climbing.worst_choice_hill_climbing import WorstChoiceHillClimbing
from local_search.algorithms.hill_climbing.hill_climbing import HillClimbing, DEFAULT_CONFIG
from test_utils import RelativePathLoader
from tests.mock import MockProblem, MockGoal, MockGoalMax, MockGoalMin, MockState

PROBLEM_SIZE = 100


def test_best_choice_hill_climbing_should_find_the_best_neighbor(student_loader: RelativePathLoader, mock_goals):
    student_solver_module = student_loader.load("local_search/algorithms/hill_climbing/best_choice_hill_climbing.py")
    student_solver: BestChoiceHillClimbing = student_solver_module.BestChoiceHillClimbing(DEFAULT_CONFIG)
    teacher_solver = BestChoiceHillClimbing()

    for goal in mock_goals:
        state = MockState.suboptimal_state(PROBLEM_SIZE)
        got_state, problem = get_climbing_results_for_a_mock_problem(student_solver, goal, state)
        assert problem.improvement(got_state,
                                   state) > 0, "algorithm returns a state that's not better than the previous " \
                                               f"one (goal type: {goal.type()})"

        exp_state = teacher_solver._climb_the_hill(problem, state)
        assert problem.objective_for(got_state) == problem.objective_for(
            exp_state), "algorithm does return an improving state, but it's not the best " \
                        f"(goal type: {goal.type()})"


def test_worst_choice_hill_climbing_should_find_the_worst_improving_neighbor(student_loader: RelativePathLoader, mock_goals):
    student_solver_module = student_loader.load("local_search/algorithms/hill_climbing/worst_choice_hill_climbing.py")
    student_solver: WorstChoiceHillClimbing = student_solver_module.WorstChoiceHillClimbing(DEFAULT_CONFIG)
    teacher_solver = WorstChoiceHillClimbing()

    for goal in mock_goals:
        state = MockState.suboptimal_state(PROBLEM_SIZE)
        got_state, problem = get_climbing_results_for_a_mock_problem(student_solver, goal, state)
        assert problem.improvement(got_state,
                                   state) > 0, "algorithm returns a state that's not better than the previous " \
                                               f"one (goal type: {goal.type()})"

        exp_state = teacher_solver._climb_the_hill(problem, state)
        assert problem.objective_for(got_state) == problem.objective_for(
            exp_state), "algorithm returns an improving state, but it's not the wors " \
                        f"(goal type: {goal.type()})"


def test_random_choice_hill_climbing_should_find_the_random_improving_neighbor(student_loader: RelativePathLoader, mock_goals, random):
    student_solver_module = student_loader.load("local_search/algorithms/hill_climbing/random_choice_hill_climbing.py")
    student_solver: RandomChoiceHillClimbing = student_solver_module.RandomChoiceHillClimbing(DEFAULT_CONFIG)
    for goal in mock_goals:
        state = MockState.suboptimal_state(PROBLEM_SIZE)

        got_state, problem = get_climbing_results_for_a_mock_problem(student_solver, goal, state)
        assert problem.improvement(got_state, state) >= 0, f"algorithm returns a state that's worse than " \
                                                                      f"the previous " \
                                                                       "one (goal type: {goal.type()})"

        got_values = set([problem.objective_for(student_solver._climb_the_hill(problem, state)) for _ in range(100)])
        assert len(
            got_values) > 1, f"algorithm is deterministic, always returns the same state, while it should be random " \
                             f"(goal type: {goal.type()})) "


def get_climbing_results_for_a_mock_problem(student_solver: HillClimbing, goal: MockGoal, state: MockState):
    problem = MockProblem(PROBLEM_SIZE, goal)
    got_state = student_solver._climb_the_hill(problem, state)
    assert got_state is not None, "algorithm returns None instead of a state"
    return got_state, problem


@pytest.fixture
def mock_goals() -> List[MockGoal]:
    return [MockGoalMin(), MockGoalMax()]