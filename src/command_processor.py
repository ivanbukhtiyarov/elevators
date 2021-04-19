""" Command processing module. Contains the logic for RI-04-01 requirement. """

from collections import namedtuple

from src.elevator import Elevator

Command = namedtuple('Command', ['source', 'action', 'value'], defaults=['0'])


def handle_move_to_floor(command: Command, elevator: Elevator):
    try:
        floor = int(command.value)
    except ValueError:
        print('Sorry, bad value. Integer is required')
        return
    print(f'Moving to floor {floor}')
    elevator.current_floor = floor


def process(command: Command, elevator: Elevator):
    dispatcher = {
        'moveToFloor': handle_move_to_floor,
    }
        
    if command.action not in dispatcher:
        print('Sorry, not implemented at the moment')
        return
    
    dispatcher[command.action](command, elevator)
