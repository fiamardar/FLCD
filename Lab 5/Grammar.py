from Production import Production


class Grammar:
    """
    Definition: A (formal) grammar is a 4-tuple: G=(N,Σ,P,S)
    with the following meanings:
    • N – set of nonterminal symbols and |N| < ∞
            o ex:  A,B,C,... – nonterminal symbols
    • Σ - set of terminal symbols (alphabet) and |Σ|<∞
            o ex: a,b,c,... ∈ Σ – terminal symbol
    • S ∈ N – start symbol/axiom
            o ex: S ∈ N – start symbol
    • P – finite set of productions (rules), with the propriety: P⊆(N∪Σ)∗ N(N∪Σ)∗ X(N∪Σ)∗


    Remarks :
    1. (α,β)∈P is a production denoted α→β
    2. N ∩ Σ = ∅

    """
    file = None
    set_of_terminals = []
    set_of_nonterminals = []
    start_symbol = None
    set_of_productions = []

    def __init__(self, fa_file):
        self._file = fa_file
        self.read_file()

    def read_file(self):
        """
        Reads line by line the content of the file and initialize the fields
        """
        with open(self._file, 'r') as file:
            line_nr = 0

            for line in file:
                line_nr += 1

                if line_nr == 1:
                    for nonterminal in line.split():
                        self.set_of_nonterminals.append(nonterminal)

                elif line_nr == 2:
                    for terminal in line.split():
                        self.set_of_terminals.append(terminal)

                elif line_nr == 3:
                    for element in line.split():
                        self.start_symbol = element

                else:
                    production_line_elems = line.split()
                    print(production_line_elems)
                    values_list = []
                    for value in range(2, len(production_line_elems), 2):
                        values_list.append(production_line_elems[value])
                    production = Production(production_line_elems[0], values_list)
                    self.set_of_productions.append(production)

    def get_rhs_symbols_for_nonterminal(self, nonterminal):
        """
        Returns the set of symbol values for a given nonterminal

        :param: nonterminal - the starting symbol of the productions
        :return: the list of symbols
        """
        for production in self.set_of_productions:
            if production.starting_symbol == nonterminal:
                return production.values_list

    def get_productions_containing_nonterminal(self, nonterminal):
        """
        Returns the set of productions having on the rhs a given nonterminal

        :param: nonterminal - the symbol to have on the rhs
        :return: the list of productions
        """
        productions = []
        for production in self.set_of_productions:
            for value in production.values_list:
                if nonterminal in value:
                    productions.append(production)
        return productions

    def cfg_check(self):
        """
        Function checks if the grammar is CFG.
        It is accepted if:
            1. All the starting symbols from all the productions are nonterminals
            2. All the values from the list of symbols for each production are terminals or nonterminals

        :return: True, if the grammar is CFG, False otherwise
        """
        for production in self.set_of_productions:
            if production.starting_symbol not in self.set_of_nonterminals:
                return False

            for symbol in production.values_list:
                for char in symbol:
                    if char not in self.set_of_terminals and char not in self.set_of_nonterminals:
                        return False
        return True
