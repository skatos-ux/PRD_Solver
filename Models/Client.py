class Client:

    def __init__(self, vehicle, tasks, availabilities):
        self.vehicle = vehicle
        self.tasks = tasks
        self.availabilities = availabilities

    def __repr__(self):
        return self.vehicle
