class Parser:
    # LL(1) - functions
    # FIRST, FOLLOW

    grammar = None
    first_dict = {}
    follow_dict = {}

    def __init__(self, grammar):
        self.grammar = grammar

    def initialize_first(self):
        """
        Function to initialize the values of F0 for all the nonterminals.
        It adds empty set [] corresponding to the nonterminal in first_dictionary
        if the nonterminal doesn't have any terminal on the first positions
        otherwise, it adds in the first dictionary to the nonterminal the corresponding value of a list
        containing all the initial values of first.
        """
        nonterminals = self.grammar.set_of_nonterminals
        terminals = self.grammar.set_of_terminals

        for nonterminal in nonterminals:
            values_list = self.grammar.get_rhs_symbols_for_nonterminal(nonterminal)
            for value in values_list:
                if value[0] in terminals:
                    if nonterminal not in self.first_dict.keys():
                        self.first_dict[nonterminal] = [value[0]]
                    else:
                        if value[0] not in self.first_dict[nonterminal]:
                            self.first_dict[nonterminal].append(value[0])
                else:
                    self.first_dict[nonterminal] = []

    @staticmethod
    def concatenate_elements(list_to_concat):
        """
        Computes the first of the elements from the given list:
        ex: list = [ [a,E], [b,c], [g] ] => the returned value will be [a, b, c]
        """
        if list_to_concat == ['E']:
            return ['E']

        first_elem = list_to_concat[0]
        if not first_elem:
            return []

        if 'E' not in first_elem:
            return first_elem

        new_list = []
        for elem in first_elem:
            if elem != 'E':
                new_list.append(elem)

        for elem in list_to_concat[1]:
            if elem != 'E':
                new_list.append(elem)

        return new_list

    def first(self):
        """
        Function which computes the FIRST.
        It initializes the fist_dictionary and then recompute it until we have the same value twice.
        """
        nonterminals = self.grammar.set_of_nonterminals
        terminals = self.grammar.set_of_terminals

        # Initialize the first_dictionary
        self.initialize_first()

        current_first = self.first_dict

        # Initialize the new first with the empty dictionary
        new_first = {}

        while True:
            # Parse all the nonterminals, recompute the first and add it to the dictionary
            for nonterminal in nonterminals:
                # Get the symbols on the rhs of the productions starting from current nonterminal
                values_list = self.grammar.get_rhs_symbols_for_nonterminal(nonterminal)

                # Initialize the list of values for FIRST with the previous ones
                new_list = []

                for elem in current_first[nonterminal]:
                    new_list.append(elem)

                # For each symbol in the list of rhs symbols, get the firsts and concatenate them
                for value in values_list:
                    all_values_to_concatenate = []
                    for char in value:
                        if char in terminals:
                            all_values_to_concatenate.append(char)
                        else:
                            # S -> AB => we need to compute F1(S) = F0(S) U F0(A) (+) F0(B)
                            all_values_to_concatenate.append(current_first[char])

                    # here we need to perform the concatenation between the elements of all_values_to_concatenate and
                    # and then unite the result with the previous result

                    concatenation_result = self.concatenate_elements(all_values_to_concatenate)
                    for elem in concatenation_result:
                        if elem not in new_list:
                            new_list.append(elem)

                new_first[nonterminal] = new_list

            if new_first != current_first:
                current_first = new_first
            else:
                print("FIRST is: ", new_first)
                self.first_dict = current_first
                break

    def initialize_follow(self):
        """
        Function to initialize the values of L0 for all the nonterminals.
        It adds empty set [] corresponding to the nonterminals in first_dictionary
        and adds epsilon E in the dictionary for the starting symbol
        """
        nonterminals = self.grammar.set_of_nonterminals

        for nonterminal in nonterminals:
            if nonterminal == self.grammar.start_symbol:
                self.follow_dict[nonterminal] = ['E']
            else:
                self.follow_dict[nonterminal] = []

    def follow(self):
        """
        Function which computes the FOLLOW.
        It initializes the follow_dictionary and then recompute it until we have the same value twice.
        """

        self.initialize_follow()

        nonterminals = self.grammar.set_of_nonterminals
        terminals = self.grammar.set_of_terminals

        current_follow = self.follow_dict
        new_follow = {}

        while True:
            # Parse all the nonterminals, recompute the follow and add it to the dictionary
            for nonterminal in nonterminals:
                # Initialize the new_list with the previous elements which are not []
                new_list = []
                if self.follow_dict[nonterminal]:
                    for elem in current_follow[nonterminal]:
                        if elem:
                            new_list.append(elem)

                # Get all the productions having the current nonterminal on the rhs
                productions = self.grammar.get_productions_containing_nonterminal(nonterminal)
                # print("productions for ", nonterminal, " are: ")

                # Parse each production and get the symbols containing the nonterminal
                for production in productions:
                    if nonterminal in production.ending_symbol:
                        value = production.ending_symbol
                        # Check if there are more occurrences of that nonterminal in the current value
                        if value.count(nonterminal) >= 1:
                            index = -1
                            while value[index + 1:].count(nonterminal) >= 1:
                                # Then get the index of the nonterminal and check if there is anything following it
                                index = value.find(nonterminal, index + 1)
                                if index + 1 == len(value):
                                    # if is the last one, we need to compute: L1(S) = L0(S) U L0(start_symbol)
                                    last_follow_of_start_symbol = current_follow[production.starting_symbol]
                                    last_follow_of_nonterminal = current_follow[nonterminal]
                                    for elem in last_follow_of_nonterminal:
                                        if elem not in new_list and elem != []:
                                            new_list.append(elem)

                                    for elem in last_follow_of_start_symbol:
                                        if elem not in new_list and elem != []:
                                            new_list.append(elem)

                                elif value[index + 1] in terminals:
                                    next_value = value[index + 1]
                                    # if the next is a terminal, it will be the follow so we add it
                                    if next_value not in new_list:
                                        new_list.append(next_value)
                                else:
                                    next_value = value[index + 1]
                                    # if the next is a nonterminal, return the first of it
                                    first = self.first_dict[next_value]
                                    if 'E' in first:
                                        # If epsilon is in the First, we need to compute also L2(D)..
                                        follow_to_add = current_follow[production.starting_symbol]
                                        if follow_to_add:
                                            for elem in follow_to_add:
                                                if elem not in new_list and elem != []:
                                                    new_list.append(elem)
                                    if first:
                                        for elem in first:
                                            if elem not in new_list and elem != [] and elem != 'E':
                                                new_list.append(elem)

                new_follow[nonterminal] = new_list

            if new_follow != current_follow:
                current_follow = new_follow
            else:
                print("FOLLOW is: ", new_follow)
                self.follow_dict = new_follow
                break
