import abc


class ModelBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def translate(self, text: list[str]) -> list[str]:
        pass
