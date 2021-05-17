import attr
from typing import List


# requested_direction - направление, куда вызвали лифт
@attr.s
class MoveRequest:
    floor = attr.ib()
    requested_direction = attr.ib()


class Elevator:
    def __init__(
        self, tonnage: int, floors_count: int, current_direction: int = 0,
        current_weight: int = 0, is_light_on: bool = False, is_smoked: bool = False, requests: List[MoveRequest] = [],
        is_communication_on: bool = False, is_doors_open: bool = False, is_doors_blocked: bool = False,
        is_empty: bool = True, current_floor: int = 1
    ):
        """
        current_direction: int - неинформативно, лучше сделать Enum
        аналогично для MoveRequest.requested_direction
        иначе их будет неудобно сравнивать для поиска ближайшего вызова
        """
        self.tonnage = tonnage
        self.floors_count = floors_count
        self.current_direction = current_direction
        self.current_weight = current_weight
        self.is_light_on = is_light_on
        self.is_smoked = is_smoked
        self.requests: List[MoveRequest] = requests
        self.is_communication_on = is_communication_on
        self.is_doors_open = is_doors_open
        self.is_doors_blocked = is_doors_blocked
        self.is_empty = is_empty
        self.current_floor = current_floor

    def open_doors(self):
        self.is_doors_open = True

    def close_doors(self):
        self.is_doors_open = False

    def turn_light_on(self):
        self.is_light_on = True

    def turn_light_off(self):
        self.is_light_on = False

    def _alarm(self):
        """
        Из доки: Оповещение о внештатной ситуации???
        Кого оповестить? Каким образом?
        """
        pass

    def move_to_floor(self, floor: int):
        """
        Наверное, тут ожидается какая-то логика имитации движения
        """
        self.current_floor = floor

    def add_request(self, request: MoveRequest):
        self.requests.append(request)

    def next_request(self):
        """
        Кажется, что взять запрос и приехать на этаж
        Вероятно, вместо списка нужно использовать какое-то дерево,
        с помощью которого можно отбирать ближайший запрос
        по направлению движения
        """
        is_moving_up = (self.current_direction > 0) # Костыль из-за несоответствия типов
        first_request = self.requests.pop(0)
        if first_request.requested_direction == is_moving_up: # bool мешает читаемость кода (см. прим. про Enum в __init__)
            self.move_to_floor(first_request.floor)
        # А вот иначе ничего не произойдёт, поэтому нужна какая-то другая структура хранения requests

    def turn_smoke_on(self):
        self.is_smoked = True

    def turn_smoke_off(self):
        self.is_smoked = False

    def call_dispatcher(self):
        self.is_communication_on = True

    def trigger(self):
        """
        Реакция на изменение параметров датчиков
        """
        pass
