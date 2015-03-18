class Experiment(object):
    def __init__(self, x=None):
        self.x = x

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value


e = Experiment(1)
print e.x
