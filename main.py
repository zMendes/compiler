#!/usr/bin/python

import sys


class Token:

    def __init__(self, type_, value):
        self.type_ = type_
        self.value = value


class PrePro:

    def filter(self, text):
        
        # Implemnentação baseada a partir do código abaixo:
        # https://www.geeksforgeeks.org/remove-comments-given-cc-program/
        isComment = False

        filteredText = ""
        i = 0
        while (i < len(text)):
            if isComment and text[i] == "*" and text[i+1] == "/":
                isComment = False
                i += 1
            elif text[i] == "/" and text[i+1] == "*":
                isComment = True
                i += 1
            elif isComment:
                i += 1
                continue
            else:
                filteredText += text[i]
            i += 1

        if isComment:
            raise KeyError
        return filteredText


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
            self.actual = Token("MULTI", None)

        elif self.origin[self.position] == "/":
            self.actual = Token("DIV", None)

        elif self.origin[self.position] == " ":
            self.selectNext()

        else:
            raise ValueError


class Parser:

    def parseTerm(self):
        result = self.tokens.actual.value

        self.tokens.selectNext()

        if self.tokens.actual.type_ == "INT":
            raise ValueError

        while self.tokens.actual.type_ == "MULTI" or self.tokens.actual.type_ == "DIV":

            if self.tokens.actual.type_ == "MULTI":
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

    def parseExpression(self):

        if self.tokens.actual.type_ == "INT":
            result = self.parseTerm()

            while self.tokens.actual.type_ == "PLUS" or self.tokens.actual.type_ == "SUB":

                if self.tokens.actual.type_ == "PLUS":
                    self.tokens.selectNext()
                    if self.tokens.actual.type_ == "INT":
                        result += self.parseTerm()
                    else:
                        raise ValueError

                if self.tokens.actual.type_ == "SUB":
                    self.tokens.selectNext()
                    if self.tokens.actual.type_ == "INT":
                        result -= self.parseTerm()
                    else:
                        raise ValueError

                # self.tokens.selectNext()
                # if self.tokens.actual.type_ == "INT":
                 #   raise ValueError
            return result
        else:
            raise ValueError

    def run(self, code):
        prepro = PrePro()
        filtered = prepro.filter(code)
        self.tokens = Tokenizer(filtered, -1, None)
        self.tokens.selectNext()
        return self.parseExpression()


if __name__ == "__main__":
    parser = Parser()
    command = " ".join(sys.argv[1:])
    print(parser.run(command))
