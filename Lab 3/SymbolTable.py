class SymbolTable:
    _elements = {}

    @staticmethod
    def hash_code(object_to_hash):
        return sum(bytearray(object_to_hash, encoding='utf8'))

    def get_elements(self):
        return self._elements

    def search(self, element_to_search):
        """
        Whenever an element is to be searched, compute the hash code of the key passed and locate the element using that
        hash code.
        :return: False - if the element wasn't found
        :return: hash_code - the hash code of the element in case it is the only one associated with it
        :return: (hash_code, index) - the tuple representing the key in the dictionary of elements and also the
                                      position in the list of values for that key (hash code)
        """
        # get the hash code of the element
        hash_code = self.hash_code(element_to_search)

        # Check if the key exists in the dictionary
        if hash_code not in self._elements.keys():
            return False
        else:
            # If it does exist, there are two possibilities: the value is an element or a list
            result = self._elements[hash_code]

            if type(result) is list:
                # If it is a list, check if the element we are looking for is in the list
                if element_to_search in result:
                    # And return the tuple of key and index
                    return hash_code, result.index(element_to_search)
            else:
                # Else, check if the element associated with the key is the one we are searching for
                if result == element_to_search:
                    # And return the key (the hash code)
                    return hash_code

            # If the element wasn't found at the key, return false
            return False

    def add(self, element_to_add):
        """
        Whenever an element is to be inserted, compute the hash code of the key passed and locate the index using
        that hash code as an index in the array.
        :param element_to_add: The element we want to add
        :return: hash_code - the hash code of the element in case it is the only one associated with it
        :return: (hash_code, index) - the tuple representing the key in the dictionary of elements and also the
                                      position in the list of values for that key (hash code)
        """

        # get the hash code of the element
        hash_code = self.hash_code(element_to_add)

        # Check if the key exists in the dictionary
        if hash_code not in self._elements.keys():
            # If it doesn't exist in the dictionary, we add it and return the key
            self._elements[hash_code] = element_to_add
            return hash_code
        else:
            # If it does exist, there are two possibilities: the value is an element or a list
            result = self._elements[hash_code]

            if type(result) is list:
                # If it is a list, check if the element we are looking for is in the list
                if element_to_add in result:
                    # And return the tuple of key and index
                    return hash_code, result.index(element_to_add)
                else:
                    # Else add it to the end of the list of elements associated with that hash code
                    result.append(element_to_add)
                    # And return the tuple of key and index
                    return hash_code, result.index(element_to_add)
            else:
                # If there is only one element associated with the hash code, check if it is the one we want to add
                if result == element_to_add:
                    # And return the key (the hash code)
                    return hash_code
                else:
                    # Else, transform the value into a list containing both elements
                    list_elements = [result, element_to_add]
                    self._elements[hash_code] = list_elements
                    # And return the tuple of key and index
                    return hash_code, list_elements.index(element_to_add)

    def delete(self, element_to_delete):
        """
        Whenever an element is to be deleted, compute the hash code of the key passed and locate the index using that
        hash code as an index in the array.
        :param element_to_delete: The element we want to remove from the SymbolTable
        :return: None - if the element doesn't exist in the ST
        :return: hash_code - the hash code of the element deleted
        """
        # get the hash code of the element
        hash_code = self.hash_code(element_to_delete)

        # Check if the key exists in the dictionary
        if hash_code in self._elements.keys():
            # If it does exist, there are two possibilities: the value is an element or a list
            result = self._elements[hash_code]

            if type(result) is list:
                # If it is a list, check if the element we are looking for is in the list
                if element_to_delete in result:
                    # If the element is in the list of values, we delete it and return the hash code
                    self._elements[hash_code].remove(element_to_delete)
                    return hash_code
            else:
                # If there is only one element associated with the hash code, check if it is the one we want to delete
                if result == element_to_delete:
                    # Then delete it and return the hash code
                    del self._elements[hash_code]
                    return hash_code

        # If it doesn't exist in the SymbolTable, return None
        return None

    def __str__(self):
        return self._elements.__str__()
