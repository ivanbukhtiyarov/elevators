import pytest
from src.elevator import (
    Elevator, MoveRequest,
)
from src.operator import Operator


def test_simple():
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

    assert operator.open_doors(1) == 'Wrong elevator number'
