""" Command processing module. Contains the logic for RI-04-01 requirement. """

from enum import Enum
from functools import partial

import attr

from src.operator import Operator


class Source(Enum):
    SMOKE_SENSOR = 'sSmoke'
    WEIGHT_SENSOR = 'sWeight'
    POSITION_SENSOR = 'sPosition'
    DOORS_SENSOR = 'sDoors'
    LIGHT_SENSOR = 'sLight'
    DISPATCHER = 'dispatcher'
    SYSTEM = 'system'
    USER_INSIDE = 'userIn'
    USER_OUTSIDE = 'userOut'


class Action(Enum):
    OPEN_DOORS = 'openDoors'
    CLOSE_DOORS = 'closeDoors'
    MOVE_TO_FLOOR = 'moveToFloor'
    SET_WEIGHT = 'setWeight'
    SET_LIGHT = 'setLight'
    SET_SMOKE = 'setSmoke'
    SET_BARRIER = 'setBarrier'
    SET_DIRECTION = 'setDirection'
    SET_FLOOR_COUNT = 'setFloorCount'
    INTERCOM_REQUEST = 'intercomRequest'
    INTERCOM_RESPOND = 'intercomRespond'
    GET_READINGS = 'getReadings' # снять показания датчика
    GET_CURRENT_PARAMS = 'getCurrentParams'
    CALL_FROM_FLOOR = 'callFromFloor'


@attr.s
class Command:
    source = attr.ib()
    action = attr.ib()
    value = attr.ib()
    elevator_id = attr.ib()


