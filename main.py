#!/usr/bin/python

import sys
from abc import ABCMeta, abstractmethod
import copy

class SymbolTable:

    def __init__(self):
        self.table = dict()
    
    def setVar(self, var, value):
        self.table[var] = value
    
    def getVar(self, var):
        return self.table[var]

sb = SymbolTable()

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

class BSt(Node):
    children = list
    value = int
    
    def __init__(self):
        self.children = []

    def Evaluate(self):
        for child in self.children:
            child.Evaluate()

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

class Print(Node):
    children = list
    value = int
    def __init__(self):
        self.children = [None]
    
    def Evaluate(self):
        print(self.children[0].Evaluate())

class Variable(Node):
    
    children = list
    value = int

    def __init__(self, value):
        self.value = value
        self.children = []
    
    def Evaluate(self):
        return sb.getVar(self.value)

class NoOp(Node):
    
    children = list
    value = int

    def __init__(self):
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
        self.invalid = ["(", ")", "/", "*", "-", "+", "=", ";", " "]

    def selectNext(self):

        self.position += 1
        if self.position >= len(self.origin):
            self.actual = Token("EOF", None)
            return
        if self.origin[self.position] == "n":
            self.selectNext()
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
        
        elif self.origin[self.position] == "=":
            self.actual = Token("EQUAL", None)
        
        elif self.origin[self.position] == ";":
            self.actual = Token("SEMICOLON", None)

        elif self.origin[self.position] != " " :
            identifier = ""

            while self.position < len(self.origin)  and self.origin[self.position] not in self.invalid:
                identifier+= self.origin[self.position]
                self.position +=1
            self.position -=1
            if (identifier == "println"):
                self.actual = Token("PRINT", identifier)    
            else:
                self.actual = Token("IDENTIFIER", identifier)

        else:
            self.selectNext()


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

        elif self.tokens.actual.type_ == "IDENTIFIER":
            tree = Variable(self.tokens.actual.value)
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
    
    def parseCommand(self):
        
        if self.tokens.actual.type_ == "IDENTIFIER":
            identifier = self.tokens.actual.value
            self.tokens.selectNext()
            if self.tokens.actual.type_ != "EQUAL":
                raise ValueError("Missing '=' in reference.")
            self.tokens.selectNext()
            value = self.parseExpression()
            sb.setVar(identifier, value.Evaluate())
            tree = Variable(identifier)

        
        elif self.tokens.actual.type_ == "PRINT":
            tree = Print()
            self.tokens.selectNext()
            if self.tokens.actual.type_ != "BRACKET_OPEN":
                raise ValueError("Missing '(' in reference.")
            self.tokens.selectNext()
            exp = self.parseExpression()
            tree.children[0] = exp
            if self.tokens.actual.type_ != "BRACKET_CLOSE":
                raise ValueError("Missing ')' in reference.")
            self.tokens.selectNext()
        
        else:
            tree = NoOp()
        
        if self.tokens.actual.type_ != "SEMICOLON":
            raise ValueError("Missing ';' in reference.")

        self.tokens.selectNext()

        return tree

    def parseBlock(self):

        head = BSt() 
        
        while self.tokens.actual.type_ != "EOF":
            head.children.append(self.parseCommand())

        return head


    def run(self, code):
        prepro = PrePro()
        filtered = prepro.filter("".join(code).replace("\n",""))
        self.tokens = Tokenizer(filtered, -1, None)
        self.tokens.selectNext()
        result = self.parseBlock()
        result.Evaluate()


if __name__ == "__main__":
    parser = Parser()
    file_name = " ".join(sys.argv[1:])
    file = open(file_name, 'r')
    content = file.readlines() 
    parser.run(content)
