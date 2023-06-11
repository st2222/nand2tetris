import sys

from asm_parser import Parser
from command import Command
from c_code import Code
from symbol_table import SymbolTable


def main(file: str):
    if file.split(".")[1] != "asm":
        raise Exception()
    file_name = file.split(".")[0]
    parser = Parser(file)
    code = Code()
    symbol_table = SymbolTable()
    address = 0
    a_address = 16
    output_list = []
    while parser.has_more_commands():
        parser.advance()
        match parser.command_type():
            case Command.C_COMMAND | Command.A_COMMAND:
                address += 1
            case Command.L_COMMAND:
                symbol_table.addEntry(parser.symbol(), address)
    second_parser = Parser(file)
    while second_parser.has_more_commands():
        second_parser.advance()
        match second_parser.command_type():
            case Command.C_COMMAND:
                output_list.append(
                    "111"
                    + code.comp(second_parser.comp())
                    + code.dest(second_parser.dest())
                    + code.jump(second_parser.jump())
                )
            case Command.A_COMMAND:
                if not symbol_table.contains(second_parser.symbol()):
                    if str.isdigit(second_parser.symbol()):
                        symbol_table.addEntry(second_parser.symbol(), second_parser.symbol())
                    else:
                        symbol_table.addEntry(second_parser.symbol(), a_address)
                        a_address += 1
                output_list.append(
                    format(int(symbol_table.getAddress(second_parser.symbol())), "016b")
                )
    with open(file_name + ".hack", mode="w") as f:
        f.write("\n".join(output_list))


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 2:
        raise Exception("invalid arg")
    main(sys.argv[1])
