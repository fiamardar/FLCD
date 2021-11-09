class Transition:
    source_state = None
    destination_state = None
    value = None

    def __init__(self, source_state, destination_state, value):
        self.source_state = source_state
        self.destination_state = destination_state
        self.value = value

    def get_source_state(self):
        return self.source_state

    def get_destination_state(self):
        return self.destination_state

    def get_value(self):
        return self.value

    def __str__(self):
        return "δ(" + self.source_state + ", " + self.value + ") = " + self.destination_state
