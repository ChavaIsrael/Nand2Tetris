
import sys
from symbols import SymbolsTable
from parse import Parser
from code import dest, comp, jump


def main():
    # The address to start declare new variables:
    new_address = 16
    # Counter for the num of command lines:
    instruction_num = 0

    first_parser = Parser(sys.argv[1])
    symbol_table = SymbolsTable()

    # Handling labels.
    while first_parser.has_more_commands():
        # Go to the next instruction (parser.line begins from -1)
        first_parser.advance()
        if first_parser.command_type() == 'L_COMMAND':
            symbol = first_parser.symbol()
            symbol_table.add_entry(symbol, instruction_num)
            # We count only command lines.
            instruction_num -= 1
        instruction_num += 1

    # Creating the output hack file.
    output_file = sys.argv[1].split('.asm')[0] + '.hack'
    hack_code = open(output_file, 'a')

    second_parser = Parser(sys.argv[1])

    while second_parser.has_more_commands():
        # Go to the next instruction (parser.line begins from -1)
        second_parser.advance()

        if second_parser.command_type() == 'A_COMMAND':
            symbol = second_parser.symbol()
            # A instruction using numbers:
            if symbol.isdigit():
                bin_num = bin(int(symbol)).split('b')[1]
                hack_code.write("0" * (16 - len(bin_num)) + bin_num + '\n')
            else:
                # Handling variables:
                if not symbol_table.contains(symbol):
                    symbol_table.add_entry(symbol, new_address)
                    new_address += 1
                # Translating the command to binary value and writing it:
                address = symbol_table.get_address(symbol)
                bin_num = bin(address).split('b')[1]
                hack_code.write("0" * (16 - len(bin_num)) + bin_num + '\n')

        if second_parser.command_type() == 'C_COMMAND':
            dst = second_parser.dest()
            cmp = second_parser.comp()
            jmp = second_parser.jump()
            hack_code.write("111" + comp(cmp) + dest(dst) + jump(jmp) + "\n")

    hack_code.close()


if __name__ == '__main__':

    main()
