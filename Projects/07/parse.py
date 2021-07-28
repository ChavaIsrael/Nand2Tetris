
class Parser:

    def __init__(self, path):
        input_file = open(path, 'r')
        self.instructions = input_file.readlines()  # The commands array.
        input_file.close()
        self.line = -1  # Save the index of the command being reading now.

    def has_more_commands(self):
        """Return true if there is additional command to read, false otherwise"""
        return self.line + 1 < len(self.instructions)

    def advance(self):
        """Advance the line, handling comments and empty lines"""
        self.line += 1
        # Handling comments, '\n', and whitespaces.
        self.instructions[self.line] = self.instructions[self.line].split('//')[0].replace('\n', "")
        # Handling empty lines.
        while self.has_more_commands() and self.instructions[self.line] == "":
            self.line += 1
            self.instructions[self.line] = self.instructions[self.line].split('//')[0].replace('\n', "")

    def command_type(self):
        """Return the type of the current command"""
        arithmetic_commands = ["add", "sub", "neg", "eq", "gt", "lt", "not", "or", "and"]
        other_commands = {
            "push": 'C_PUSH',
            "pop": 'C_POP',
            "function": 'C_FUNCTION',
            "return": 'C_RETURN',
            "if": 'C_IF',
            "goto": 'C_GOTO',
            "call": 'C_CALL',
            "label": 'C_LABEL'
        }
        for arithmetic_command in arithmetic_commands:
            # Arithmetic command:
            if arithmetic_command in self.instructions[self.line]:
                return 'C_ARITHMETIC'
        for other_command in other_commands:
            # Other types
            if other_command in self.instructions[self.line]:
                return other_commands[other_command]

    def arg1(self):
        """Return the first arg of the command"""
        if self.command_type() == 'C_RETURN':
            return None
        if self.command_type() == 'C_ARITHMETIC':
            return self.instructions[self.line]
        return self.instructions[self.line].split(' ')[1]

    def arg2(self):
        """Return the second arg of the command"""
        valid_commands = ['C_PUSH', 'C_POP', 'C_FUNCTION', 'C_CALL']
        if self.command_type() in valid_commands:
            return self.instructions[self.line].split(' ')[2]
