from FiniteAutomata import FiniteAutomata


def print_menu():
    print("\nFor displaying the elements of the FA in file, press: \n"
          "0. Exit\n"
          "1. The set of states\n"
          "2. The alphabet\n"
          "3. The initial state\n"
          "4. The set of final states\n"
          "5. All the transitions\n"
          "6. Check if a sequence is accepted by the FA\n")


if __name__ == '__main__':

    finite_automata = FiniteAutomata("FA_integer.in")

    while True:
        print_menu()
        result = int(input())

        if result == 1:
            print("The set of states: ", finite_automata.get_set_of_states())
        elif result == 2:
            print("The alphabet: ", finite_automata.get_alphabet())
        elif result == 3:
            print("The initial state is: ", finite_automata.get_initial_state())
        elif result == 4:
            print("The set of final states: ", finite_automata.get_set_of_final_states())
        elif result == 5:
            print("All the transitions: ")
            for transition in finite_automata.get_transitions():
                print(transition)
        elif result == 6:
            print("Enter the sequence to check: ")
            sequence = input()
            if finite_automata.check_sequence(sequence):
                print("Yes, the sequence is accepted by the FA")
            else:
                print("No, the sequence is NOT accepted by the FA")
        elif result == 0:
            break
        else:
            print("Incorrect value! Please try again")
