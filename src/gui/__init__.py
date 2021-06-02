from typing import List
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow
from dataclasses import dataclass
import random
import math
from src.command_processor import Command, CommandProcessor, Source, Action
from src.operator import Operator
from src.elevator import Elevator as ElevatorLogic
import time


class SliderWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(int)

    def run(self, start, finish, step):
        while start != finish:
            start += step
            time.sleep(0.5)
            print(start)
            self.progress.emit(start)
        self.finished.emit()


@dataclass
class UIConfig:
    floor_height: int = 30
    between_floors: int = 5

    button_width: int = 65
    label_width: int = 35
    between_buttons: int = 5

    between_elevators: int = 70
    elevator_width: int = 22

    margin_side: int = 10
    margin_height: int = 20

    circle_radius: int = 10

    def button_size(self):
        return (self.button_width, self.floor_height)

    def calculate_width(self, elevators_number: int) -> int:
        width = 2 * self.margin_side + self.label_width + \
            2 * (self.button_width + self.between_buttons) + elevators_number * (self.elevator_width + self.between_elevators) \
            + elevators_number * self.button_width

        return width

    def calculate_height(self, floors_number: int) -> int:
        height = 2 * self.margin_height + floors_number * (self.floor_height + self.between_floors) - self.between_floors

        return height
    
    def calculate_floor_offset_y(self, total_height, floor_number):
        return total_height - (
            self.margin_height + floor_number*self.floor_height + self.between_floors*(floor_number - 1)
        )
    
    @property
    def elevators_section_offset_x(self):
        return self.margin_side + self.label_width + 5 + 2 * self.button_width + self.between_buttons
    
    def calculate_elevator_offset_x(self, number: int) -> int:
        return self.elevators_section_offset_x + (number - 1)*self.elevator_width + (number - 1/2)*self.between_elevators \
            + (number - 1)*self.button_width  # ширина кнопок датчиков
    
    def calculate_elevator_offset_y(self):
        return self.margin_height + self.floor_height/2 - self.circle_radius

    def calculate_elevator_height(self, floor_number: int):
        return (floor_number - 1) * (self.floor_height + self.between_floors) + 2*(self.circle_radius)
    
    def calculate_sensors_offset_x(self, number):
        return self.calculate_elevator_offset_x(number) + self.elevator_width + (self.between_elevators - self.button_width)/2

    def calculate_sensor_offset_y(self, floors_number, sensor_number):
        sensors_total = 3  # HARDCODE
        window_height = self.calculate_height(floors_number)

        middle_window = window_height / 2

        return middle_window + (sensors_total/2 - sensor_number) * self.floor_height
    
    def select_window_size(self, floors_number):
        columns = 2
        rows = math.ceil(floors_number / columns)
        width = 2*self.margin_side + columns*self.button_width + (columns - 1)*self.between_buttons
        height = 2*self.margin_height + rows * self.floor_height + (rows-1) * self.between_floors

        return (width, height)
    
    def select_floor_button_offset(self, floor_number, total_floors):
        columns = 2
        rows = math.ceil(total_floors / columns)

        button_column = floor_number // rows
        button_row = floor_number % rows

        (_, height) = self.select_window_size(total_floors)

        button_x = self.margin_side + button_column*(self.button_width + self.between_buttons)
        button_y = height - (2* self.margin_height + button_row*(self.floor_height + self.between_floors))

        return (button_x, button_y)


