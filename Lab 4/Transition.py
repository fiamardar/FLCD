class Transition:
    initial_state = None
    final_state = None
    value = None

    def __init__(self, initial_state, final_state, value):
        self.initial_state = initial_state
        self.final_state = final_state
        self.value = value

    def get_initial_state(self):
        return self.initial_state

    def get_final_state(self):
        return self.final_state

    def get_value(self):
        return self.value

    def __str__(self):
        return "δ(" + self.initial_state + ", " + self.value + ") = " + self.final_state
