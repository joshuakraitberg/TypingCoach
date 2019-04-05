from typing_coach.util import Subject, Observer
from typing_coach.constants import KeyStates


class PhraseBuilder(Subject, Observer):
    def __init__(self, phrase, logger):
        Subject.__init__(self)
        self._phrase = phrase
        self._logger = logger
        self._len = len(phrase)
        self._pos = 0
        self._bad = 0
        self._good = 0
        self._states = [KeyStates.NONE] * self._len
        self._states[0] = KeyStates.CURSOR

    @property
    def phrase(self):
        return self._phrase

    @property
    def logger(self):
        return self._logger

    @property
    def states(self):
        return self._states

    @property
    def good(self):
        return self._good

    @property
    def bad(self):
        return self._bad

    def is_full(self):
        return self._pos == self._len

    def is_correct(self):
        return self._good == self._len

    def add(self, key):
        # Remove key
        if key == '\b':
            if self._pos:
                if key == self._phrase[self._pos]:
                    self._good -= 1
                else:
                    self._bad -= 1
                self._states[self._pos] = KeyStates.NONE
                self._pos -= 1
                self._states[self._pos] = KeyStates.CURSOR

        # Add key
        elif self._pos < self._len:
            if key == self._phrase[self._pos]:
                self._states[self._pos] = KeyStates.CORRECT
                self._good += 1
            else:
                self._states[self._pos] = KeyStates.INCORRECT
                self._bad += 1
            self._pos += 1
            if self._pos < self._len:
                self._states[self._pos] = KeyStates.CURSOR

    def update(self):
        i, k, t = self._logger.last()
        self.add(k)
        self.notify()
