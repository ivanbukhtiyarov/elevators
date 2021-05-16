""" Command processing module. Contains the logic for RI-04-01 requirement. """

from enum import Enum
from src.elevator import Elevator
import attr


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
    value = attr.ib(default=None)


class CommandProcessor:
    def __init__(self, elevator: Elevator):
        self.elevator = elevator
        self.is_verbose = True  # Вывод сообщений в стдаут

    def process(self, command: Command):
        try:
            # Здесь в зависимости от сочетания Source и Action определяется метод-обработчик, который будет вызван
            source_enum_name = Source(command.source).name
            action_enum_name = Action(command.action).name
            processor = getattr(self, f'{source_enum_name.lower()}_{action_enum_name.lower()}')
            if command.value is not None:
                value = self.get_parsed_value(command.value, Action(command.action))
                if value is not None:
                    processor(value)
                else:
                    print('Illegal value for this action')
            else:
                processor()
        except AttributeError as e:
            self.default_process()
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

    def smoke_sensor_get_readings(self):
        if self.is_verbose:
            print('Getting readings from smoke sensor')
        return self.elevator.is_smoked

    def weight_sensor_get_readings(self):
        if self.is_verbose:
            print('Getting readings from weight sensor')
        return self.elevator.current_weight

    def position_sensor_get_readings(self):
        """ Возвращает текущий этаж и направление кабины лифта """
        if self.is_verbose:
            print('Getting readings from position sensor')
        return self.elevator.current_floor, self.elevator.current_direction

    def doors_sensor_get_readings(self):
        if self.is_verbose:
            print('Getting readings from doors sensor')
        return self.elevator.is_doors_open

    def light_sensor_get_readings(self):
        if self.is_verbose:
            print('Getting readings from light sensor')
        return self.elevator.is_light_on

    def dispatcher_open_doors(self):
        if self.is_verbose:
            print('Doors opened by dispatcher')
        return self.elevator.open_doors()

    def dispatcher_close_doors(self):
        if self.is_verbose:
            print('Doors closed by dispatcher')
        return self.elevator.close_doors()

    def dispatcher_move_to_floor(self, floor: int):
        if self.is_verbose:
            print('"Move to floor" request is made by dispatcher')
        return self.elevator.move_to_floor(floor)

    def dispatcher_set_weight(self, weight: int):
        if self.is_verbose:
            print('Weight has been manually set by dispatcher')
        self.elevator.current_weight = weight

    def dispatcher_set_light(self, on: bool):
        if on:
            if self.is_verbose:
                print('Light has been manually set on by dispatcher')
            self.elevator.turn_light_on()
        else:
            if self.is_verbose:
                print('Light has been manually set off by dispatcher')
            self.elevator.turn_light_off()

    def dispatcher_set_smoke(self, on: bool):
        if on:
            if self.is_verbose:
                print('Smoke has been manually set on by dispatcher')
            self.elevator.turn_smoke_on()
        else:
            if self.is_verbose:
                print('Smoke has been manually set off by dispatcher')
            self.elevator.turn_smoke_off()

    def dispatcher_set_barrier(self, on: bool):
        if on:
            if self.is_verbose:
                print('Door barrier has been manually set on by dispatcher')
            self.elevator.is_door_blocked = True
        else:
            if self.is_verbose:
                print('Door barrier has been manually set off by dispatcher')
            self.elevator.is_door_blocked = False

    def dispatcher_set_direction(self, direction: int):
        if self.is_verbose:
            print('Direction has been manually set on by dispatcher')
        self.elevator.current_direction = direction

    def dispatcher_intercom_request(self):
        if self.is_verbose:
            print('Intercom request was made by dispatcher')
        self.elevator.call_dispatcher()

    def dispatcher_intercom_respond(self):
        if self.is_verbose:
            print('Intercom response was made by dispatcher')
        self.elevator.call_dispatcher()

    def dispatcher_call_from_floor(self, floor: int):
        if self.is_verbose:
            print('"Call from floor" request is made by dispatcher')
        return self.elevator.move_to_floor(floor)

    def system_open_doors(self):
        if self.is_verbose:
            print('Doors opened by system')
        return self.elevator.open_doors()

    def system_close_doors(self):
        if self.is_verbose:
            print('Doors closed by system')
        return self.elevator.close_doors()

    def system_move_to_floor(self, floor: int):
        if self.is_verbose:
            print('"Move to floor" request is made by system')
        return self.elevator.move_to_floor(floor)

    def system_set_weight(self, weight: int):
        if self.is_verbose:
            print('Weight has been manually set by system')
        self.elevator.current_weight = weight

    def system_set_light(self, on: bool):
        if on:
            if self.is_verbose:
                print('Light has been manually set on by system')
            self.elevator.turn_light_on()
        else:
            if self.is_verbose:
                print('Light has been manually set off by system')
            self.elevator.turn_light_off()

    def system_set_smoke(self, on: bool):
        if on:
            if self.is_verbose:
                print('Smoke has been manually set on by system')
            self.elevator.turn_smoke_on()
        else:
            if self.is_verbose:
                print('Smoke has been manually set off by system')
            self.elevator.turn_smoke_off()

    def system_set_barrier(self, on: bool):
        if on:
            if self.is_verbose:
                print('Door barrier has been manually set on by system')
            self.elevator.is_door_blocked = True
        else:
            if self.is_verbose:
                print('Door barrier has been manually set off by system')
            self.elevator.is_door_blocked = False

    def system_set_direction(self, direction: int):
        if self.is_verbose:
            print('Direction has been manually set by system')
        self.elevator.current_direction = direction

    def system_set_floor_count(self, count: int):
        if self.is_verbose:
            print('Floor count has been manually set by system')
        self.elevator.current_direction = count

    def system_intercom_request(self):
        if self.is_verbose:
            print('Intercom request was made by system')
        self.elevator.call_dispatcher()

    def system_intercom_respond(self):
        if self.is_verbose:
            print('Intercom response was made by system')
        self.elevator.call_dispatcher()

    def system_get_current_params(self):
        if self.is_verbose:
            print('Getting elevator parameters')
        return {
            'tonnage': self.elevator.tonnage,
            'floors_count': self.elevator.floors_count,
            'current_direction': self.elevator.current_direction,
            'current_weight': self.elevator.current_weight,
            'is_light_on': self.elevator.is_light_on,
            'is_smoked': self.elevator.is_smoked,
            'requests': self.elevator.requests,
            'is_communication_on': self.elevator.is_communication_on,
            'is_doors_open': self.elevator.is_doors_open,
            'is_doors_blocked': self.elevator.is_doors_blocked,
            'is_empty': self.elevator.is_empty,
            'current_floor': self.elevator.current_floor,
        }

    def system_call_from_floor(self, floor: int):
        if self.is_verbose:
            print('"Call from floor" request is made by system')
        return self.elevator.move_to_floor(floor)

    def user_inside_open_doors(self):
        if self.is_verbose:
            print('Doors opened by a passenger inside')
        return self.elevator.open_doors()

    def user_inside_close_doors(self):
        if self.is_verbose:
            print('Doors a passenger inside')
        return self.elevator.close_doors()

    def user_inside_move_to_floor(self, floor: int):
        if self.is_verbose:
            print('"Move to floor" request is made by a passenger inside')
        return self.elevator.move_to_floor(floor)

    # Пока не совсем понятна логика запроса и ответа на голосовую связь.
    def user_inside_intercom_request(self):
        if self.is_verbose:
            print('Intercom request was made by a passenger inside')
        self.elevator.call_dispatcher()

    def user_outside_intercom_request(self):
        if self.is_verbose:
            print('Intercom request was made by a passenger outside')
        self.elevator.call_dispatcher()

    def user_outside_call_from_floor(self, floor: int):
        if self.is_verbose:
            print('"Call from floor" request is made by a passenger outside')
        return self.elevator.move_to_floor(floor)