class Elevator:
    def __init__(self, parent_widget, number: int, floors_number: int, ui_config: UIConfig):
        self.current_floor = 1
        self._is_locked = False

        self.logic = ElevatorLogic(floors_count=floors_number, tonnage=10000)
        self.parent_widget = parent_widget
        self.total_floors = floors_number

        self.ui_config = ui_config
        self.number = number
        self.height = self.ui_config.calculate_elevator_height(floors_number)

        elevator_x = self.ui_config.calculate_elevator_offset_x(number)
        elevator_y = self.ui_config.calculate_elevator_offset_y()

        self.slider = QtWidgets.QSlider(parent_widget)
        self.slider.setGeometry(QtCore.QRect(elevator_x, elevator_y, self.ui_config.elevator_width, self.height))
        self.slider.setOrientation(QtCore.Qt.Vertical)
        self.slider.setMinimum(1)
        self.slider.setMaximum(floors_number)
        self.slider.setDisabled(True)

        sensors_offset_x = self.ui_config.calculate_sensors_offset_x(number)

        smoke_sensor_offset_y = self.ui_config.calculate_sensor_offset_y(floors_number, sensor_number=0)
        self.smoke_sensor = QtWidgets.QPushButton(parent_widget)
        self.smoke_sensor.setGeometry(QtCore.QRect(
            sensors_offset_x, smoke_sensor_offset_y, self.ui_config.button_width, self.ui_config.floor_height
        ))
        self.smoke_sensor.setText("Дым")
        self.smoke_sensor.clicked.connect(self.trigger_smoke_sensor)

        light_sensor_offset_y = self.ui_config.calculate_sensor_offset_y(floors_number, sensor_number=1)
        self.light_sensor = QtWidgets.QPushButton(parent_widget)
        self.light_sensor.setGeometry(QtCore.QRect(
            sensors_offset_x, light_sensor_offset_y, self.ui_config.button_width, self.ui_config.floor_height
        ))
        self.light_sensor.setText("Свет")
        self.light_sensor.clicked.connect(self.trigger_light_sensor)

        doors_sensor_offset_y = self.ui_config.calculate_sensor_offset_y(floors_number, sensor_number=2)
        self.doors_sensor = QtWidgets.QPushButton(parent_widget)
        self.doors_sensor.setGeometry(QtCore.QRect(
            sensors_offset_x, doors_sensor_offset_y, self.ui_config.button_width, self.ui_config.floor_height
        ))
        self.doors_sensor.setText("Двери")
        self.doors_sensor.clicked.connect(self.trigger_doors_sensor)
    
    def _show_select_floor_dialog(self, should_show_dialog, floor_number):
        if should_show_dialog:
            select_dialog = SelectFloorDialog(self, floor_number)
            select_dialog.exec_()
    
    def move_to_floor(self, to, should_show_dialog = True):
        self.current_floor = to
        self._is_locked = True
        _from = self.slider.value()
        duration = abs(to - _from) * 500
        self.animation = QtCore.QPropertyAnimation(self.slider, b"sliderPosition")
        self.animation.setDuration(duration)
        self.animation.setStartValue(_from)
        self.animation.setEndValue(to)
        self.animation.start()
        self.animation.finished.connect(self.unlock)
        self.animation.finished.connect(lambda: self._show_select_floor_dialog(should_show_dialog, to))
    
    def unlock(self):
        self._is_locked = False
    
    def trigger_smoke_sensor(self):
        my_dialog = QtWidgets.QDialog(self.parent_widget)
        label = QtWidgets.QLabel(my_dialog)
        label.setText(f"Сработал датчик задымления в лифте {self.number}")
        label.adjustSize()
        my_dialog.adjustSize()
        my_dialog.exec_()
        self.move_to_floor(1, False)
    
    def trigger_light_sensor(self):
        my_dialog = QtWidgets.QDialog(self.parent_widget)
        label = QtWidgets.QLabel(my_dialog)
        label.setText(f"Перебои электричества в лифте {self.number}")
        label.adjustSize()
        my_dialog.adjustSize()
        my_dialog.exec_()
        self.move_to_floor(1, False)
    
    def trigger_doors_sensor(self):
        my_dialog = QtWidgets.QDialog(self.parent_widget)
        label = QtWidgets.QLabel(my_dialog)
        label.setText(f"Двери лифта {self.number} заблокированы")
        label.adjustSize()
        my_dialog.adjustSize()
        my_dialog.exec_()
        self.move_to_floor(1, False)
    
    def add_call(self, floor_number):
        print(f"Elevator {self.number} called to {floor_number} floor")


