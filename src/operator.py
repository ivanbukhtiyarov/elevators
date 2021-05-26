"""
Из доки: IOperator описывает функционал диспетчера
вопрос нейминга не разрешён
"""
from typing import List, Optional

from src.elevator import Elevator, MoveRequest


class Operator:
    def __init__(self, elevators: List[Elevator]):
        """
        Из доки:
        Содержит ссылку на экземпляр лифта
        Зачем?
        Разве диспетчер не следит за несколькими лифтами?
        Кажется, нужно несколько лифтов
        """

        self.elevators_list = elevators

    def open_doors(self, num: int) -> None:
        if num < 1 or num > len(self.elevators_list):
            raise ValueError('Wrong elevator number')
        self.elevators_list[num - 1].open_doors()

    def close_doors(self, num: int) -> None:
        if num < 1 or num > len(self.elevators_list):
            raise ValueError('Wrong elevator number')
        self.elevators_list[num - 1].close_doors()

    def call_dispatcher(self, num: int) -> None:
        if num < 1 or num > len(self.elevators_list):
            raise ValueError('Wrong elevator number')
        """
        В доке написан про попытку
        ToDo: Реализовать именно попытку
        """
        try:
            self.elevators_list[num - 1].call_dispatcher()
        except Exception as e:
            pass

    def move_to_floor(self, floor: int, num: int) -> None:
        if num < 1 or num > len(self.elevators_list):
            raise ValueError('Wrong elevator number')
        self.elevators_list[num - 1].move_to_floor(floor)

    def get_elevator_state(self, num: int) -> dict:
        if num < 1 or num > len(self.elevators_list):
            raise ValueError('Wrong elevator number')
        """
        Состояние кабины лифта
        Какое состояние???
        мб в классе лифта собрать инфу со всех датчиков
        """
        state = {
            "direction": self.elevators_list[num - 1].current_direction,
            "weight": self.elevators_list[num - 1].current_weight,
            "light": self.elevators_list[num - 1].is_light_on,
            "smoke": self.elevators_list[num - 1].is_smoked,
            "requests": self.elevators_list[num - 1].requests,
            "communication": self.elevators_list[num - 1].is_communication_on,
            "is_doors_open": self.elevators_list[num - 1].is_doors_open,
            "is_empty": self.elevators_list[num - 1].is_empty,
        }
        return state

    def restart(self, num: int) -> None:
        if num < 1 or num > len(self.elevators_list):
            raise ValueError('Wrong elevator number')

        self.elevators_list[num - 1].current_floor = 1
        self.elevators_list[num - 1].current_direction = 0
        self.elevators_list[num - 1].current_weight = 0
        self.elevators_list[num - 1].turn_light_on()
        self.elevators_list[num - 1].is_smoked = False
        self.elevators_list[num - 1].requests = []
        self.elevators_list[num - 1].is_doors_blocked = False
        self.elevators_list[num - 1].is_communication_on = False
        self.elevators_list[num - 1].open_doors()
        self.elevators_list[num - 1].is_empty = True
        self.elevators_list[num - 1].move_to_floor(1)
        # дожны ли эти функции возвращать информацию об успехе операции или что-то еще?

    def get_tonnage(self, elevator_id: int) -> Optional[int]:
        if 0 < elevator_id <= len(self.elevators_list) :
            return self.elevators_list[elevator_id].tonnage
        return None

    def get_floors_count(self, elevator_id: int) -> Optional[int]:
        if 0 < elevator_id <= len(self.elevators_list) :
            return self.elevators_list[elevator_id].floors_count
        return None

    def get_current_direction(self, elevator_id: int) -> Optional[int]:
        if 0 < elevator_id <= len(self.elevators_list) :
            return self.elevators_list[elevator_id].current_direction
        return None

    def get_current_weight(self, elevator_id: int) -> Optional[int]:
        if 0 < elevator_id <= len(self.elevators_list) :
            return self.elevators_list[elevator_id].current_weight
        return None

    def is_light_on(self, elevator_id: int) -> Optional[bool]:
        if 0 < elevator_id <= len(self.elevators_list) :
            return self.elevators_list[elevator_id].is_light_on
        return None

    def is_smoked(self, elevator_id: int) -> Optional[bool]:
        if 0 < elevator_id <= len(self.elevators_list) :
            return self.elevators_list[elevator_id].is_smoked
        return None

    def get_requests(self, elevator_id: int) -> Optional[list[MoveRequest]]:
        if 0 < elevator_id <= len(self.elevators_list) :
            return self.elevators_list[elevator_id].requests
        return None

    def is_communication_on(self, elevator_id: int) -> Optional[bool]:
        if 0 < elevator_id <= len(self.elevators_list) :
            return self.elevators_list[elevator_id].is_communication_on
        return None

    def is_doors_open(self, elevator_id: int) -> Optional[bool]:
        if 0 < elevator_id <= len(self.elevators_list) :
            return self.elevators_list[elevator_id].is_doors_open
        return None

    def is_doors_blocked(self, elevator_id: int) -> Optional[bool]:
        if 0 < elevator_id <= len(self.elevators_list) :
            return self.elevators_list[elevator_id].is_doors_blocked
        return None

    def is_empty(self, elevator_id: int) -> Optional[bool]:
        if 0 < elevator_id <= len(self.elevators_list) :
            return self.elevators_list[elevator_id].is_empty
        return None

    def get_current_floor(self, elevator_id: int) -> Optional[int]:
        if 0 < elevator_id <= len(self.elevators_list) :
            return self.elevators_list[elevator_id].current_floor
        return None

    def process_call(self, floor) -> None:
        if not 1 < floor <= self.elevators_list[0].floors_count:
            raise ValueError('Floor is out of range')

        best_elevator_id = self._find_suitable_elevator_id(floor)
        self.elevators_list[best_elevator_id].add_request(MoveRequest(floor))

    def _find_suitable_elevator_id(self, floor: int) -> int:
        best_elevator_id = 0
        for i, elevator in enumerate(self.elevators_list):
            if self._is_approaching(elevator, floor) \
                    and self._is_closer(rookie=elevator, champion=self.elevators_list[best_elevator_id], floor=floor):
                best_elevator_id = i
        return best_elevator_id

    def _is_approaching(self, elevator: Elevator, floor: int) -> bool:
        return elevator.current_direction == 0 \
               or elevator.current_floor > floor and elevator.current_direction == -1 \
               or elevator.current_floor < floor and elevator.current_direction == 1

    def _is_closer(self, rookie: Elevator, champion: Elevator, floor: int) -> bool:
        return abs(rookie.current_floor - floor) < abs(champion.current_floor - floor)

    def set_floor_count(self, count: int):
        if count < 1:
            raise ValueError('Floor number less than one')

        for elevator in self.elevators_list:
            elevator.floors_count = count

    def set_direction(self, direction, elevator_id: int):
        if direction not in [-1, 0, 1]:
            raise ValueError('Bad direction')
        if not 0 < elevator_id <= len(self.elevators_list):
            raise ValueError('Bad elevator id')

        self.elevators_list[elevator_id].current_direction = direction

    def block_door(self, elevator_id: int):
        if not 0 < elevator_id <= len(self.elevators_list):
            raise ValueError('Bad elevator id')

        self.elevators_list[elevator_id].is_doors_blocked = True

    def unblock_door(self, elevator_id: int):
        if not 0 < elevator_id <= len(self.elevators_list):
            raise ValueError('Bad elevator id')

        self.elevators_list[elevator_id].is_doors_blocked = False

    def turn_smoke_on(self, elevator_id: int):
        if not 0 < elevator_id <= len(self.elevators_list):
            raise ValueError('Bad elevator id')

        self.elevators_list[elevator_id].is_smoked = True

    def turn_smoke_off(self, elevator_id: int):
        if not 0 < elevator_id <= len(self.elevators_list):
            raise ValueError('Bad elevator id')

        self.elevators_list[elevator_id].is_smoked = False

    def turn_light_on(self, elevator_id: int):
        if not 0 < elevator_id <= len(self.elevators_list):
            raise ValueError('Bad elevator id')

        self.elevators_list[elevator_id].is_light_on = True

    def turn_light_off(self, elevator_id: int):
        if not 0 < elevator_id <= len(self.elevators_list):
            raise ValueError('Bad elevator id')

        self.elevators_list[elevator_id].is_light_on = False

    def set_weight(self, weight: int, elevator_id: int):
        if not 0 < elevator_id <= len(self.elevators_list):
            raise ValueError('Bad elevator id')
        if weight < 0:
            raise ValueError('Weight cannot be less than 0')

        self.elevators_list[elevator_id].current_weight = weight
