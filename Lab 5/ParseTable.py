from tabulate import tabulate


class ParseTable:
    grammar = None
    first = None
    follow = None
    table = {}

    def __init__(self, grammar, first, follow):
        self.grammar = grammar
        self.follow = follow
        self.first = first
        self.populate_table()

    def print_table(self):
        print()
        columns = ['X']
        for terminal in self.grammar.set_of_terminals:
            columns.append(terminal)
        columns.append('$')
        lines = self.grammar.set_of_nonterminals
        for terminal in columns:
            if terminal != 'E' and terminal != 'X':
                lines.append(terminal)

        table_elems = []
        for line_elem in lines:
            line = [line_elem]
            for column_elem in columns:
                if column_elem != 'X':
                    if (line_elem, column_elem) in self.table.keys():
                        line.append(self.table[(line_elem, column_elem)])
                    else:
                        line.append('')
            table_elems.append(line)

        print(tabulate(table_elems, headers=columns))

        print()

    def populate_table(self):
        for non_terminal in self.grammar.set_of_nonterminals:
            # luam toate productions care pleaca din nonterminal si pentru fiecare ending symbol verificam daca
            # in FIRST(ending) exista terminal sau daca rhs e EPSILON
            symbols = self.grammar.get_rhs_symbols_for_nonterminal(non_terminal)

            for symbol in symbols:
                if symbol == 'E':
                    follow_non_terminal = self.follow[non_terminal]

                    for value in follow_non_terminal:
                        prod_nr = self.grammar.get_production_number_for_production(non_terminal, symbol)
                        if value == 'E':
                            self.table[(non_terminal, '$')] = ('E', prod_nr)
                        else:
                            self.table[(non_terminal, value)] = ('E', prod_nr)
                else:
                    prod_nr = self.grammar.get_production_number_for_production(non_terminal, symbol)

                    if symbol[0] in self.grammar.set_of_terminals:
                        self.table[(non_terminal, symbol[0])] = (symbol, prod_nr)
                    else:
                        for terminal in self.grammar.set_of_terminals:
                            if terminal != 'E':

                                if terminal in self.first[symbol[0]]:
                                    self.table[(non_terminal, terminal)] = (symbol, prod_nr)

        for terminal in self.grammar.set_of_terminals:
            self.table[(terminal, terminal)] = 'pop'

        self.table[('$', '$')] = 'acc'

        print(self.table)
        self.print_table()

    def run(self):
        w = 'a+a*a'
        input_stack = w + '$'
        working_stack = self.grammar.start_symbol + '$'
        output_stack = []

        while True:
            a = input_stack[0]
            A = working_stack[0]

            if (A, a) in self.table.keys():
                value_tuple = self.table[(A, a)]

                if value_tuple == 'pop':
                    input_stack = input_stack[1:]
                    working_stack = working_stack[1:]
                elif value_tuple == 'acc':
                    print("ACCEPTED!")
                    print(output_stack)
                    return output_stack
                else:
                    prod_number = value_tuple[1]
                    replacing_symbol = value_tuple[0]
                    output_stack.append(prod_number)

                    working_stack = working_stack[1:]

                    if replacing_symbol != 'E':
                        working_stack = replacing_symbol + working_stack

            else:
                print("Error found: at (" + A + ", " + a + ")")
                print("Current working stack: ", working_stack)
                print("Current output stack: ", output_stack)
                return None
