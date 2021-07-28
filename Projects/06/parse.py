
class Parser:

    def __init__(self, path):
        self.path = path
        input_file = open(path, 'r')
        self.instructions = input_file.readlines()
        input_file.close()
        self.line = -1

    def has_more_commands(self):
        return self.line + 1 < len(self.instructions)

    def advance(self):
        self.line += 1
        # Handling comments, '\n', and whitespaces.
        self.instructions[self.line] = self.instructions[self.line].split('//')[0].replace('\n', "").replace(" ", "")
        # Handling empty lines.
        while self.has_more_commands() and self.instructions[self.line] == "":
            self.line += 1
            self.instructions[self.line] = self.instructions[self.line].split('//')[0].replace('\n', "").replace(" ", "")

    def command_type(self):
        if self.instructions[self.line][0] == '(':
            return 'L_COMMAND'
        if self.instructions[self.line][0] == '@':
            return 'A_COMMAND'
        return 'C_COMMAND'

    def symbol(self):
        # Label:
        if self.instructions[self.line][0] == '(':
            return self.instructions[self.line][1:-1]
        # A instruction:
        return self.instructions[self.line][1:]

    def dest(self):
        return self.instructions[self.line].split('=')[0] \
            if self.instructions[self.line].find('=') >= 0 else "null"

    def comp(self):
        return self.instructions[self.line].split('=')[1].split(';')[0] \
            if self.instructions[self.line].find('=') >= 0 \
            else self.instructions[self.line].split(';')[0]

    def jump(self):
        return self.instructions[self.line].split(';')[1] \
            if self.instructions[self.line].find(';') >= 0 else "null"
