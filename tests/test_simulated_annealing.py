import pytest

from local_search.algorithms.simulated_annealing import SimulatedAnnealing
from test_utils import create_object_copy_with_student_method
from tests.mock import MockState

PROBLEM_SIZE = 100


@pytest.fixture
def student_solver(student_loader, method_name: str) -> SimulatedAnnealing:
    teacher_solver = SimulatedAnnealing()
    return create_object_copy_with_student_method(teacher_solver,
                                                  student_loader,
                                                  "local_search/algorithms/simulated_annealing.py",
                                                  method_name)


@pytest.mark.parametrize('method_name', [SimulatedAnnealing._reheat.__name__])
def test_reheat_should_restore_temp_and_reset_schedule(student_solver):
    student_solver.temperature = 0
    student_solver.steps_from_last_state_update = 100
    student_solver.cooling_time = 100
    state = MockState.suboptimal_state()
    new_state = student_solver._reheat(state)
    assert state == new_state, "reheating modifies the state, it shouldn't!"
    print(student_solver.config)
    expected_temp = student_solver.config.escape_reheat_ratio * \
        student_solver.config.initial_temperature
    assert student_solver.temperature == expected_temp, f"reheating should change temperature according to " \
                                                        f"self.config, got {student_solver.temperature}, " \
                                                        f"expected {expected_temp}"
    assert student_solver.steps_from_last_state_update == 0, "reheating should reset the " \
                                                             "'steps_from_last_state_update' "
    assert student_solver.cooling_time == 0, "reheating should reset the 'cooling_time'"


@pytest.mark.parametrize('method_name', [SimulatedAnnealing._update_temperature.__name__])
def test_update_temperature(student_solver):
    assert False


@pytest.mark.parametrize('method_name', [SimulatedAnnealing._calculate_transition_probability.__name__])
def test_calculate_transition_probability(student_solver):
    assert False


@pytest.mark.parametrize('method_name', [SimulatedAnnealing._find_next_state.__name__])
def test_find_next_state(student_solver):
    assert False
