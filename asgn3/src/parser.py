#!/usr/bin/python
import ply.yacc as yacc
import os
import sys
from sys import argv
# Get the token map from the lexer.  This is required.
from Lexer import tokens
import re
import derivation as drv

############################################################# POSSIBLE STARTS ###############################
def p_start_1(p):
    '''start : expression_statements'''

def p_start_2(p):
    '''start : loop_statements'''

############################################################# EXPRESSION STSTEMENTS ########################

def p_expression_statements_1(p):
    '''expression_statements : expression start'''

def p_expression_statements_2(p):
    '''expression_statements : expression'''

############################################################# POSSIBLE LOOP STATEMENTS #######################

def p_loop_statements_1(p):
    '''loop_statements : while_loop start'''
    
def p_loop_statements_2(p):
    '''loop_statements : while_loop'''
    
def p_loop_statements_3(p):
    '''loop_statements : for_loop start'''
    
def p_loop_statements_4(p):
    '''loop_statements : for_loop'''
    
############################################################# LOOPS #########################################    

def p_for_loop(p):
    '''for_loop : KEYWORD_FOR BR_LCIR IDENTIFIER KEYWORD_IN IDENTIFIER BR_RCIR compound_statement'''
    
def p_while_loop(p):
    '''while_loop : KEYWORD_WHILE BR_LCIR if_cond BR_RCIR compound_statement'''

############################################################# IF CONDITION #########################################

def p_if_cond_1(p):
    '''if_cond :  TYPE_BOOLEAN'''

def p_if_cond_2(p):
    '''if_cond :  comparison_statement'''

#######################################################

def p_comparison_statement_1(p):
    '''comparison_statement :  IDENTIFIER compop any_type '''

def p_comparison_statement_2(p):
    '''comparison_statement :  any_type compop any_type'''

############################################################# COMPOUND STATEMENTS ##########################

def p_compound_statement(p):
    '''compound_statement :  BR_LCUR expression BR_RCUR'''

############################################################# EXPRESSION TYPES #############################

def p_expression_math_1(p):
    '''expression : IDENTIFIER OP_ASGN rightside'''

def p_expression_math_2(p):
    '''expression : rightside'''

def p_expression_math_3(p):
    '''expression : jump_statements'''
  
def p_jump_statements(p):
    '''jump_statements :  KEYWORD_BREAK
                       | KEYWORD_NEXT'''

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
    '''vector : any_type'''

def p_vector_2(p):
    '''vector : TYPE_NUMERIC SEP_COLON TYPE_NUMERIC'''

########################################################## ANY_TYPE ########################################
def p_any_type_1(p):
    '''any_type : TYPE_NUMERIC'''

def p_any_type_2(p):
    '''any_type : TYPE_INTEGER'''

def p_any_type_3(p):
    '''any_type : TYPE_STRING'''

def p_any_type_4(p):
    '''any_type : TYPE_BOOLEAN'''

########################################################### COMPARISON ###############################3############

def p_comop_definition_1(p):
    '''compop : OP_GREAT'''

def p_comop_definition_2(p):
    '''compop : OP_LESS'''
    
def p_comop_definition_3(p):
    '''compop : OP_LEEQ'''
    
def p_comop_definition_4(p):
    '''compop : OP_GREQ'''
 
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