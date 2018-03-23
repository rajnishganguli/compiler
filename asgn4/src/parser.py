#!/usr/bin/python
import ply.yacc as yacc
import os
import sys
from sys import argv
import lexer
from lexer import tokens
import re
import TAC as tac
import SymbolTable as st

filename = sys.argv[1]

def p_program(p):
    '''program : start'''
    TAC.emit('EndOfCode', [])
def p_start(p):
    '''start : expression_statements'''
    p[0] = p[1]
def p_expression_statements_1(p):
    '''expression_statements : expression start'''
    p[0] = [p[1]] + p[2]

def p_expression_statements_2(p):
    '''expression_statements : expression'''
    p[0] = p[1]

def p_expression_math_1(p):
    '''expression : IDENTIFIER OP_ASGN rightside'''
    var_dict = ST.varlookup(p[1])
    if(var_dict == False):
        var_dict = globalST.varlookup(p[1])
        if (var_dict == False):
            ST.varinsert(p[1], {"type":p[3]['type'], "declare": True})
            var_dict = {"type":p[3]['type'], "declare": True}
    TAC.emit('Assignment', [p[1], p[3]['place']])
    p[0] = {"place":p[1], "type": var_dict["type"]} 

def p_expression_math_2(p):
    '''expression : rightside
                  | jump_statements'''
    p[0] = p[1]

def p_jump_statements(p):
    '''jump_statements :  KEYWORD_BREAK
                       | KEYWORD_NEXT '''
    p[0] = p[1]

def p_math_rightside_1(p):
    '''rightside : TYPE_NUMERIC math rightside'''
    if(p[3]["type"] != "num"):
        print("TYPE ERROR: variable", p[1],'and',p[3], 'not matching type.')
    temp_name = ST.newtemp({"type" : "num"})
    TAC.emit('Arithmetic',[p[2],temp_name,p[1],p[3]["place"]])
    p[0] = {"place": temp_name, "type": p[3]["type"]}

def p_math_rightside_2(p):
    '''rightside : any_type'''
    p[0] = p[1]

def p_math(p):
    '''math : OP_PLUS
            | OP_MINUS
            | OP_MULT
            | OP_DIVIDE
            | OP_EXPO
            | OP_REMDR'''
    p[0] = p[1]

def p_any_type_1(p):
    '''any_type : TYPE_NUMERIC'''
    temp_name = ST.newtemp({"type":"num"})
    TAC.emit('Assignment', [temp_name, p[1]])
    p[0] = {"place": temp_name, "type": "num"} 

def p_any_type_2(p):
    '''any_type : TYPE_INTEGER'''
    temp_name = ST.newtemp({"type":"int"})
    TAC.emit('Assignment', [temp_name, p[1]])
    p[0] = {"place": temp_name, "type": "int"}        

def p_any_type_3(p):
    '''any_type : TYPE_STRING'''
    temp_name = ST.newtemp({"type":"str"})
    TAC.emit('Assignment', [temp_name, p[1]])
    p[0] = {"place": temp_name, "type": "str"} 

def p_any_type_4(p):
    '''any_type : TYPE_BOOLEAN'''
    temp_name = ST.newtemp({"type":"bool"})
    TAC.emit('Assignment', [temp_name, p[1]])
    p[0] = {"place": temp_name, "type": "bool"}

def p_error(p):
    print("Syntax error in input!")



no_special_reg = 0
globalST = st.Symtable("global")

localST = st.Symtable("local")

ST = globalST

myfile = open(filename,'r')
inputArray = myfile.readlines()
myfile.close()
ldata = ""
for i in range(0,len(inputArray)):
    ldata = ldata + inputArray[i]

lexer.lexer.input(ldata)



yacc.yacc()
pdata = ""
myfile = open(filename,'r')
for line in myfile.readlines():
    if line!='\n':
        pdata = pdata + line

TAC = tac.TAC()

result = yacc.parse(pdata)
print "global symboltable";
print ST.vardict
print ST.funcdict
if (TAC.error == False):
    TAC.printTAC()