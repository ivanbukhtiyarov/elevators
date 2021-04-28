from abc import ABC, abstractmethod


class AbstractSensor(ABC):
    @abstractmethod
    def get_state(self, *args, **kwargs):
        """
        Снятие показаний с датчика
        Какие входные параметры???
        """
        pass

    @abstractmethod
    def trigger(self):
        """
        Оповещение оператора об изменении параметра
        """
        pass
