class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def parse(self):
        return self.statement()

    def statement(self):
        if self.match("VAR"):
            return self.assignment()
        elif self.match("STRING"):
            return self.string()
        elif self.match("ID"):
            return self.operation()
        else:
            raise Exception("Invalid statement")

    def assignment(self):
        name = self.consume("ID").value
        self.consume("EQUALS")
        value = self.expression()
        return ("ASSIGN", name, value)

    def string(self):
        return ("STRING", self.consume("STRING").value)

    def operation(self):
        left = self.consume("ID").value
        operator = self.consume("OP").value
        right = self.expression()
        return (operator, left, right)

    def expression(self):
        if self.match("ID"):
            return self.consume("ID").value
        elif self.match("NUMBER"):
            return self.consume("NUMBER").value
        elif self.match("STRING"):
            return self.string()
        else:
            raise Exception("Invalid expression")

    def match(self, token_type):
        if self.index >= len(self.tokens):
            return False
        return self.tokens[self.index].type == token_type

    def consume(self, token_type):
        if not self.match(token_type):
            raise Exception(
                f"Expected {token_type} but got {self.tokens[self.index].type}"
            )
        return self.tokens[self.index + 1]


print(Parser("VAR a").consume(""))
