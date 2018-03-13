#!/usr/bin/python
import ply.yacc as yacc
import os
import sys
from sys import argv
from Lexer import tokens
import re
import derivation as drv

############################################################# POSSIBLE STARTS ###############################
def p_start(p):
    '''start : expression_statements'''

############################################################# EXPRESSION STSTEMENTS ########################
def p_expression_statements_1(p):
    '''expression_statements : expression start'''

def p_expression_statements_2(p):
    '''expression_statements : expression'''


############################################################# EXPRESSION TYPES #############################
def p_expression_math_1(p):
    '''expression : IDENTIFIER OP_ASGN rightside'''

def p_expression_math_3(p):
    '''expression : jump_statements'''
  
def p_jump_statements(p):
    '''jump_statements :  KEYWORD_BREAK
                       | KEYWORD_NEXT '''

########################################################### RIGHTSIDE ######################################
def p_math_rightside_1(p):
    '''rightside : TYPE_NUMERIC math rightside
                 | TYPE_INTEGER math rightside   
                 | IDENTIFIER math rightside'''

def p_math_rightside_2(p):
    '''rightside : vector'''

########################################################### MATH OPERATOR ##################################
def p_math_1(p):
    '''math : OP_PLUS '''
        
def p_math_2(p):
    '''math : OP_MINUS '''
        
def p_math_3(p):
    '''math : OP_MULT '''
        
def p_math_4(p):
    '''math : OP_DIVIDE '''
        
def p_math_5(p):
    '''math : OP_EXPO '''
        
def p_math_6(p):
    '''math : OP_REMDR '''


########################################################### VECTOR #########################################
def p_vector_1(p):
    '''vector : any_type '''

def p_vector_2(p):
    '''vector : TYPE_NUMERIC SEP_COLON TYPE_NUMERIC'''



########################################################## ANY_TYPE ########################################
def p_any_type_1(p):
    '''any_type : TYPE_NUMERIC'''

def p_any_type_2(p):
    '''any_type : TYPE_INTEGER '''

def p_any_type_3(p):
    '''any_type : TYPE_STRING '''

def p_any_type_4(p):
    '''any_type : TYPE_BOOLEAN '''


######################################################### ERROR PRODUCTION ##################################
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