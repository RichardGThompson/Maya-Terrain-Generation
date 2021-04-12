import maya.cmds as cmds
import random
import math

variables = ['F']
conditions = ['+', '-', '[', ']']
axiom = 'F'
rules = [['F', 'F+[F+F-F]']]

systemString = axiom

newString = ''

numberOfIterations = 2

for i in range(numberOfIterations):
    for char in systemString:
        for rule in rules:
            if(rule[0] == char):
                newString += rule[1]
                systemString = newString
    print('Iteration number {} result: {}'.format(i, newString))

print('Ruleset Created: {}'.format(newString))
