from Transition import Transition


class FiniteAutomata:
    """
    Definition: A finite automaton (FA) is a 5-tuple
    M = (Q,Σ,δ,q0,F) where:
    • Q - finite set of states (|Q|<∞) ex: Q = {q0, q1, q2}  => the line contains: q0,q1,q2
    • Σ - finite alphabet (|Σ|<∞)      ex: ∑ = {0, 1}        => the line contains: 0,1
    • q0 – initial state q0 ∊ Q        ex: q0 = {q0}         => the line contains: q0
    • F⊆Q – set of final states        ex: F = {q2}          => the line contains: q2
    • δ – transition function : δ:Q×Σ→P(Q)
        • we will read from file line by line the transitions
                    ex: q0 ->(1) q1    => the line contains: q0,q1,1 (initial state, final state, value)

    """
    _file = None
    _set_of_states = []
    _alphabet = []
    _initial_state = None
    _set_of_final_states = []
    _set_of_transitions = []

    def __init__(self, fa_file):
        self._file = fa_file
        self.read_file()

    def get_set_of_states(self):
        return self._set_of_states

    def get_alphabet(self):
        return self._alphabet

    def get_initial_state(self):
        return self._initial_state

    def get_set_of_final_states(self):
        return self._set_of_final_states

    def get_transitions(self):
        return self._set_of_transitions

    def read_file(self):
        """
        Reads line by line the content of the file
        """
        with open(self._file, 'r') as file:
            line_nr = 0

            for line in file:
                line_nr += 1

                if line_nr == 1:
                    for state in line.split():
                        self._set_of_states.append(state)

                elif line_nr == 2:
                    for element in line.split():
                        self._alphabet.append(element)

                elif line_nr == 3:
                    for element in line.split():
                        self._initial_state = element

                elif line_nr == 4:
                    for state in line.split():
                        self._set_of_final_states.append(state)

                else:
                    elements = line.split()
                    transition = Transition(elements[0], elements[1], elements[2])
                    self._set_of_transitions.append(transition)

    def get_corresponding_transition(self, initial_state, value):
        """
        Returns the transition which has the initial state and the value specified
        :param initial_state: The state from which the transition starts
        :param value: The value symbol of the transitions
        :return: The corresponding transition if found, None otherwise
        """
        corresponding_transition = None

        for transition in self._set_of_transitions:
            if transition.get_initial_state() == initial_state and transition.get_value() == value:
                corresponding_transition = transition
                break

        return corresponding_transition

    def check_sequence(self, sequence):
        """
        Function checks if a sequence is accepted by the FA.
        It is accepted if and only if the last state of the sequence is also one of the final states
        and if the input is empty (if we find corresponding transitions for all the elements in the sequence)

        :param sequence: The sequence we want to check
        :return: True, if the sequence is accepted by the FA, False otherwise
        """
        # First set the current state to the initial state
        current_state = self._initial_state

        # Parse the sequence character by character
        for character in sequence:

            # returns the transition which goes from current state with current value
            transition = self.get_corresponding_transition(current_state, character)

            if transition is None:
                return False

            current_state = transition.get_final_state()

        if current_state in self._set_of_final_states:
            return True

        return False
