class ClientOptions:

    def __init__(self, client, redo=1):
        self.client = client
        self.redo = redo

    def __repr__(self):
        return self.client.vehicle
