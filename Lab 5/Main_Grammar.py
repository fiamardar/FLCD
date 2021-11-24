from Grammar import Grammar
from Parser import Parser


def print_menu():
    print("\nFor displaying the elements of the FA in file, press: \n"
          "0. Exit\n"
          "1. Set of nonterminals\n"
          "2. Set of terminals\n"
          "3. Set of productions\n"
          "4. Productions for a given nonterminal\n"
          "5. CFG check\n"
          "6. Get FIRST and FOLLOW\n")


if __name__ == '__main__':

    grammar = Grammar("g4.txt")

    while True:
        print_menu()
        result = int(input())

        if result == 1:
            print("The set of nonterminals: ", grammar.set_of_nonterminals)
        elif result == 2:
            print("The set of terminals: ", grammar.set_of_terminals)
        elif result == 3:
            print("The set of productions: ")
            for production in grammar.set_of_productions:
                print(production)
        elif result == 4:
            print("Enter the nonterminal: ")
            nonterminal = input()
            print("The productions for the given nonterminal are: ")
            print(grammar.get_rhs_symbols_for_nonterminal(nonterminal))
        elif result == 5:
            print("Grammar is CFG: ", grammar.cfg_check())
        elif result == 6:
            parser = Parser(grammar)
            parser.first()
            parser.follow()
        elif result == 0:
            break
        else:
            print("Incorrect value! Please try again")
