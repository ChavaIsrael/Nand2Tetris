
class CodeWriter:

    def __init__(self, path):
        # Open the output asm file
        self.__output_file = open(path, 'w')
        # Save the file name to use in the static segment push/pop:
        self.__file_name = path.replace('.asm', '').split('\\')[-1]
        # Count the num of comparision commands in order to create different labels names:
        self.__count_comparisons = 0

    def __write_add(self):
        """Write add command"""
        add_code = ['@SP\n', 'M=M-1;\n', 'A=M;\n', 'D=M;\n', 'A=A-1;\n', 'M=M+D;\n']
        self.__output_file.writelines(add_code)

    def __write_sub(self):
        """Write sub command"""
        sub_code = ['@SP\n', 'M=M-1;\n', 'A=M;\n', 'D=M;\n', 'A=A-1;\n', 'M=M-D;\n']
        self.__output_file.writelines(sub_code)

    def __write_neg(self):
        """Write neg command"""
        neg_code = ['@SP\n', 'A=M-1;\n', 'M=-M;\n']
        self.__output_file.writelines(neg_code)

    def __write_eq(self):
        """Write eq command"""
        eq_code = ['@SP\n', 'M=M-1;\n', 'A=M;\n', 'D=M;\n', 'A=A-1;\n', 'D=M-D;\n', f"@EQ{self.__count_comparisons}\n", "D;JEQ\n", "@SP\n", 'A=M-1;\n' "M=0;\n", f"@END{self.__count_comparisons}\n", "D;JMP\n", f"(EQ{self.__count_comparisons})\n", "@SP\n", 'A=M-1;\n' "M=-1;\n", f"(END{self.__count_comparisons})\n"]
        self.__output_file.writelines(eq_code)
        self.__count_comparisons += 1  # Advance the comparision counter.

    def __write_gt(self):
        """Write gt command"""
        gt_code = ['@SP\n', 'M=M-1;\n', 'A=M;\n', 'D=M;\n', 'A=A-1;\n', 'D=M-D;\n', f"@GT{self.__count_comparisons}\n", "D;JGT\n", "@SP\n", 'A=M-1;\n' "M=0;\n", f"@END{self.__count_comparisons}\n", "D;JMP\n", f"(GT{self.__count_comparisons})\n", "@SP\n", 'A=M-1;\n' "M=-1;\n", f"(END{self.__count_comparisons})\n"]
        self.__output_file.writelines(gt_code)
        self.__count_comparisons += 1  # Advance the comparision counter.

    def __write_lt(self):
        """Write lt command"""
        lt_code = ['@SP\n', 'M=M-1;\n', 'A=M;\n', 'D=M;\n', 'A=A-1;\n', 'D=M-D;\n', f"@LT{self.__count_comparisons}\n", "D;JLT\n", "@SP\n", 'A=M-1;\n' "M=0;\n", f"@END{self.__count_comparisons}\n", "D;JMP\n", f"(LT{self.__count_comparisons})\n", "@SP\n", 'A=M-1;\n' "M=-1;\n", f"(END{self.__count_comparisons})\n"]
        self.__output_file.writelines(lt_code)
        self.__count_comparisons += 1  # Advance the comparision counter.

    def __write_not(self):
        """Write not command"""
        not_code = ['@SP\n', 'A=M-1;\n', 'M=!M;\n']
        self.__output_file.writelines(not_code)

    def __write_or(self):
        """Write or command"""
        or_code = ['@SP\n', 'M=M-1;\n', 'A=M;\n', 'D=M;\n', 'A=A-1;\n', 'M=M|D;\n']
        self.__output_file.writelines(or_code)

    def __write_and(self):
        """Write and command"""
        and_code = ['@SP\n', 'M=M-1;\n', 'A=M;\n', 'D=M;\n', 'A=A-1;\n', 'M=M&D;\n']
        self.__output_file.writelines(and_code)

    def write_arithmetic(self, command):
        """Get arithmetic command and write it to the output file"""
        command_function = {
            "add": self.__write_add,
            "sub": self.__write_sub,
            "neg": self.__write_neg,
            "eq": self.__write_eq,
            "gt": self.__write_gt,
            "lt": self.__write_lt,
            "not": self.__write_not,
            "or": self.__write_or,
            "and": self.__write_and,
        }

        # Send to the
        command_function[command]()

    def write_push_pop(self, command, segment, index):
        """Get push/pop command and write it to the output file"""
        # Saved pointers:
        saved_pointers = {
            "local": 'LCL',
            "argument": 'ARG',
            "this": 'THIS',
            "that": 'THAT'
        }
        code = []
        # Handling the different segment types:
        if segment in saved_pointers:
            if command == 'C_PUSH':
                code = [f'@{saved_pointers[segment]}\n', 'D=M;\n', f'@{index}\n', 'A=D+A;\n', 'D=M;\n', '@SP\n', 'A=M;\n', 'M=D;\n', '@SP\n', 'M=M+1;\n']
            else:
                code = [f'@{saved_pointers[segment]}\n', 'D=M;\n', f'@{index}\n', 'D=D+A;\n', '@R13\n', 'M=D;\n', '@SP\n', 'M=M-1;\n', 'A=M;\n', 'D=M;\n', '@R13\n', 'A=M;\n', 'M=D;\n']
        if segment == 'temp':
            if command == 'C_PUSH':
                code = [f'@{5+index}\n', 'D=M;\n', '@SP\n', 'A=M;\n', 'M=D;\n', '@SP\n', 'M=M+1;\n']
            else:
                code = ['@SP\n', 'M=M-1;\n', 'A=M;\n', 'D=M;\n', f'@{5+index}\n', 'M=D;\n']
        if segment == 'constant':
            if command == 'C_PUSH':
                code = [f'@{index}\n', 'D=A;\n', '@SP\n', 'A=M;\n', 'M=D;\n', '@SP\n', 'M=M+1;\n']
        if segment == "pointer":
            if command == 'C_PUSH':
                code = [f'@R{3+index}\n', 'D=M;\n', '@SP\n', 'A=M;\n', 'M=D;\n', '@SP\n', 'M=M+1;\n']
            else:
                code = [f'@R{3+index}\n', 'D=A;\n', '@R13\n', 'M=D;\n', '@SP\n', 'M=M-1;\n', 'A=M;\n', 'D=M;\n', '@R13\n', 'A=M;\n', 'M=D;\n']
        if segment == 'static':
            if command == 'C_PUSH':
                code = [f'@{self.__file_name}.{index}\n', 'D=M;\n', '@SP\n', 'A=M;\n', 'M=D;\n', '@SP\n', 'M=M+1;\n']
            else:
                code = [f'@{self.__file_name}.{index}\n', 'D=A;\n', '@R13\n', 'M=D;\n', '@SP\n', 'M=M-1;\n', 'A=M;\n', 'D=M;\n', '@R13\n', 'A=M;\n', 'M=D;\n']

        # Write the push/pop code to the output file:
        self.__output_file.writelines(code)

    def close(self):
        """Close output file"""
        self.__output_file.close()
