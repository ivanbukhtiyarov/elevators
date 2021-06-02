""" Behold! The CLI (Compact Lift sImulation) module.
The greatest command-line elevator simulator you have seen
"""

import sys
import os.path

import yaml

from src.elevator import Elevator
from src.operator import Operator
from src.command_processor import Command, CommandProcessor


def is_source_valid(source: str) -> bool:
    """ Source validation """
    # TODO: source must be one of allowed values from ri-04-01
    return True


def is_action_valid(action: str) -> bool:
    """ Action validation """
    # TODO: action must be one of allowed values from ri-04-01
    return True


def is_value_valid(action: str, value: str) -> bool:
    """ Value validation """
    # TODO: value must be suitable for the action
    return True


def is_command_valid(command: Command):
    return is_source_valid(command.source) and is_action_valid(command.action) and \
           (is_value_valid(command.action, command.value) if command.value else True)


def print_greeting() -> None:
    """ Say hello to user """
    print('Welcome to our CLI (Compact Lift sImulation) module')


def process_command(command: Command, command_processor: CommandProcessor):
    """ Perform actions based on user's command """
    if is_command_valid(command):
        command_processor.process(command)
    else:
        print('Sorry, the command is not valid')


def print_help() -> None:
    """ Basic non-interactive help """
    print("""Currently the following commands are supported:
    help - print this message;
    start - start simulation;
    stop - stop simulation;
    exit - close the program;
    <source> <action> [value=<value>] [elevator_id=<elevator_id>]  - give simulation command""")


def initialize_elevator() -> Elevator:
    print('First of all, we need to define some basic elevator parameters')
    tonnage = int(input('Please, define tonnage of the elevator in kilograms\n'))
    floors_count = int(input('Please, define amount of floors in the building\n'))
    print('Setting up the elevator...')
    elevator = Elevator(tonnage=tonnage, floors_count=floors_count, current_direction=0, current_weight=0,
                        is_light_on=False, is_smoked=False, requests=[], is_communication_on=False, is_doors_open=False,
                        is_doors_blocked=False, is_empty=True, current_floor=1)
    print('The elevator is set up and ready to go.')
    print('Feel free to explore it! Try typing <help> to learn more. Have fun!')
    return elevator


def is_start_query(split_input: list) -> bool:
    return len(split_input) == 1 and split_input[0] == 'start'


def is_stop_query(split_input: list) -> bool:
    return len(split_input) == 1 and split_input[0] == 'stop'


def is_help_query(split_input: list) -> bool:
    return len(split_input) == 1 and split_input[0] == 'help'


def is_command_query(split_input: list) -> bool:
    return 1 < len(split_input) < 5


def is_exit_query(split_input: list) -> bool:
    return len(split_input) == 1 and split_input[0] == 'exit'


def start_simulation():
    """ Actions before simulation start """
    print('Simulation started')


def stop_simulation():
    """ Actions after simulation stop """
    print('Simulation stopped')


def elevator_from_config(config_path=None):
    if config_path:
        if os.path.exists(config_path):
            with open(os.path.abspath(config_path), 'r') as f:
                config = yaml.safe_load(f)
            print(yaml.dump(config))
            try:
                elevator = Elevator(**config)
                print(f'Your elevator is {elevator}')
                return elevator
            except Exception as e:
                print(f'Problems with reading config file: {e}\n')
        else:
            print(f'No such file: {config_path}\n')


def main():
    # TODO: automatic (random) simulation mode
    print_greeting()

    elevator = None
    if len(sys.argv) > 2:
        if sys.argv[1] == '--config':
            config_path = sys.argv[2]
            elevator = elevator_from_config(config_path)
    if not elevator:
        elevator = initialize_elevator()
    command_processor = CommandProcessor(Operator([elevator]))

    is_simulation_active = False
    while True:
        split_input = input().split()
        if is_start_query(split_input):
            start_simulation()
            is_simulation_active = True
        elif is_stop_query(split_input):
            stop_simulation()
            is_simulation_active = False
        elif is_help_query(split_input):
            print_help()
        elif is_command_query(split_input):
            if is_simulation_active:
                value = None
                elevator_id = None

                if len(split_input) > 2:
                    third_argument = split_input[2].split('=')
                    if third_argument[0] == 'value':
                        value = third_argument[1]
                    elif third_argument[0] == 'elevator_id':
                        elevator_id = int(third_argument[1])
                    if len(split_input) > 3:
                        fourth_argument = split_input[3].split('=')
                        if fourth_argument[0] == 'value':
                            value = fourth_argument[1]
                        elif fourth_argument[0] == 'elevator_id':
                            elevator_id = int(fourth_argument[1])

                process_command(Command(source=split_input[0],
                                        action=split_input[1],
                                        value=value,
                                        elevator_id=elevator_id), command_processor)
            else:
                print('Simulation is not active')
        elif is_exit_query(split_input):
            confirmation_answer = input('Do you want to close the program (y/n)\n')
            while confirmation_answer != 'y' and confirmation_answer != 'n':
                confirmation_answer = input('Please, type "y" or "n"\n')
            if confirmation_answer == 'y':
                if is_simulation_active:
                    stop_simulation()
                return


if __name__ == '__main__':
    main()
