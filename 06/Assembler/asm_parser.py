from command import Command


class Parser:
    def __init__(self, file: str):
        with open(file) as f:
            self.command_list = [s.strip() for s in f.readlines()]
        self.n: int = 0
        self.current_command = ""

    def has_more_commands(self) -> bool:
        return self.n + 1 <= len(self.command_list)

    def advance(self) -> None:
        self.current_command = self.command_list[self.n].replace(" ", "").split("//")[0]
        self.n += 1

    def command_type(self) -> Command:
        if not self.current_command:
            return Command.NONE
        # if self.current_command[0] == "/" and self.current_command[1] == "/":
        #     return Command.COMMENT
        if self.current_command[0] == "@":
            return Command.A_COMMAND
        if self.current_command[0] == "(":
            return Command.L_COMMAND
        if "=" in self.current_command or ";" in self.current_command:
            return Command.C_COMMAND
        raise Exception("invalid command")

    def symbol(self) -> str:
        if self.current_command[0] == "@":
            return self.current_command[1:]
        elif self.current_command[0] == "(":
            return self.current_command[1 : len(self.current_command)-1]
        else:
            raise Exception("not a or l command")

    def dest(self) -> str:
        if "=" in self.current_command:
            return self.current_command.split("=")[0]
        else:
            return None

    def comp(self):
        comp = self.current_command
        if "=" in comp:
            comp = comp.split("=")[1]
        if ";" in comp:
            comp = comp.split(";")[0]
        return comp

    def jump(self):
        if ";" not in self.current_command:
            return None
        jump = self.current_command
        if "=" in jump:
            jump = jump.split("=")[1]
        jump = jump.split(";")[1]
        return jump
