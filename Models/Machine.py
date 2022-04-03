class Machine:

    def __init__(self, name, availabilities):
        self.name = name
        self.availabilities = availabilities

    def __repr__(self):
        return self.name
