from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow


class ElevatorsWindow(QMainWindow):
    FLOOR_HEIGHT = 30
    BETWEEN_FLOORS = 5

    BUTTON_WIDTH = 60
    LABEL_WIDTH = 35
    BETWEEN_BUTTONS = 5

    BETWEEN_ELEVATORS = 80
    ELEVATOR_WIDTH = 22

    MARGIN_SIDE = 10
    MARGIN_HEIGHT = 20

    def __init__(self, floors: int, elevators: int):
        super().__init__()

        self.setWindowTitle("Лифты")
        self.calculate_height(floors)
        self.calculate_width(elevators)

        self.window_width = self.calculate_width(elevators)
        self.window_height = self.calculate_height(floors)
        self.resize(self.window_width, self.window_height)

        self.floors_number = floors
        self.elevators_number = elevators

        self.floor_labels = []
        self.up_buttons = []
        self.down_buttons= []

        # ToDo: заполнить отметки, на которых слайдер должен останавливаться
        #       по прибытии на этаж
        self.elevator_floor_checkpoints = []

        self.elevators = []

        for i in range(1, floors+1):
            self._init_floor(i)
        
        for j in range(1, elevators+1):
            self._init_elevator(j)
    
    def calculate_width(self, elevators_number: int):
        width = 2 * self.MARGIN_SIDE + self.LABEL_WIDTH + \
            2 * (self.BUTTON_WIDTH + self.BETWEEN_BUTTONS) + elevators_number * (self.ELEVATOR_WIDTH + self.BETWEEN_ELEVATORS)

        return width
    
    def calculate_height(self, floors_number: int):
        height = 2 * self.MARGIN_HEIGHT + floors_number * (self.FLOOR_HEIGHT + self.BETWEEN_FLOORS) - self.BETWEEN_FLOORS

        return height
    
    def _init_floor(self, number: int):
        floor_offset_y = self.window_height - (
            self.MARGIN_HEIGHT + number*self.FLOOR_HEIGHT + self.BETWEEN_FLOORS*(number - 1)
        )

        floor_label = QtWidgets.QLabel(self)
        floor_label.setGeometry(QtCore.QRect(self.MARGIN_SIDE, floor_offset_y, self.LABEL_WIDTH, self.FLOOR_HEIGHT))
        floor_label.setAlignment(QtCore.Qt.AlignCenter)
        floor_label.setText(str(number))

        up_button_offset_x = self.MARGIN_SIDE + self.LABEL_WIDTH + 5
        up_button = QtWidgets.QPushButton(self)
        up_button.setGeometry(QtCore.QRect(up_button_offset_x, floor_offset_y, self.BUTTON_WIDTH, self.FLOOR_HEIGHT))
        up_button.setText("up")

        down_button_offset_x = up_button_offset_x + self.BUTTON_WIDTH + self.BETWEEN_BUTTONS
        down_button = QtWidgets.QPushButton(self)
        down_button.setGeometry(QtCore.QRect(down_button_offset_x, floor_offset_y, self.BUTTON_WIDTH, self.FLOOR_HEIGHT))
        down_button.setText("down")

        self.floor_labels.append(floor_label)
        self.up_buttons.append(up_button)
        self.down_buttons.append(down_button)
    
    def _init_elevator(self, number: int):
        # Радиус шарика на слайдере
        circle_radius = 10
        elevators_section_offset_x = self.MARGIN_SIDE + self.LABEL_WIDTH + 5 + 2 * self.BUTTON_WIDTH + self.BETWEEN_BUTTONS

        elevator_x = elevators_section_offset_x + (number - 1)*self.ELEVATOR_WIDTH + (number - 1/2)*self.BETWEEN_ELEVATORS
        elevator_y = self.MARGIN_HEIGHT + self.FLOOR_HEIGHT/2 - circle_radius
        elevator_height = (self.floors_number - 1) * (self.FLOOR_HEIGHT + self.BETWEEN_FLOORS) + 2*(circle_radius)

        elevator = QtWidgets.QSlider(self)
        elevator.setGeometry(QtCore.QRect(elevator_x, elevator_y, self.ELEVATOR_WIDTH, elevator_height))
        elevator.setOrientation(QtCore.Qt.Vertical)

        self.elevators.append(elevator)

    def add_label(self):
        # ToDo: счетчик нажатий для этажа
        # запоминать номер и направление. Когда лифт приедет,
        # в зависимости от этажа и направления дисейблить кнопки неправильных этажей
        print("click")
