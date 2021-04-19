""" Command processing module. Contains the logic for RI-04-01 requirement. """

from collections import namedtuple

from src.elevator import Elevator

Command = namedtuple('Command', ['source', 'action', 'value'], defaults=['0'])


def process(command: Command, elevator: Elevator):
    if command.action == 'moveToFloor':
        try:
            floor = int(command.value)
        except ValueError:
            print('Sorry, bad value. Integer is required')
            return
        print(f'Moving to floor {floor}')
        elevator.current_floor = floor
    else:
        print('Sorry, not implemented at the moment')
