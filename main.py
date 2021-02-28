#!/usr/bin/python

import sys

command = " ".join(sys.argv[1:])#.replace(" ", "")

operator = False
space = False

result = 0
if command[0].isnumeric == False or command[-1].isnumeric() == False:
    if (command[0] != " " or command[-1] != " "):
        raise KeyError

number = "" # command[-1]
start = 0
for i in range(len(command)-1,-1,-1):

    if i != 0 and i!= len(command)-1:    
        if command[i] == " " and command[i-1].isnumeric() and command[i+1].isnumeric():
            raise KeyError
    if command[i].isnumeric():
        number+= command[i]
    if command[i] == "+":
        result += int(number[::-1])
        number = ""
        start = i
    
    if command[i] == "-":
        result -= int(number[::-1])
        number = ""
        start = i

result+= int(number[::-1])
    
print(result)