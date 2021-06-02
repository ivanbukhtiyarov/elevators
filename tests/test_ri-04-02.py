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

    request_5_down = MoveRequest(5, DIRECTION_DOWN)
    request_14_up = MoveRequest(14, REQUEST_UP)
    request_9_down = MoveRequest(9, REQUEST_DOWN)
    request_7_down = MoveRequest(7, REQUEST_DOWN)
    request_7_up = MoveRequest(7, REQUEST_UP)
    request_2_up = MoveRequest(2, REQUEST_UP)

    elevator.add_request(request_5_down)
    assert elevator.requests == [request_5_down]

    elevator.add_request(request_14_up)
    assert elevator.requests == [request_5_down, request_14_up]

    elevator.add_request(request_9_down)
    assert elevator.requests == [request_5_down, request_14_up, request_9_down]

    elevator.add_request(request_7_up)
    assert elevator.requests == [
        request_5_down, request_14_up,
        request_9_down, request_7_up
    ]

    elevator.add_request(request_7_down)
    assert elevator.requests == [
        request_5_down, request_14_up,
        request_9_down, request_7_up,
        request_7_down
    ]

    elevator.add_request(request_2_up)
    assert elevator.requests == [
        request_5_down, request_14_up,
        request_9_down, request_7_up,
        request_7_down, request_2_up
    ]

