#!/usr/bin/python
import ply.yacc as yacc
import os
import sys
from sys import argv
# Get the token map from the lexer.  This is required.
from Lexer import tokens
import re
import derivation as drv

def p_program(p):
    '''program : start'''
############################################################# POSSIBLE STARTS ###############################
def p_start_1(p):
    '''start : expression_statements'''

def p_start_2(p):
    '''start : loop_statements'''

def p_start_3(p):
    '''start : functions_statements '''  

def p_start_4(p):
    '''start : conditional_statements '''      

############################################################# EXPRESSION STATEMENTS ########################
def p_expression_statements_1(p):
    '''expression_statements : expression start'''

def p_expression_statements_2(p):
    '''expression_statements : expression'''

############################################################# LOOP STATEMENTS #############################
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


############################################################# FUNCTION STATEMENTS ############################
def p_functions_statements_1(p):
    '''functions_statements : function_definition start '''
        
def p_functions_statements_2(p):
    '''functions_statements : function_definition '''
        
def p_functions_statements_3(p):
    '''functions_statements : function_call start '''
            
# def p_functions_statements_4(p):
#     '''functions_statements : function_call '''

############################################################## FUNCTION DEFINITION #######################################
def p_function_definition(p):
    '''function_definition : IDENTIFIER OP_ASGN KEYWORD_FUNCTION BR_LCIR arg_list BR_RCIR compound_statement'''

def p_arg_list_definition_1(p):
    '''arg_list : arg_list SEP_COMMA argument'''
        
def p_arg_list_definition_2(p):
    '''arg_list : argument'''

def p_argument_definition_1(p):
    '''argument : IDENTIFIER OP_ASGN any_type'''
        
def p_argument_definition_2(p):
    '''argument : IDENTIFIER'''
        
def p_argument_definition_3(p):
    '''argument : '''

############################################################### FUNCTION CALLING ###########################
def p_function_call(p):
    '''function_call : IDENTIFIER BR_LCIR arg_to_pass BR_RCIR'''

def p_arg_to_pass_1(p):
    '''arg_to_pass : arg_to_pass SEP_COMMA arg'''

def p_arg_to_pass_2(p):
    '''arg_to_pass : arg'''

def p_arg(p):
    '''arg : rightside'''

############################################################## CONDITIONAL STATEMENTS ######################
def p_conditional_statements_1(p):
    '''conditional_statements : if_else_statement start '''
        
def p_conditional_statements_2(p):
    '''conditional_statements : if_else_statement '''
        
def p_conditional_statements_3(p):
    '''conditional_statements : if_statement start '''
        
def p_conditional_statements_4(p):
    '''conditional_statements : if_statement'''

########################################################### IF ELSE STATEMENTS ###############################
def p_if_else_statement_definition_1(p):
    '''if_else_statement : KEYWORD_IF BR_LCIR if_cond BR_RCIR compound_statement KEYWORD_ELSE if_else_statement '''
        
def p_if_else_statement_definition_2(p):
    '''if_else_statement : KEYWORD_IF BR_LCIR if_cond BR_RCIR compound_statement KEYWORD_ELSE compound_statement '''

def p_if_statement_definition(p):
    '''if_statement : KEYWORD_IF BR_LCIR if_cond BR_RCIR compound_statement '''
        
def p_compound_statement_1(p):
    '''compound_statement : BR_LCUR statement_list BR_RCUR '''
        
def p_compound_statement_2(p):
    '''compound_statement :  statement '''
        
def p_statement_list_1(p):
    '''statement_list : statement_list statement'''
        
def p_statement_list_2(p):
    '''statement_list : statement'''
        
def p_statement_definition_1(p):
    '''statement : expression'''
                
def p_statement_definition_3(p):
    '''statement : for_loop'''
        
def p_statement_definition_4(p):
    '''statement : while_loop'''
        
def p_statement_definition_5(p):
    '''statement : if_statement'''

############################################################# COMPARISON STATEMENTS ########################

def p_comparison_statement_1(p):
    '''comparison_statement :  IDENTIFIER compop any_type '''

def p_comparison_statement_1_1(p):
    '''comparison_statement :  IDENTIFIER compop IDENTIFIER '''

def p_comparison_statement_2(p):
    '''comparison_statement :  any_type compop any_type'''

