import abc
import time


tepoc = time.time


class Subject(object):
    def __init__(self):
        self._observers = set()

    def addObserver(self, observer):
        self._observers.add(observer)

    def removeObserver(self, observer):
        self._observers.remove(observer)

    def notify(self):
        for o in self._observers:
            o.update()


class Observer(abc.ABC):
    @abc.abstractmethod
    def update(self):
        pass
