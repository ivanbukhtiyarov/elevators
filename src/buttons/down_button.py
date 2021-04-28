from src.elevator import Elevator
from src.operator import Operator
from src.buttons.abstract_button import AbstractButton


class DownButton(AbstractButton):
    def __init__(self, elevator: Elevator, operator: Operator):
        pass

    # Think about return type
    def get_state(self):
        pass

    def trigger(self):
        pass
