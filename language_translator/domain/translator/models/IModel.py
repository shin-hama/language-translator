import abc


class IModel(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def translate(self, text: str) -> str:
        pass
