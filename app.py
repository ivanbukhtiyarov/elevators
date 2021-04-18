""" Behold! The CLI (Compact Lift sImulation) module.
The greatest command-line elevator simulator you have seen
"""
from typing import Optional
from collections import namedtuple

from src.elevator import Elevator

Command = namedtuple('Command', ['source', 'action', 'value'])


def is_source_valid(source: str) -> bool:
    """ Source validation """
    # TODO: source must be one of allowed values from ri-04-01
    pass


def is_action_valid(action: str) -> bool:
    """ Action validation """
    # TODO: action must be one of allowed values from ri-04-01
    pass


def is_value_valid(action: str, value: str) -> bool:
    """ Value validation """
    # TODO: value must be suitable for the action
    pass


def is_command_valid(command: Command):
    return is_source_valid(command.source) and is_action_valid(command.action) and \
           (is_value_valid(command.value) if command.value else True)


def read_command() -> Optional[Command]:
    """ Read a command from user in format <source> <action> <value> """
    command_attributes = input().split()
    if len(command_attributes) < 2:
        print('You might have missed some arguments')
        return None
    elif len(command_attributes) > 3:
        print('Too many command arguments')
        return None

    source, action = command_attributes[0], command_attributes[1]
    value = command_attributes[2] if len(command_attributes) > 2 else None
    command = Command(source, action, value)

    return command if is_command_valid(command) else None


def print_greeting() -> None:
    """ Say hello to user """
    print('Welcome to our CLI (Compact Lift sImulation) module')
    print('Feel free to explore it! Try typing <help> to learn some syntax')


def process_command():
    """ Perform actions based on user's command """
    pass


def print_help() -> None:
    """ Basic non-interactive help """
    pass


def init_elevator(tonnage: int, floors_count: int) -> Elevator:
    return Elevator(tonnage=tonnage, floors_count=floors_count, current_direction=0, current_weight=0,
                    is_light_on=False, is_smoked=False, requests=[], is_communication_on=False, is_doors_open=False,
                    is_empty=True, current_floor=1)


def main():
    # TODO: Elevator parameters' (tonnage, floors_count and may be others) initialization on start,
    # Commands for simulation start and stop, help command and automatic (random) simulation mode
    # Simulation mode should be carefully logged
    print_greeting()
    user_command = read_command()
    while(user_command is not None):
        process_command()
        user_command = read_command()


if __name__ == '__main__':
    main()