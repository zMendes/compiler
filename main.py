#!/usr/bin/python

import sys
from abc import ABCMeta, abstractmethod
import copy



class Node(metaclass=ABCMeta):
    def __init__(self):
        pass
    
    @property
    @abstractmethod
    def value():
        pass

    @property
    @abstractmethod
    def children():
        pass

    @abstractmethod
    def Evaluate(self):
        pass

class BinOp(Node):
    
    children = list
    value = int

    def __init__(self, value):
        self.value = value
        self.children = [None] * 2
    
    def Evaluate(self):
        a = self.children[0].Evaluate()
        b = self.children[1].Evaluate()
        if self.value == "PLUS":
            return a + b
        
        elif self.value == "SUB":
            return a - b

        elif self.value == "MULTI":
            return a * b
        
        elif self.value == "DIV":
            return int(a / b)

class UnOp(Node):
    
    children = list
    value = int

    def __init__(self, value):
        self.value = value
        self.children = [None] 
    
    def Evaluate(self):

        if self.value == "PLUS":
            return self.children[0].Evaluate()
        elif self.value == "SUB":
            return -self.children[0].Evaluate()


class IntVal(Node):
    
    children = list
    value = int

    def __init__(self, value):
        self.value = value
        self.children = [] 
    
    def Evaluate(self):
        return self.value

class NoOp(Node):
    
    children = list
    value = int

    def __init__(self, value):
        self.value = value
        self.children = []
    
    def Evaluate(self):
        pass

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

        elif self.origin[self.position] == "(":
            self.actual = Token("BRACKET_OPEN", None)
        
        elif self.origin[self.position] == ")":
            self.actual = Token("BRACKET_CLOSE", None)

        else:# self.origin[self.position] == " ":
            self.selectNext()

        #else:
        #    print(self.origin[self.position])
        #    raise ValueError


class Parser:

    def parseFactor(self):

        if self.tokens.actual.type_ == "INT":
            tree = IntVal(self.tokens.actual.value)
            self.tokens.selectNext()
        
        elif self.tokens.actual.type_ == "PLUS":
            self.tokens.selectNext()
            tree = UnOp("PLUS")
            tree.children[0] = self.parseFactor() 
        
        elif self.tokens.actual.type_ == "SUB":
            self.tokens.selectNext()
            tree = UnOp("SUB")
            tree.children[0] = self.parseFactor()
        
        elif self.tokens.actual.type_ == "BRACKET_OPEN":
            self.tokens.selectNext()
            tree = self.parseExpression()
            if self.tokens.actual.type_ != "BRACKET_CLOSE":
                raise ValueError
            self.tokens.selectNext()
        
        else:
           raise ValueError
        
        return tree
            



    def parseTerm(self):
        
        tree = self.parseFactor()


        if self.tokens.actual.type_ == "INT":
            raise ValueError

        while self.tokens.actual.type_ == "MULTI" or self.tokens.actual.type_ == "DIV":

            if self.tokens.actual.type_ == "MULTI":
                self.tokens.selectNext()
                aux = BinOp("MULTI")
                aux.children[0] = copy.deepcopy(tree)
                aux.children[1] = self.parseFactor()
                tree = copy.deepcopy(aux)

            if self.tokens.actual.type_ == "DIV":
                self.tokens.selectNext()
                aux = BinOp("DIV")
                aux.children[0] = copy.deepcopy(tree)
                aux.children[1] = self.parseFactor()
                tree = copy.deepcopy(aux)
            
            if self.tokens.actual.type_ == "INT":
                raise ValueError

        return tree

    def parseExpression(self):

            tree = self.parseTerm()

            while self.tokens.actual.type_ == "PLUS" or self.tokens.actual.type_ == "SUB":

                if self.tokens.actual.type_ == "PLUS":
                    self.tokens.selectNext()
                    aux = BinOp("PLUS")
                    aux.children[0] = copy.deepcopy(tree)
                    aux.children[1] = self.parseTerm()
                    tree = copy.deepcopy(aux)

                if self.tokens.actual.type_ == "SUB":
                    self.tokens.selectNext()
                    aux = BinOp("SUB")
                    aux.children[0] = copy.deepcopy(tree)
                    aux.children[1] = self.parseTerm()
                    tree = copy.deepcopy(aux)


            return tree

    def run(self, code):
        prepro = PrePro()
        filtered = prepro.filter("".join(code))
        self.tokens = Tokenizer(filtered, -1, None)
        self.tokens.selectNext()
        result = self.parseExpression()
        if self.tokens.actual.type_ != "EOF":
            raise ValueError
        return result


if __name__ == "__main__":
    parser = Parser()
    file_name = " ".join(sys.argv[1:])
    file = open(file_name, 'r')
    content = file.readlines() 
    print(parser.run(content).Evaluate())
