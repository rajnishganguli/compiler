#!/usr/bin/python
import ply.yacc as yacc
import os
import sys
from sys import argv
from Lexer import tokens
import re
import derivation as drv

def p_start(p):
    '''start : expression_statements'''

def p_expression_statements_1(p):
    '''expression_statements : expression start'''

def p_expression_statements_2(p):
    '''expression_statements : expression'''

def p_expression_math_1(p):
    '''expression : IDENTIFIER OP_ASGN rightside'''

def p_expression_math_3(p):
    '''expression : jump_statements'''
  
def p_jump_statements(p):
    '''jump_statements :  KEYWORD_BREAK
                       | KEYWORD_NEXT '''

def p_math_rightside_1(p):
    '''rightside : TYPE_NUMERIC math rightside
                 | TYPE_INTEGER math rightside   
                 | IDENTIFIER math rightside'''

def p_math_rightside_2(p):
    '''rightside : vector'''

def p_math(p):
    '''math : OP_PLUS
            | OP_MINUS
            | OP_MULT
            | OP_DIVIDE
            | OP_EXPO
            | OP_REMDR'''

def p_vector_1(p):
    '''vector : any_type '''

def p_vector_2(p):
    '''vector : TYPE_NUMERIC SEP_COLON TYPE_NUMERIC'''

def p_any_type_1(p):
    '''any_type : TYPE_NUMERIC'''

def p_any_type_2(p):
    '''any_type : TYPE_INTEGER '''

def p_any_type_3(p):
    '''any_type : TYPE_STRING '''

def p_any_type_4(p):
    '''any_type : TYPE_BOOLEAN '''

def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()
script, data = argv
sys.stderr = open('parser_output.txt', 'w')
fp = open(os.path.abspath(data),"r")
result = parser.parse(fp.read(),debug=1)
fp.close()
sys.stderr.close()
drv.make_html(data)