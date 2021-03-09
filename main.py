#!/usr/bin/python

import sys


class Token:

    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value


class Tokenizer:

    def __init__(self, origin, position, actual):
        self.origin = origin
        self.position = position
        self.actual = actual

    def selectNext(self):

        self.position += 1
        # print(self.origin[self.position])
        if self.position >= len(self.origin):
            self.actual = Token("EOF", None)

        elif self.origin[self.position].isnumeric():
            number = ""
            while self.position < len(self.origin) and self.origin[self.position].isnumeric():
                number += self.origin[self.position]
                self.position += 1
            self.actual = Token("INT", int(number))
            self.position -= 1

        elif self.origin[self.position] == "+":
            self.actual = Token("PLUS", None)

        elif self.origin[self.position] == "-":
            self.actual = Token("SUB", None)

        elif self.origin[self.position] == "*":
            self.actual = Token("MULT", None)

        elif self.origin[self.position] == "/":
            self.actual = Token("DIV", None)

        elif self.origin[self.position] == " ":
            self.selectNext()

        else:
            raise ValueError


class Parser:

    def parseExpression(self):

        if self.tokens.actual.type_ == "INT":

            result = self.tokens.actual.value
            self.tokens.selectNext()
            while self.tokens.actual.type_ == "PLUS" or self.tokens.actual.type_ == "SUB" or self.tokens.actual.type_ == "MULT" or self.tokens.actual.type_ == "DIV":
                
                if self.tokens.actual.type_ == "PLUS":
                    self.tokens.selectNext()
                    if self.tokens.actual.type_ == "INT":
                        result += self.tokens.actual.value
                    else:
                        raise ValueError

                if self.tokens.actual.type_ == "SUB":
                    self.tokens.selectNext()
                    if self.tokens.actual.type_ == "INT":
                        result -= self.tokens.actual.value
                    else:
                        raise ValueError
                
                if self.tokens.actual.type_ == "MULT":
                    self.tokens.selectNext()
                    if self.tokens.actual.type_ == "INT":
                        result *= self.tokens.actual.value
                    else:
                        raise ValueError
                
                if self.tokens.actual.type_ == "DIV":
                    self.tokens.selectNext()
                    if self.tokens.actual.type_ == "INT":
                        result /= self.tokens.actual.value
                    else:
                        raise ValueError
                self.tokens.selectNext()
                if self.tokens.actual.type_ == "INT":
                    raise ValueError
            return result
        else:
            raise ValueError

    def run(self, code):
        self.tokens = Tokenizer(code, -1, None)
        self.tokens.selectNext()
        return self.parseExpression()


if __name__ == "__main__":
    parser = Parser()
    command = " ".join(sys.argv[1:])  # .replace(" ", "")
    print(parser.run(command))
