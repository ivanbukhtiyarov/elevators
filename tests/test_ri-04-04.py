import pytest
from src.elevator import (
    Elevator, MoveRequest,
    DIRECTION_DOWN, DIRECTION_UP,
    REQUEST_DOWN, REQUEST_UP
)


def test_queue_lifecycle():
    elevator = Elevator(
        tonnage=1000,
        floors_count=25,
        current_direction=DIRECTION_DOWN,
        current_weight=0,
        current_floor=17,
    )

    elevator.open_doors()
    assert elevator.is_doors_open == True

    elevator.close_doors()
    assert elevator.is_doors_open == False

    elevator.turn_light_on()
    assert elevator.is_light_on == True

    elevator.turn_light_off()
    assert elevator.is_light_on == False

    elevator.turn_smoke_on()
    assert elevator.is_smoked == True

    elevator.turn_smoke_off()
    assert elevator.is_smoked == False