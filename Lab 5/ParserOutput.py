from Node import Node
from tabulate import tabulate


def get_parent_index(table_tree, production):
    parent_index = 0
    for node in table_tree:
        if node.info == production.starting_symbol:
            parent_index = node.index

    return parent_index


class ParserOutput:
    parsing_tree = None
    grammar = None
    productions_string = ""
    tree_table = None

    def __init__(self, parsing_tree, grammar):
        self.grammar = grammar
        self.parsing_tree = parsing_tree
        self.transform_into_representation()
        self.transform_into_representation_table_father_sibling()

    def transform_into_representation(self):
        for prod_nr in self.parsing_tree:
            self.productions_string += str(prod_nr)

        print("The output representation - productions string is: ", self.productions_string)

    def print_table(self):
        columns = ['index', 'info', 'parent', 'left sibling']
        lines = []
        for node in self.tree_table:
            line = [node.index, node.info, node.parent, node.sibling]
            lines.append(line)

        print("Tree table is:")
        print(tabulate(lines, headers=columns))

    def transform_into_representation_table_father_sibling(self):
        """
        Function to transform the parsing tree (represented as productions string - a list of production numbers)
        into table (using father and sibling relation)
        """
        tree_table = []

        root = Node(1, self.grammar.start_symbol, 0, 0)  # index, info, parent, sibling
        tree_table.append(root)

        current_index = 1
        current_node = root
        parent_index = 0
        for prod_nr in self.parsing_tree:
            sibling_index = 0
            # get the production with the current number
            production = self.grammar.get_production_for_prod_number(prod_nr)

            parent_index = get_parent_index(tree_table, production)
            for symbol in production.ending_symbol:
                current_index += 1
                if sibling_index == 0:
                    new_node = Node(current_index, symbol, parent_index, sibling_index)
                    sibling_index = current_index
                else:
                    new_node = Node(current_index, symbol, parent_index, sibling_index)
                    sibling_index += 1
                tree_table.append(new_node)

        self.tree_table = tree_table
        self.print_table()