def p_comparison_statement_3(p):
    '''comparison_statement : BR_LCIR if_cond BR_RCIR '''


############################################################# IF CONDITION ###################################

def p_if_cond_1(p):
    '''if_cond :  TYPE_BOOLEAN'''

def p_if_cond_2(p):
    '''if_cond :  comparison_statement'''

def p_if_cond_3(p):
    '''if_cond : comparison_statement logop if_cond '''
        
def p_if_cond_4(p):
    '''if_cond : comparison_statement bitop if_cond '''

def p_if_cond_5(p):
    '''if_cond : OP_BITNOT if_cond '''

############################################################# LOGICAL OPERATOR #############################
def p_logop_1(p):
    '''logop : OP_LOGAND '''
        
def p_logop_2(p):
    '''logop : OP_LOGOR '''

############################################################# BITWISE OPERATOR ##############################
def p_bitop_1(p):
    '''bitop : OP_BITAND '''
        
def p_bitop_2(p):
    '''bitop : OP_BITOR '''

############################################################# EXPRESSION TYPES #############################

def p_expression_math_1(p):
    '''expression : IDENTIFIER OP_ASGN rightside'''

def p_expression_math_2(p):
    '''expression : rightside'''

def p_expression_math_3(p):
    '''expression : jump_statements'''
      
def p_expression_math_4(p):
    '''expression : KEYWORD_PRINT BR_LCIR rightside BR_RCIR  '''    

def p_expression_math_5(p):
    '''expression : KEYWORD_RETURN BR_LCIR rightside BR_RCIR  '''
  
############################################################ JUMP STATEMENTS #############################  
def p_jump_statements_1(p):
    '''jump_statements :  KEYWORD_BREAK '''
        
def p_jump_statements_2(p):
    '''jump_statements :  KEYWORD_NEXT '''

########################################################### RIGHTSIDE ######################################
def p_math_rightside_1(p):
    '''rightside : TYPE_NUMERIC math rightside '''

def p_math_rightside_2(p):
    '''rightside : TYPE_INTEGER math rightside '''
    
def p_math_rightside_3(p):
    '''rightside : IDENTIFIER math rightside '''
        
def p_math_rightside_4(p):
    '''rightside : BR_LCIR rightside BR_RCIR '''
        
def p_math_rightside_5(p):
    '''rightside : any_type bitop rightside '''
        
def p_math_rightside_6(p):
    '''rightside : any_type logop rightside '''

def p_math_rightside_8(p):
    '''rightside : IDENTIFIER bitop rightside '''

def p_math_rightside_9(p):
    '''rightside : IDENTIFIER logop rightside '''

def p_math_rightside_10(p):
    '''rightside : IDENTIFIER '''

def p_math_rightside_11(p):
    '''rightside : any_type '''

def p_math_rightside_12(p):
    '''rightside : function_call '''

def p_math_rightside_13(p):
    '''rightside : IDENTIFIER BR_LCSR IDENTIFIER BR_RCSR'''

def p_math_rightside_14(p):
    '''rightside : IDENTIFIER BR_LCSR TYPE_INTEGER BR_RCSR'''

def p_math_rightside_15(p):
    '''rightside : IDENTIFIER BR_LCSR KEYWORD_VECTOR_CONSTRUCTOR BR_LCIR arg_to_pass BR_RCIR BR_RCSR'''

def p_math_rightside_16(p):
    '''rightside : vector_definition'''

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
    '''vector_definition : TYPE_NUMERIC SEP_COLON TYPE_NUMERIC'''

def p_vector_2(p):
    '''vector_definition : KEYWORD_VECTOR BR_LCIR SEP_COMMA TYPE_INTEGER BR_RCIR'''
    
def p_vector_3(p):
    '''vector_definition : KEYWORD_VECTOR BR_LCIR SEP_COMMA IDENTIFIER BR_RCIR'''
    
def p_vector_4(p):
    '''vector_definition : KEYWORD_VECTOR_CONSTRUCTOR BR_LCIR arg_to_pass BR_RCIR'''

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

def p_comop_definition_5(p):
    '''compop : OP_NOEQ'''

def p_comop_definition_6(p):
    '''compop : OP_COMP'''
 
######################################################### ERROR PRODUCTION ##################################

def p_error(p):
    print p
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