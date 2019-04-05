from typing_coach.util import tepoc, Subject


class KeyLogger(Subject):
    def __init__(self):
        Subject.__init__(self)
        self._last = None
        self._count = 0
        self._keys = []
        self._times = []

    def __len__(self):
        return self._count

    def __iter__(self):
        for k, t in zip(self._keys, self._times):
            yield k, t

    @property
    def keys(self):
        return self._keys

    @property
    def times(self):
        return self._times

    def count(self):
        return self._count

    def last(self):
        return self._last

    def get(self, item):
        return self._keys[item], self._times[item]

    def log(self, key, time=tepoc):
        t = time()
        i = self._count
        self._keys.append(key)
        self._times.append(t)
        self._count += 1
        self._last = i, key, t
        self.notify()

