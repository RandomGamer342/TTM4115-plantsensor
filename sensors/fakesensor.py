from sensors import sensor
import time


class FakeSensor():
    def __init__(self, id, threshold, timerate, humidity = None):
        self.id = id
        self.threshold = min(max(threshold, 0.), 1.)
        self.timerate = timerate
        self.time = time.time()
        if humidity is None:
            self.humidity = self.threshold
        else:
            self.humidity = min(max(humidity, 0.), 1.)

    def read(self):
        curtime = time.time()
        self.humidity -= max((curtime - self.time) / self.timerate, 0.)
        self.time = curtime
        return self.humidity

    def water(self, fraction=None):
        if fraction is None:
            fraction = self.threshold

        self.humidity = min(max(fraction, 0.), 1.)
        self.time = time.time()
        return self.humidity
