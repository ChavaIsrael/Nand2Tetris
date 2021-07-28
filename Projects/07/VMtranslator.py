
import sys
from parse import Parser
from codeWriter import CodeWriter


def main():
    """The main function"""
    input_path = sys.argv[1]
    parser = Parser(input_path)

    # Define the path for the output:
    output_path = input_path.split('.vm')[0] + '.asm'

    codewriter = CodeWriter(output_path)

    # Pass over the commands, parse them, and write their translation to the output file
    while parser.has_more_commands():
        # Go to the next instruction (parser.line begins from -1)
        parser.advance()

        # Arithmetic command:
        if parser.command_type() == 'C_ARITHMETIC':
            command = parser.arg1()
            codewriter.write_arithmetic(command)

        # Push/Pop command:
        elif parser.command_type() == 'C_PUSH' or parser.command_type() == 'C_POP':
            segment = parser.arg1()
            index = int(parser.arg2())
            codewriter.write_push_pop(parser.command_type(), segment, index)

    # Close the output file:
    codewriter.close()


if __name__ == '__main__':
    main()
