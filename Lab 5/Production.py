class Production:
    starting_symbol = None
    values_list = []

    def __init__(self, starting_symbol, values_list):
        self.starting_symbol = starting_symbol
        self.values_list = values_list

    def __str__(self):
        string = self.starting_symbol + " -> ";
        for value in self.values_list:
            string += value + " | "
        return string[:-2]
