import re


class Scanner:
    _reserved_words = ["start", "end", "number", "read", "print", "if", "fi", "else",
                       "string", "for", "rof", "list", "char", "root", "while", "elihw",
                       "space", "tab", "newline", "integer"]
    _operators = ['+', '-', '*', '/', '^', '=', "gt", "lt", "eq", "geqt", "leqt", "<-", "and", "or", "not"]
    _separators = ['[', ']', '{', '}', '(', ')', ':', ';', ',', '"', '\'', ' ', '\t', '\n']
    _symbol_table = {}
    integer_FA = None
    identifier_FA = None
    pif = []  # list of tuples
    errors = ""
    file = None
    current_line = 0

    def __init__(self, symbol_table, filename, integer_FA, identifier_FA):
        self._symbol_table = symbol_table
        self.file = filename
        self.integer_FA = integer_FA
        self.identifier_FA = identifier_FA
        self.read_words_from_file()

    def get_pif(self):
        """
        Returns the PIF of the scanner
        :return: PIF
        """
        return self.pif

    def get_symbol_table(self):
        """
        Returns the Symbol Table of the scanner
        :return: Symbol Table
        """

        return self._symbol_table

    def get_error_string(self):
        """
        Returns the error string of the scanner
        :return: error string
        """
        return self.errors

    def is_operator(self, token):
        """
        Checks if the given token is operator
        :param token: The given token
        :return: True, if it is operator, False otherwise
        """
        if token in self._operators:
            return True
        return False

    def is_separator(self, token):
        """
        Checks if the given token is separator
        :param token: The given token
        :return: True, if it is separator, False otherwise
        """
        if token in self._separators:
            return True
        return False

    def is_reserved_word(self, token):
        """
        Checks if the given token is reserved word
        :param token: The given token
        :return: True, if it is reserved word, False otherwise
        """
        if token in self._reserved_words:
            return True
        return False

    def is_constant(self, token):
        """
        Checks if the given token is constant
        :param token: The given token
        :return: True, if it is constant, False otherwise
        """
        # if re.search("^(-?[1-9]+[0-9]*|0)$", token):
        if self.integer_FA.check_sequence(token):
            return True
        return False

    def is_identifier(self, token):
        """
        Checks if the given token is identifier
        :param token: The given token
        :return: True, if it is identifier, False otherwise
        """
        # if re.search("^[a-zA-Z]+([-_]*[a-zA-Z]*[0-9]*)*$", token):
        if self.identifier_FA.check_sequence(token):
            return True
        return False

    @staticmethod
    def is_function(token):
        """
        Checks if the given token is a function surrounded by parentheses ex: root(x)
        :param token: The token we want to check
        :return: False, if the token is not a function
        :return: If is true, returns a list containing all the elements from the function
        """

        if re.search("^\(*(root|sqrt)\([a-zA-Z0-9_-]*\)+$", token):
            separators_before = []
            separators_after = []
            if re.search("^\(*(root|sqrt)\(+[a-zA-Z0-9_-]*\)+$", token):
                function_name_index = re.search("(root|sqrt)", token).span()  # only the function name

                for i in range(0, function_name_index[0]):
                    separators_before.append(token[i])

                function_name = token[function_name_index[0]: function_name_index[1]]

                first_p = token[function_name_index[1]]

                p = -1
                for i in range(function_name_index[1], len(token)):
                    if token[i] == ")":
                        p = i
                        break

                identifier = token[function_name_index[1] + 1: p]

                for i in range(p, len(token)):
                    separators_after.append(token[i])

                return separators_before, function_name, first_p, identifier, separators_after

        return False

    @staticmethod
    def is_negative_number(token):
        """
        Checks if the given token is a negative number surrounded by parentheses
        :param token: The token we want to check
        :return: False, if the token is not a negative number
        :return: If is true, returns a list containing the constant on the first position
                             and the list of separators which surround the constant
        """
        if re.search("^\(+-[1-9][0-9]*\)+$", token):
            separators_before = []
            separators_after = []
            if re.search("^\(+-[1-9][0-9]*\)+$", token):

                res = re.search("-[1-9][0-9]*", token)  # only the - and digits
                constant = token[res.span()[0]: res.span()[1]]

                for i in range(0, res.span()[0]):
                    separators_before.append(token[i])

                for i in range(res.span()[1], len(token)):
                    separators_after.append(token[i])

                return constant, separators_before, separators_after

        return False

    @staticmethod
    def is_unsplitted_token(token):
        """
        Checks if the given token is unsplitted
        :param token: The given token
        :return: True, if it is unsplitted, False otherwise
        """
        if re.search("^[,[a-zA-Z0-9](,?[a-zA-Z0-9_-]*[,;]?)*([a-zA-Z0-9]+[;])?(]|]:|:)?$", token):
            return True
        return False

    @staticmethod
    def split_word_operator(token):
        """
        Split the token of the template word-operator/separator
        :param token: The token we want to split
        :return: List with the split elements
        """
        x = re.search("^[0-9a-zA-Z][_a-zA-Z0-9]*", token)
        list_of_letters = list(token)
        first_word_list = []
        second_word_list = []
        first_word = ""
        second_word = ""
        for i in range(x.span()[0], x.span()[1]):
            first_word_list.append(list_of_letters[i])
            first_word = "".join(first_word_list)
        for i in range(x.span()[1], len(list_of_letters)):
            second_word_list.append(list_of_letters[i])
            second_word = "".join(second_word_list)

        return [first_word, second_word]

    @staticmethod
    def split_operator_word(token):
        """
        Split the token of the template operator/separator-word
        :param token: The token we want to split
        :return: List with the split elements
        """
        x = re.search("[a-zA-Z]+$", token)
        first_word = ""
        second_word = ""
        list_of_letters = list(token)
        first_word_list = []
        second_word_list = []
        for i in range(0, x.span()[0]):
            first_word_list.append(list_of_letters[i])
            first_word = "".join(first_word_list)
        for i in range(x.span()[0], len(list_of_letters)):
            second_word_list.append(list_of_letters[i])
            second_word = "".join(second_word_list)

        return [first_word, second_word]

    def check_line_for_strings(self, line):
        """
        Function which checks if the given line contains string.
        In this case, we split the line and parse the tokens, detecting them and adding to ST and PIF
        :param line: The line we want to check
        :return: False, if it doesn't contain strings
        """
        strings = re.findall("\"[^\"']*\"", line)
        if len(strings) == 0:
            return False

        opened_quote = False
        string_id = 0
        while string_id < len(strings):
            new_line = line.split()
            for word in new_line:

                # check if the word opens and closes the quotes
                if re.search("^\".*\"$", word):
                    self.pif.append(("constant", word))

                # check if the word contains " as first character
                elif re.search("^\".*$", word) and opened_quote is False:
                    # if it contains it, add the string to the ST and PIF
                    self.pif.append(("constant", self.get_st_position(strings[string_id])))
                    opened_quote = True

                # check if the word contains " -> to close the first one
                elif re.search("^.*\".*$", word) and opened_quote is True:
                    split_word = word.split("\"")
                    if len(split_word) > 1:
                        for i in range(1, len(split_word)):
                            self.detect_token(split_word[i])
                    string_id += 1
                    opened_quote = False

                elif opened_quote is False:
                    self.detect_token(word)

    def get_st_position(self, token):
        """
        Return the position of the token from the ST if it already exists
        otherwise add it first and then return the position
        :param token: The token we want to get the position for
        :return: The position of the token in ST
        """
        search_result = self._symbol_table.search(token)
        if search_result:
            return search_result
        # It doesn't exist in the ST, we need to add it
        return self._symbol_table.add(token)

    def read_words_from_file(self):
        """
        Reads line by line the content of the file and detect the tokens
        :return: None
        """
        with open(self.file, 'r') as file:
            for line in file:
                self.current_line += 1
                if self.check_line_for_strings(line) is False:
                    for word in line.split():
                        self.detect_token(word)

    def detect_token(self, word):
        """
        Functions which detects the tokens by calling the defined functions,
        and performs the operations corresponding to the scanner: completing the ST and PIF
        :param word: The token
        :return: None
        """
        # first check if it is a word with only letters or we need to split it
        if self.is_operator(word) or self.is_separator(word):
            self.pif.append((word, 0))

        elif self.is_constant(word):  # if it is constant
            st_result = self.get_st_position(word)
            self.pif.append(("constant", st_result))

        elif self.is_reserved_word(word):  # if it is a reserved word
            self.pif.append((word, 0))

        elif self.is_identifier(word):  # if it is an identifier
            st_result = self.get_st_position(word)
            self.pif.append(("identifier", st_result))

        elif self.is_function(word):  # if it is a function
            result = self.is_function(word)
            separators_before = result[0]
            function_name = result[1]
            first_p = result[2]
            identifier = result[3]
            separators_after = result[4]

            for i in separators_before:
                self.pif.append((i, 0))

            self.pif.append((function_name, 0))

            self.pif.append((first_p, 0))

            st_result = self.get_st_position(identifier)
            self.pif.append(("identifier", st_result))

            for i in separators_after:
                self.pif.append((i, 0))

        elif self.is_negative_number(word):  # if it is a negative number
            result = self.is_negative_number(word)
            constant = result[0]
            operators_before = result[1]
            operators_after = result[2]

            for i in operators_before:
                self.pif.append((i, 0))

            st_result = self.get_st_position(constant)
            self.pif.append(("constant", st_result))

            for i in operators_after:
                self.pif.append((i, 0))

        elif self.is_unsplitted_token(word):  # if we need to split it
            x = re.search("^[0-9a-zA-Z].*$", word)
            try:
                if x:
                    result = self.split_word_operator(word)
                    self.detect_token(result[0])
                    for char in list(result[1]):
                        self.detect_token(char)
                elif re.search("[a-zA-Z]$", word):
                    result = self.split_operator_word(word)
                    for res in result:
                        self.detect_token(res)
            except UnboundLocalError:
                self.errors += "Lexical Error at line " + str(self.current_line) + " at " + word + "\n"
            except TypeError:
                self.errors += "Lexical Error at line " + str(self.current_line) + " at " + word + "\n"
            except RecursionError:
                self.errors += "Lexical Error at line " + str(self.current_line) + " at " + word + "\n"

        else:
            self.errors += "Lexical Error at line " + str(self.current_line) + " at " + word + "\n"
