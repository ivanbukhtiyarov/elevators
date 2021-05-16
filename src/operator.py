"""
Из доки: IOperator описывает функционал диспетчера
вопрос нейминга не разрешён
"""
from src.elevator import Elevator
from typing import List


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
    
    def open_doors(self, num: int,):
        if num < 0 or num > len(self.elevators_list)-1:
            return "Wrong elevator number"
        self.elevators_list[num].open_doors()
    
    def close_doors(self, num: int,):
        if num < 0 or num > len(self.elevators_list)-1:
            return "Wrong elevator number"
        self.elevators_list[num].close_doors()

    def light_on(self, num: int,):
        if num < 0 or num > len(self.elevators_list)-1:
            return "Wrong elevator number"
        self.elevators_list[num].turn_light_on()
    
    def light_off(self, num: int,):
        if num < 0 or num > len(self.elevators_list)-1:
            return "Wrong elevator number"
        self.elevators_list[num].turn_light_off()
    
    def call(self):
        if num < 0 or num > len(self.elevators_list)-1:
            return "Wrong elevator number"
        """
        В доке написан про попытку
        ToDo: Реализовать именно попытку
        """
        try:
            self.elevators[num].call_dispatcher()
        except Exception as e:
            pass
    
    def move_to_floor(self,num: int, floor: int):
        if num < 0 or num > len(self.elevators_list)-1:
            return "Wrong elevator number"
        self.elevators_list[num].move_to_floor(floor)
    
    def get_elevator_state(self, num: int):
        if num < 0 or num > len(self.elevators_list)-1:
            return "Wrong elevator number"
        """
        Состояние кабины лифта
        Какое состояние???
        мб в классе лифта собрать инфу со всех датчиков
        """
        state = {direction: self.elevators_list[num].current_direction(),
        weight: self.elevators_list[num].current_weight(),
        light: self.elevators_list[num].is_light_on(),
        smoke: self.elevators_list[num].is_smoked(),
        requests: self.elevators_list[num].requests(),
        communication: self.elevators_list[num].is_communication_on(),
        is_doors_open: self.elevators_list[num].is_doors_open(),
        is_empty: self.elevators_list[num].is_empty(),
        }
        return state

    def restart(self):
        if num < 0 or num > len(self.elevators_list)-1:
            return "Wrong elevator number"
        """
        Tnot elevators_list.get(num)
        """
        self.elevators_list[num].current_direction = 0
        self.elevators_list[num].current_weight = 0
        self.elevators_list[num].turn_light_on()
        self.elevators_list[num].is_smoked = False
        self.elevators_list[num].requests = []
        self.elevators_list[num].is_communication_on = False
        self.elevators_list[num].open_doors()
        self.elevators_list[num].is_empty = True
        self.elevators_list[num].move_to_floor(1)
        # дожны ли эти функции возвращать информацию об успехе операции или что-то еще?