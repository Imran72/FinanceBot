from enum import Enum


# Класс состояний для пользователя
class Mode():

    def __init__(self):
        self.mode = self.States.INITIAL_STATE

    class States(Enum):
        # Исходное состояние бота: режим выбора функции
        INITIAL_STATE = 0
        # Состояние записи данных полученных от пользователя
        RECORDING_STATE = 1
