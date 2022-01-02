class Production:
    starting_symbol = None
    ending_symbol = None
    production_number = None

    def __init__(self, starting_symbol, ending_symbol, production_number):
        self.starting_symbol = starting_symbol
        self.ending_symbol = ending_symbol
        self.production_number = production_number

    def __str__(self):
        string = self.starting_symbol + " -> " + self.ending_symbol + " (" + self.production_number + ")";
        # for value in self.values_list:
        #     string += value + " | "
        # return string[:-2]
        return string

    def get_production_number(self):
        return self.production_number
