from src.elevator import Elevator
from src.operator import Operator
from src.sensors.abstract_sensor import AbstractSensor


class DoorBlockSensor(AbstractSensor):
    def __init__(self, elevator: Elevator, operator: Operator):
        pass

    # Think about return type
    def get_state(self):
        pass

    def trigger(self):
        pass
