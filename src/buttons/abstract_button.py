from abc import ABC, abstractmethod


class AbstractButton(ABC):
    @abstractmethod
    def get_state(self, *args, **kwargs):
        pass

    @abstractmethod
    def trigger(self):
        pass