class SelectFloorDialog(QtWidgets.QDialog):
    def __init__(self, elevator: Elevator, floor_number):
        super().__init__(elevator.parent_widget)
        self.elevator = elevator
        self.setWindowTitle(f"{floor_number} этаж")
        label = QtWidgets.QLabel(self)
        label.setText(f"Лифт {elevator.number}")
        self.resize(*elevator.ui_config.select_window_size(elevator.total_floors))
        for i in range(elevator.total_floors):
            self._init_button(i, floor_number)
    
    def _init_button(self, i, floor_number):
        floor_button = QtWidgets.QPushButton(self)
        floor_button.setText(str(i+1))
        floor_button.setGeometry(
            QtCore.QRect(
                *self.elevator.ui_config.select_floor_button_offset(i+1, self.elevator.total_floors), 
                *self.elevator.ui_config.button_size())
        )
        if i+1 == floor_number:
            floor_button.setDisabled(True)

        floor_button.clicked.connect(lambda: self.button_callback(i))
    
    def button_callback(self, n):
        self.elevator.move_to_floor(n+1, False)
        self.elevator.logic.move_to_floor(n+1)
        self.close()


class ElevatorsWindow(QMainWindow):
    def __init__(self, 
        floors: int, elevators: int, 
        ui_config: UIConfig = UIConfig()
    ):
        super().__init__()

        self.ui_config: UIConfig = ui_config

        self.setWindowTitle("Лифты")

        self.window_width = self.ui_config.calculate_width(elevators)
        self.window_height = self.ui_config.calculate_height(floors)
        self.resize(self.window_width, self.window_height)

        self.floors_number = floors
        self.elevators_number = elevators

        self.floor_labels = []
        self.up_buttons = []
        self.down_buttons= []

        # ToDo: заполнить отметки, на которых слайдер должен останавливаться
        #       по прибытии на этаж
        self.elevator_floor_checkpoints = []

        self.elevators: List[Elevator] = []

        for i in range(1, floors+1):
            self._init_floor(i)
        
        self.up_buttons[-1].hide()
        self.down_buttons[0].hide()
        
        for j in range(1, elevators+1):
            self._init_elevator(j)

        self.processor = CommandProcessor(Operator(
            [x.logic for x in self.elevators]
        ))
    
    def _init_floor(self, number: int):
        floor_offset_y = self.ui_config.calculate_floor_offset_y(self.window_height, number)

        # ToDo: calculations to UIConfig
        floor_label = QtWidgets.QLabel(self)
        floor_label.setGeometry(QtCore.QRect(self.ui_config.margin_side, floor_offset_y, self.ui_config.label_width, self.ui_config.floor_height))
        floor_label.setAlignment(QtCore.Qt.AlignCenter)
        floor_label.setText(str(number))

        up_button_offset_x = self.ui_config.margin_side + self.ui_config.label_width + 5
        up_button = QtWidgets.QPushButton(self)
        up_button.setGeometry(QtCore.QRect(up_button_offset_x, floor_offset_y, self.ui_config.button_width, self.ui_config.floor_height))
        up_button.setText("up")
        up_button.clicked.connect(lambda: self.call_elevator(number))

        down_button_offset_x = up_button_offset_x + self.ui_config.button_width + self.ui_config.between_buttons
        down_button = QtWidgets.QPushButton(self)
        down_button.setGeometry(QtCore.QRect(down_button_offset_x, floor_offset_y, self.ui_config.button_width, self.ui_config.floor_height))
        down_button.setText("down")
        down_button.clicked.connect(lambda: self.call_elevator(number))

        self.floor_labels.append(floor_label)
        self.up_buttons.append(up_button)
        self.down_buttons.append(down_button)
    
    def _init_elevator(self, number: int):
        elevator = Elevator(self, number, self.floors_number, self.ui_config)
        self.elevators.append(elevator)

    def call_elevator(self, floor_number):
        self.processor.process(Command(
            source=Source.SYSTEM,
            action=Action.CALL_FROM_FLOOR, 
            value=floor_number,
        ))
        for (i, elevator) in enumerate(self.elevators):
            elevator_params = self.processor.process(Command(
                source=Source.SYSTEM,
                action=Action.GET_CURRENT_PARAMS,
                elevator_id=i,
            ))
            if elevator_params['current_floor'] != elevator.current_floor and not elevator._is_locked:
                elevator.move_to_floor(floor_number)