class CommandProcessor:
    def __init__(self, operator: Operator):
        self.operator = operator
        self.is_verbose = True  # Вывод сообщений в стдаут

    def process(self, command: Command):
        try:
            # Здесь в зависимости от сочетания Source и Action определяется метод-обработчик, который будет вызван
            source_enum_name = Source(command.source).name
            action_enum_name = Action(command.action).name
            processor = getattr(self, f'{source_enum_name.lower()}_{action_enum_name.lower()}')

            if command.value:
                value = self.get_parsed_value(command.value, Action(command.action))
                if value and command.elevator_id > 0:
                    processor(value, command.elevator_id)
                elif value:
                    processor(value)
                else:
                    print('Illegal value for this action')
            elif command.elevator_id > 0:
                processor(command.elevator_id)
            else:
                processor()
        except AttributeError as e:
            self.default_process()
        except TypeError as e:
            print('Something went wrong. Most possibly, the action does not support elevator id argument')
        except Exception as e:
            print('Something is wrong with the source or action')

    def get_parsed_value(self, value: str, action: Action):
        if action in [Action.SET_LIGHT, Action.SET_SMOKE, Action.SET_BARRIER]:
            if value in ['True', 'true', '1', 'on', 'On']:
                return True
            elif value in ['False', 'false', '0', 'off', 'Off']:
                return False
            else:
                return None
        elif action in [Action.CALL_FROM_FLOOR, Action.MOVE_TO_FLOOR, Action.SET_WEIGHT, Action.SET_FLOOR_COUNT]:
            try:
                return int(value)
            except ValueError:
                return None
        elif action == Action.SET_DIRECTION:
            # TODO: Заменить на енум, если direction поменяется с инта на енум
            try:
                direction = int(value)
                if direction in [-1, 0, 1]:
                    return direction
                else:
                    return None
            except ValueError:
                return None
        return None

    # Ниже обработчики запросов по парам Source, Action. Имена функций имеют вид <ключ_из_Source>_<ключ_из_Action>
    # Ключи переведелы в lowercase. Важно именовать по такому принципу,
    # потому что имена вызываемых методов определяются в рантайме в зависимости от комбинации Source и Action
    def default_process(self):
        print('Sorry, that source cannot perform the action')

    def smoke_sensor_get_readings(self, elevator_id: int):
        if self.is_verbose:
            print('Getting readings from smoke sensor')
        return self.operator.is_smoked(elevator_id)

    def weight_sensor_get_readings(self, elevator_id: int):
        if self.is_verbose:
            print('Getting readings from weight sensor')
        return self.operator.get_current_weight(elevator_id)

    def position_sensor_get_readings(self, elevator_id: int):
        """ Возвращает текущий этаж и направление кабины лифта """
        if self.is_verbose:
            print('Getting readings from position sensor')
        return self.operator.get_current_floor(elevator_id), self.operator.get_current_direction(elevator_id)

    def doors_sensor_get_readings(self, elevator_id: int):
        if self.is_verbose:
            print('Getting readings from doors sensor')
        return self.operator.is_doors_open(elevator_id)

    def light_sensor_get_readings(self, elevator_id: int):
        if self.is_verbose:
            print('Getting readings from light sensor')
        return self.operator.is_light_on(elevator_id)

    def dispatcher_open_doors(self, elevator_id: int):
        if self.is_verbose:
            print('Doors opened by dispatcher')
        return self.operator.open_doors(elevator_id)

    def dispatcher_close_doors(self, elevator_id: int):
        if self.is_verbose:
            print('Doors closed by dispatcher')
        return self.operator.close_doors(elevator_id)

    def dispatcher_move_to_floor(self, floor: int, elevator_id: int):
        if self.is_verbose:
            print('"Move to floor" request is made by dispatcher')
        return self.operator.move_to_floor(floor, elevator_id)

    def dispatcher_set_weight(self, weight: int, elevator_id: int):
        if self.is_verbose:
            print('Weight has been manually set by dispatcher')
        self.operator.set_weight(weight, elevator_id)

    def dispatcher_set_light(self, on: bool, elevator_id: int):
        if on:
            if self.is_verbose:
                print('Light has been manually set on by dispatcher')
            self.operator.turn_light_on(elevator_id)
        else:
            if self.is_verbose:
                print('Light has been manually set off by dispatcher')
            self.operator.turn_light_off(elevator_id)

    def dispatcher_set_smoke(self, on: bool, elevator_id: int):
        if on:
            if self.is_verbose:
                print('Smoke has been manually set on by dispatcher')
            self.operator.turn_smoke_on(elevator_id)
        else:
            if self.is_verbose:
                print('Smoke has been manually set off by dispatcher')
            self.operator.turn_smoke_off(elevator_id)

    def dispatcher_set_barrier(self, on: bool, elevator_id: int):
        if on:
            if self.is_verbose:
                print('Door barrier has been manually set on by dispatcher')
            self.operator.block_door(elevator_id)
        else:
            if self.is_verbose:
                print('Door barrier has been manually set off by dispatcher')
            self.operator.unblock_door(elevator_id)

    def dispatcher_set_direction(self, direction: int, elevator_id: int):
        if self.is_verbose:
            print('Direction has been manually set on by dispatcher')
        self.operator.set_direction(direction, elevator_id)

    def dispatcher_intercom_request(self, elevator_id: int):
        if self.is_verbose:
            print('Intercom request was made by dispatcher')
        self.operator.call_dispatcher(elevator_id)

    def dispatcher_intercom_respond(self, elevator_id: int):
        if self.is_verbose:
            print('Intercom response was made by dispatcher')
        self.operator.call_dispatcher(elevator_id)

    def dispatcher_call_from_floor(self, floor: int):
        if self.is_verbose:
            print('"Call from floor" request is made by dispatcher')

        try:
            return self.operator.process_call(floor)
        except ValueError as e:
            print(f'Cannot call an elevator: {e}')

    def system_open_doors(self, elevator_id: int):
        if self.is_verbose:
            print('Doors opened by system')
        return self.operator.open_doors(elevator_id)

    def system_close_doors(self, elevator_id: int):
        if self.is_verbose:
            print('Doors closed by system')
        return self.operator.close_doors(elevator_id)

    def system_move_to_floor(self, floor: int, elevator_id: int):
        if self.is_verbose:
            print('"Move to floor" request is made by system')
        return self.operator.move_to_floor(floor, elevator_id)

    def system_set_weight(self, weight: int, elevator_id: int):
        try:
            if self.is_verbose:
                print('Weight has been manually set by system')
            self.operator.set_weight(weight, elevator_id)
        except ValueError as e:
            print(e)

    def system_set_light(self, on: bool, elevator_id: int):
        try:
            if on:
                if self.is_verbose:
                    print('Light has been manually set on by system')
                self.operator.turn_light_on(elevator_id)
            else:
                if self.is_verbose:
                    print('Light has been manually set off by system')
                self.operator.turn_light_off(elevator_id)
        except ValueError as e:
            print(e)

    def system_set_smoke(self, on: bool, elevator_id: int):
        try:
            if on:
                if self.is_verbose:
                    print('Smoke has been manually set on by system')
                self.operator.turn_smoke_on(elevator_id)
            else:
                if self.is_verbose:
                    print('Smoke has been manually set off by system')
                self.operator.turn_smoke_off(elevator_id)
        except ValueError as e:
            print(e)

    def system_set_barrier(self, on: bool, elevator_id: int):
        try:
            if on:
                if self.is_verbose:
                    print('Door barrier has been manually set on by system')
                self.operator.block_door(elevator_id)
            else:
                if self.is_verbose:
                    print('Door barrier has been manually set off by system')
                self.operator.unblock_door(elevator_id)
        except ValueError as e:
            print(e)

    def system_set_direction(self, direction: int, elevator_id: int):
        try:
            if self.is_verbose:
                print('Direction has been manually set by system')
            self.operator.set_direction(direction, elevator_id)
        except ValueError as e:
            print(e)

    def system_set_floor_count(self, count: int):
        try:
            self.operator.set_floor_count(count)
            if self.is_verbose:
                print('Floor count has been manually set by system')
        except ValueError as e:
            print(e)

    def system_intercom_request(self, elevator_id: int):
        if self.is_verbose:
            print('Intercom request was made by system')
        self.operator.call_dispatcher(elevator_id)

    def system_intercom_respond(self, elevator_id: int):
        if self.is_verbose:
            print('Intercom response was made by system')
        self.operator.call_dispatcher(elevator_id)

    def system_get_current_params(self, elevator_id: int):
        if self.is_verbose:
            print('Getting elevator parameters')
        return {
            'tonnage': self.operator.get_tonnage(elevator_id),
            'floors_count': self.operator.get_floors_count(elevator_id),
            'current_direction': self.operator.get_current_direction(elevator_id),
            'current_weight': self.operator.get_current_weight(elevator_id),
            'is_light_on': self.operator.is_light_on(elevator_id),
            'is_smoked': self.operator.is_smoked(elevator_id),
            'requests': self.operator.get_requests(elevator_id),
            'is_communication_on': self.operator.is_communication_on(elevator_id),
            'is_doors_open': self.operator.is_doors_open(elevator_id),
            'is_doors_blocked': self.operator.is_doors_blocked(elevator_id),
            'is_empty': self.operator.is_empty(elevator_id),
            'current_floor': self.operator.get_current_floor(elevator_id),
        }

    def system_call_from_floor(self, floor: int):
        if self.is_verbose:
            print('"Call from floor" request is made by system')

        try:
            return self.operator.process_call(floor)
        except ValueError as e:
            print(f'Cannot call an elevator: {e}')

    def user_inside_open_doors(self, elevator_id: int):
        if self.is_verbose:
            print('Doors opened by a passenger inside')
        return self.operator.open_doors(elevator_id)

    def user_inside_close_doors(self, elevator_id: int):
        if self.is_verbose:
            print('Doors a passenger inside')
        return self.operator.close_doors(elevator_id)

    def user_inside_move_to_floor(self, floor: int, elevator_id: int):
        if self.is_verbose:
            print('"Move to floor" request is made by a passenger inside')
        return self.operator.move_to_floor(floor, elevator_id)

    # Пока не совсем понятна логика запроса и ответа на голосовую связь.
    def user_inside_intercom_request(self, elevator_id: int):
        if self.is_verbose:
            print('Intercom request was made by a passenger inside')
        self.operator.call_dispatcher(elevator_id)

    def user_outside_intercom_request(self, elevator_id: int):
        if self.is_verbose:
            print('Intercom request was made by a passenger outside')
        self.operator.call_dispatcher(elevator_id)

    def user_outside_call_from_floor(self, floor: int):
        if self.is_verbose:
            print('"Call from floor" request is made by a passenger outside')

        try:
            return self.operator.process_call(floor)
        except ValueError as e:
            print(f'Cannot call an elevator: {e}')
