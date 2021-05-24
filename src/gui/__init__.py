from typing import List
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow
from dataclasses import dataclass
import random


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


class Elevator:
    def __init__(self, parent_widget: int, number: int, floors_number: int, ui_config: UIConfig):
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
    
    def move_to_floor(self, floor_number):
        self.slider.setValue(floor_number)
    
    def trigger_smoke_sensor(self):
        print(f"Triggered smoke sensor for elevator {self.number}")
    
    def trigger_light_sensor(self):
        print(f"Triggered light sensor for elevator {self.number}")
    
    def trigger_doors_sensor(self):
        print(f"Triggered doors sensor for elevator {self.number}")


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
        
        for j in range(1, elevators+1):
            self._init_elevator(j)
    
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
        random_elevator = random.randint(0, self.elevators_number - 1)
        self.elevators[random_elevator].move_to_floor(floor_number)
