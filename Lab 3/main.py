
from SymbolTable import SymbolTable
from Scanner import Scanner


def write_message_to_file(message):
    new_file = open("message.out", mode="w", encoding="utf-8")
    new_file.write(message)
    new_file.close()


def write_PIF_to_file(pif):
    new_file = open("PIF.out", mode="w", encoding="utf-8")
    for i in pif:
        new_file.write(str(i))
        new_file.write("\n")
    new_file.close()


def write_ST_to_file(st):
    new_file = open("ST.out", mode="w", encoding="utf-8")
    for i in st.items():
        new_file.write(str(i))
        new_file.write("\n")
    new_file.close()


if __name__ == '__main__':
    symbol_table = SymbolTable()
    file = "token.txt"
    scanner = Scanner(symbol_table, file)

    if not scanner.errors:
        scanner.errors = "Lexically correct"

    print(scanner.get_symbol_table())
    print(scanner.get_pif())
    print(scanner.errors)

    write_ST_to_file(scanner.get_symbol_table().get_elements())
    write_PIF_to_file(scanner.get_pif())
    write_message_to_file(scanner.errors)
