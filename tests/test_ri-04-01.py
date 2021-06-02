from copy import deepcopy
from random import randint

import pytest

from src.command_processor import Command, CommandProcessor, Source, Action
from src.elevator import Elevator, MoveRequest
from src.operator import Operator

# Pls don't change it
elevators_count = 3


@pytest.fixture()
def elevators() -> list[Elevator]:
    elevator = Elevator(
        tonnage=1000,
        floors_count=25,
        current_direction=0,
        current_weight=0,
        current_floor=0,
        is_light_on=True,
        is_smoked=True,
        requests=[],
        is_communication_on=False,
        is_doors_open=False,
        is_doors_blocked=False,
        is_empty=True
    )
    return [deepcopy(elevator) for i in range(elevators_count)]


@pytest.fixture()
def processor(elevators) -> CommandProcessor:
    return CommandProcessor(Operator(elevators))


def test_sensors_get_readings(elevators, processor):
    """Get readings from sensors (check that doesn't raise)"""
    for source in Source:
        if 'SENSOR' not in source.name:
            continue
        elevator_id = randint(0, elevators_count - 1)
        command = Command(source=source.value, action='getReadings', elevator_id=elevator_id)
        returned_value = processor.process(command)
        print(returned_value)
        assert returned_value is not None


def test_sensors_readings(elevators, processor):
    """Check that readings are correct"""
    elevators[0].current_weight = 100
    assert processor.process(Command(source='sWeight', action='getReadings', elevator_id=0)) == 100

    elevators[1].is_light_on = True
    assert processor.process(Command(source='sLight', action='getReadings', elevator_id=1))

    elevators[2].is_doors_open = False
    assert not processor.process(Command(source='sDoors', action='getReadings', elevator_id=2))


def test_move_to_floor(elevators, processor):
    """Check move to floor command"""
    processor.process(Command(source='dispatcher', action='moveToFloor', elevator_id=0, value=6))
    assert elevators[0].current_floor == 6

    # Must not raise
    processor.process(Command(source='dispatcher', action='moveToFloor', elevator_id=0, value=100500))
    processor.process(Command(source='dispatcher', action='moveToFloor', elevator_id=100500, value=0))


def test_call_from_floor(elevators, processor):
    """Check call from floor command"""
    processor.process(Command(source='userOut', action='callFromFloor', value=3))
    assert elevators[0].current_floor == 3
    for i in range(1, elevators_count):
        assert elevators[i].current_floor == 0

    processor.process(Command(source='userOut', action='callFromFloor', value=20))
    assert elevators[0].current_floor == 20
    for i in range(1, elevators_count):
        assert elevators[i].current_floor == 0

    processor.process(Command(source='userOut', action='callFromFloor', value=17))
    assert elevators[0].current_floor == 17
    for i in range(1, elevators_count):
        assert elevators[i].current_floor == 0

    processor.process(Command(source='userOut', action='callFromFloor', value=6))
    assert elevators[0].current_floor == 17
    assert elevators[1].current_floor == 6
    assert elevators[2].current_floor == 0
