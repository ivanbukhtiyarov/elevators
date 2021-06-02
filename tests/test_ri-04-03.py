import pytest
from src.elevator import (
    Elevator, MoveRequest,
)
from src.operator import Operator


def test_simple():
    '''Tests calls of default elevators methods from operator'''
    elevator = Elevator(
        tonnage=1000,
        floors_count=25,
        current_direction=0,
        current_weight=0,
        current_floor=17,
        is_light_on=True,
        is_smoked=True,
        requests=[],
        is_communication_on=False,
        is_doors_open=False,
        is_doors_blocked=False,
        is_empty=True
    )
    operator = Operator([elevator])
    operator.open_doors(0)
    assert operator.elevators_list[0].is_doors_open == True

    operator.close_doors(0)
    assert operator.elevators_list[0].is_doors_open == False

    with pytest.raises(Exception) as e_info:
        assert operator.open_doors(1)

    operator.call_dispatcher(0)
    assert operator.elevators_list[0].is_communication_on == True

    operator.move_to_floor(20, 0)
    assert operator.elevators_list[0].current_floor == 20

    operator.turn_light_off(0)
    assert operator.elevators_list[0].is_light_on == False

    operator.turn_smoke_on(0)
    assert operator.elevators_list[0].is_smoked == True
