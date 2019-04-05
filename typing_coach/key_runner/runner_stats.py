import time



class KeyRunnerStats(KeyRunnerConsumer):
    """Contains key states, used to build pretty colour text"""

    def __init__(self, phrase):
        KeyRunnerConsumer.__init__(self, phrase)
        self.index = 0
        self.backlog = 0
        self.previous_time = None
        self.keys = []
        self.delay = []
        self.valid_keys = []

    def consume(self, key):
        t = time.time()
        if key == '\b':
            if self.backlog > 0:
                self.backlog -= 1
            elif self.index > 0:
                self.index -= 1
        elif (self.index + self.backlog) < self.phrase_len:
            if key == self.phrase[self.index]:
                self.index += 1
                self.valid_keys.append(len(self.keys))
            else:
                self.backlog += 1
        elif key == '\r' or key == '\n':
            return True

        self.keys.append(key)
        self.delay.append(t - self.previous_time if self.previous_time else 0)
        self.previous_time = t
        return False

    def get_cpm(self):
        t = sum(self.delay)
        return len(self.keys) / t * 60 if t else 0

    def get_real_cpm(self):
        t = sum(self.delay)
        return len(self.valid_keys) / t * 60 if t else 0
