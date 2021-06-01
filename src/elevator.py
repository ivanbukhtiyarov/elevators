from collections import namedtuple
from typing import List
MoveRequest = namedtuple('MoveRequest', ['floor', 'requested_direction'])

class Elevator:
    def __init__(
        self, tonnage: int, floors_count: int, current_direction: int, 
        current_weight: int, is_light_on: bool, is_smoked: bool, requests: List[MoveRequest],
        is_communication_on: bool, is_doors_open: bool, 
        is_empty: bool, current_floor: int
    ):
        """
        current_direction: int - неинформативно, лучше сделать Enum
        аналогично для MoveRequest.requested_direction
        иначе их будет неудобно сравнивать для поиска ближайшего вызова
        """
        self.tonnage = tonnage
        self.floors_count = floors_count
        self.current_durection = current_direction
        self.current_weight = current_weight
        self.is_light_on = is_light_on
        self.is_smoked = is_smoked,
        self.requests: List[MoveRequest] = requests
        self.is_communication_on = is_communication_on
        self.is_doors_open = is_doors_open
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
        is_moving_up = (self.current_durection > 0) # Костыль из-за несоответствия типов
        
        if len(self.requests)<1:
            raise Exception("queue is empty")
    
        # разделяем то, что надодится выше, а что ниже 
        less_and_up = sorted([x for x in self.requests 
                              if x.floor<self.current_floor and x.requested_direction == True], 
                             reverse = True,key = lambda x:x[0])

        less_and_down = sorted([x for x in self.requests 
                                if x.floor<self.current_floor  and x.requested_direction == False], 
                               reverse = True,key = lambda x:x[0])

        bigger_and_up = sorted([x for x in self.requests 
                                if x.floor>self.current_floor  and x.requested_direction == True],
                              key = lambda x:x[0])

        bigger_and_down = sorted([x for x in self.requests 
                                  if x.floor>self.current_floor and x.requested_direction == False],
                                key = lambda x:x[0])

        if is_moving_up and len(bigger_and_up)>0:
            self.move_to_floor(bigger_and_up.pop(0).floor)

        elif is_moving_up and len(bigger_and_down)>0:
            self.current_durection = 0
            self.move_to_floor(bigger_and_down.pop(-1).floor)

        elif not is_moving_up and len(less_and_down)>0:
            self.move_to_floor(less_and_down.pop(0).floor)

        elif not is_moving_up and len(less_and_up)>0:
            self.current_durection = 1
            self.move_to_floor(less_and_up.pop(-1).floor)
        else:
            #если мы оказались тут, значит что то пошло не так
            raise Exception("Unexpected behaviour")
        
        self.requests = less_and_up+less_and_down+bigger_and_up+bigger_and_down

    def turn_smoke_on(self):
        self.is_smoked = True

    def turn_smoke_off(self):
        self.is_smoked = False

    def is_door_blocked(self):
        pass

    def call_dispatcher(self):
        self.is_communication_on = True

    def trigger(self):
        """
        Реакция на изменение параметров датчиков
        """
        pass