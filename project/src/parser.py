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

def p_start_1(p):
    '''start : expression_statements'''

def p_start_2(p):
    '''start : loop_statements'''

def p_start_3(p):
    '''start : functions_statements '''

def p_start_4(p):
    '''start : conditional_statements '''

def p_start_5(p):
    '''start : '''

def p_expression_statements_1(p):
    '''expression_statements : expression start'''

def p_loop_statements_1(p):
    '''loop_statements : while_loop start'''

def p_loop_statements_2(p):
    '''loop_statements : for_loop start'''

def p_functions_statements_1(p):
    '''functions_statements : function_definition start '''
        
def p_functions_statements_3(p):
    '''functions_statements : function_call start '''

def p_conditional_statements_1(p):
    '''conditional_statements : if_else_statement start '''

def p_conditional_statements_3(p):
    '''conditional_statements : if_statement start '''

def p_if_else_statement_definition_2(p):
    '''if_else_statement : KEYWORD_IF BR_LCIR if_cond BR_RCIR M_1 compound_statement KEYWORD_ELSE M_2 compound_statement M_3'''

def p_if_statement_definition(p):
    '''if_statement : KEYWORD_IF BR_LCIR if_cond BR_RCIR M_1 compound_statement M_3'''

def p_while_loop(p):
    '''while_loop : KEYWORD_WHILE BR_LCIR M_4 if_cond BR_RCIR M_5 compound_statement M_6'''

def p_for_loop(p):
    '''for_loop : KEYWORD_FOR BR_LCIR IDENTIFIER KEYWORD_IN for_range BR_RCIR M_7 compound_statement M_8'''

def p_function_definition_1(p):
    '''function_definition : fname OP_FUNC_ASGN KEYWORD_FUNCTION BR_LCIR arg_list M_10 BR_RCIR compound_statement M_11
    					| fname OP_FUNC_ASGN KEYWORD_FUNCTION BR_LCIR BR_RCIR M_12 compound_statement M_13'''
    global ST
    # print p[1]["fname"]
    # print ST.vardict
    # print ST.funcdict
    global globalST
    ST = globalST
    global localST
    localST = st.Symtable("local")

def p_fname(p):
    '''fname : IDENTIFIER'''
    global no_special_reg
    global localST
    global ST
    ST = localST
    label_name = ST.newlabel()
    TAC.emit("goto", [label_name])
    TAC.emit("flabel", [p[1]])
    p[0] = {"label": label_name,"fname":p[1]}
    no_special_reg = 0

def p_arg_list_definition_1(p):
    '''arg_list : IDENTIFIER M_9 SEP_COMMA arg_list
    			| IDENTIFIER M_9'''
    if(len(p)==3):
        p[0]= [p[1]]
    else:
        p[0]=[p[1]]+ p[4]
def p_M_9(p):
    '''M_9 : '''
    vardict = globalST.varlookup(p[-1])
    if(vardict != False):
        print ("Function Argument cannot be a declared same name as global variable")
    ST.varinsert(p[-1], {"type":"none", "declare":True})

    global no_special_reg
    if(no_special_reg > 3):
        print("no of arguments greater than 4")
    no_special_reg += 1

def p_M_10(p):
    '''M_10 : '''
    global no_special_reg
    no_special_reg = 0
    globalST.funcinsert(p[-5]["fname"],{"num":len(p[-1])})
    for i in reversed(p[-1]):
        TAC.emit("func_arg", [i, no_special_reg])
        no_special_reg += 1

def p_M_12(p):
    '''M_12 : '''
    global no_special_reg
    no_special_reg = 0
    globalST.funcinsert(p[-5]["fname"],{"num":0})

def p_M_11(p):
    '''M_11 : '''
    # TAC.emit("return", [0])
    TAC.emit("label", [p[-8]["label"]])

def p_M_13(p):
    '''M_13 : '''
    TAC.emit("return", [0])
    TAC.emit("label", [p[-7]["label"]])

def p_M_1(p):
	'''M_1 : '''
	label_name = ST.newlabel()
	TAC.emit("ifgoto", ["==", p[-2]["place"], "0", label_name])
	p[0] = {"label": label_name}

def p_M_2(p):
    '''M_2 : '''
    label_name = ST.newlabel()
    TAC.emit("goto", [label_name])
    TAC.emit("label", [p[-3]["label"]])
    p[0] = {"label": label_name}

def p_M_3(p):
    '''M_3 : '''
    TAC.emit("label",[p[-2]["label"]])
    # for label in p[-3]:
    #     TAC.emit("label",[label]) 

def p_M_4(p):
    '''M_4 : '''
    label_name = ST.newlabel()
    TAC.emit("label",[label_name])
    p[0] = {"label" : label_name}

def p_M_5(p):
    '''M_5 : '''
    label_name = ST.newlabel()
    TAC.emit("ifgoto", ["==", p[-2]["place"], "0", label_name])
    p[0] = {"label": label_name}

def p_M_6(p):
    '''M_6 : '''
    TAC.emit("goto", [p[-5]["label"]])
    TAC.emit("label", [p[-2]["label"]])
    # for i in p[-3]:
    #     TAC.emit("label", [i])

def p_M_7(p):
    '''M_7 : '''
    temp_name = ST.newtemp({})
    # print p[-2]
    TAC.emit("Assignment", [temp_name, p[-2][0]])
    label_name = ST.newlabel()
    TAC.emit("label", [label_name])
    p[0] = {"label1": label_name, "iter": temp_name}
    label_name2 = ST.newlabel()
    TAC.emit("ifgoto", [">", temp_name, p[-2][1], label_name2])
    ST.varinsert(p[-4], {"type":"int", "declare": True})
    TAC.emit("Assignment", [p[-4], temp_name])
    p[0]["label2"] = label_name2

def p_M_8(p):
    '''M_8 : '''
    TAC.emit("Arithmetic", ["+", p[-2]["iter"], p[-2]["iter"], "1"])
    TAC.emit("goto", [p[-2]["label1"]])
    TAC.emit("label", [p[-2]["label2"]])
    # TAC.emit("Assignment", [p[-6], p[-2]["iter"]])
    # if(isinstance(p[-3],list)):
    #     for i in p[-3]:
    #         TAC.emit("label", [i])

def p_function_call(p):
    '''function_call : fname2 BR_LCIR arg_to_pass BR_RCIR M_14'''
    TAC.emit('call', [p[1],''])
    TAC.emit('pop', [p[3]])
    temp_name = ST.newtemp({"type" : 'int'})
    TAC.emit('retval', [temp_name])
    p[0] = {'place':temp_name, 'type':'int'}
def p_fname_2(p):
    '''fname2 : IDENTIFIER'''
    p[0] = p[1]
def p_M_14(p):
	'''M_14 : '''
	funcdict = globalST.funclookup(p[-4])
	if(funcdict==False):
		print ('ERROR:',p[-4], 'not defined')
		TAC.error = True
	elif(funcdict["num"]!=p[-2]):
		print ('ERROR', 'Number of arguments passed mismatch in',p[-4])
		TAC.error = True

def p_arg_to_pass_1(p):
    '''arg_to_pass : arg_to_pass SEP_COMMA arg M_15'''
    p[0] = p[1] + 1
def p_arg_to_pass_2(p):
    '''arg_to_pass : arg M_15'''
    p[0] = 1
def p_arg_to_pass_3(p):
    '''arg_to_pass : '''
    p[0] = 0
def p_arg_1(p):
    '''arg : rightside'''
    p[0] = p[1]

def p_M_15(p):
	'''M_15 : '''
	TAC.emit("param", [p[-1]["place"]])

def p_compound_statement_1(p):
    '''compound_statement : BR_LCUR statement_list BR_RCUR'''
    p[0] = p[2]

def p_statement_list_1(p):
    '''statement_list : statement_list statement'''
        
def p_statement_list_2(p):
    '''statement_list : statement'''
        
def p_statement_definition_1(p):
    '''statement : expression'''
    p[0] = p[1]
def p_statement_definition_3(p):
    '''statement : for_loop'''
    p[0] = p[1]
def p_statement_definition_4(p):
    '''statement : while_loop'''
    p[0] = p[1]    
def p_statement_definition_5(p):
    '''statement : if_statement'''
    p[0] = p[1]
def p_statement_definition_6(p):
    '''statement : if_else_statement'''
    p[0] = p[1]
# def p_if_cond_0(p):
#     '''if_cond :  TYPE_BOOLEAN'''
#     p[0] = p[1]
def p_if_cond_1(p):
    '''if_cond :  rightside'''
    p[0] = p[1]
def p_if_cond_2(p):
    '''if_cond :  comparison_statement'''
    p[0] = p[1]

def p_if_cond_3(p):
    '''if_cond : comparison_statement logop if_cond'''
    temp_name = ST.newtemp({"type" : p[3]["type"]})
    TAC.emit('Arithmetic',[p[2],temp_name, p[1]['place'], p[3]['place']])
    p[0] = {"place": temp_name, "type": p[3]["type"]}

def p_if_cond_4(p):
    '''if_cond : comparison_statement bitop if_cond '''
    temp_name = ST.newtemp({"type" : p[3]["type"]})
    TAC.emit('Arithmetic',[p[2],temp_name, p[1]['place'], p[3]['place']])
    p[0] = {"place": temp_name, "type": p[3]["type"]}

def p_if_cond_5(p):
    '''if_cond : OP_BITNOT if_cond '''
    temp_name = ST.newtemp({"type" : p[2]["type"]})
    TAC.emit('logicalNOT',[p[1],temp_name, p[2]['place']])
    p[0] = {"place": temp_name, "type": p[2]["type"]}

def p_comparison_statement_0(p):
    '''comparison_statement :  IDENTIFIER compop any_type '''
    var_dict = ST.varlookup(p[1])
    if(var_dict == False):
        var_dict = globalST.varlookup(p[1])
        if (var_dict == False):
            print("ERROR: variable", p[1],'is not defined.')
            TAC.error = True
    temp_name = ST.newtemp({"type" : p[3]["type"]})
    TAC.emit('Arithmetic',[p[2],temp_name, p[1], p[3]["place"]])
    p[0] = {"place": temp_name, "type": p[3]["type"]}

def p_comparison_statement_1(p):
	'''comparison_statement :  IDENTIFIER compop IDENTIFIER '''
	var_dict1 = ST.varlookup(p[1])
	var_dict2 = ST.varlookup(p[3])
	if(var_dict1 == False or var_dict2 == False):
		var_dict1 = globalST.varlookup(p[1])
		var_dict2 = globalST.varlookup(p[3])
		if (var_dict1 == False and var_dict2 == False):
			print("ERROR: variable", p[1], 'and', p[3],'is not defined.')
			TAC.error = True
		elif(var_dict1 != False and var_dict2 == False):
			print("ERROR: variable", p[3],'is not defined.')
			TAC.error = True
		elif(var_dict1 == False and var_dict2 != False):
			print("ERROR: variable", p[1],'is not defined.')
			TAC.error = True
	if((var_dict1['type']=='int' or var_dict1['type']=='num' ) and (var_dict2['type']=='int' or var_dict2['type']=='num' )):
		if(var_dict1['type']=='int' and var_dict2['type']=='int'):
			temp_name = ST.newtemp({'type':'int'})
			TAC.emit('Arithmetic',[p[2],temp_name, p[1], p[3]])
			p[0] = {"place": temp_name, "type":'int' }
		else:
			temp_name = ST.newtemp({'type':'num'})
			TAC.emit('Arithmetic',[p[2],temp_name, p[1], p[3]])
			p[0] = {"place": temp_name, "type":'num' }
	elif((var_dict1['type']=='int' or var_dict1['type']=='num' ) and (var_dict2['type']!='int' or var_dict2['type']!='num' )):
		print("ERROR: variable", p[3],'is not type of num or int')
		TAC.error = True
	elif((var_dict1['type']!='int' or var_dict1['type']!='num' ) and (var_dict2['type']=='int' or var_dict2['type']=='num' )):
		print("ERROR: variable", p[1],'is not type of num or int')
		TAC.error = True
	else:
		print("ERROR: variable", p[1],'and',p[3],'are not type of num or int')
		TAC.error = True

def p_comparison_statement_2(p):
	'''comparison_statement :  any_type compop any_type'''
	if((p[1]['type']=='int' or p[1]['type']=='num' ) and (p[3]['type']=='int' or p[3]['type']=='num' )):
		if(p[1]['type']=='int' and p[3]['type']=='int'):
			temp_name = ST.newtemp({'type':'int'})
			TAC.emit('Arithmetic',[p[2],temp_name, p[1]['place'], p[3]['place']])
			p[0] = {"place": temp_name, "type":'int' }
		else:
			temp_name = ST.newtemp({'type':'num'})
			TAC.emit('Arithmetic',[p[2],temp_name, p[1]['place'], p[3]['place']])
			p[0] = {"place": temp_name, "type":'num' }
	elif((p[1]['type']=='int' or p[1]['type']=='num' ) and (p[3]['type']!='int' or p[3]['type']!='num' )):
		print("ERROR: variable", p[3],'is not type of num or int')
		TAC.error = True
	elif((p[1]['type']!='int' or p[1]['type']!='num' ) and (p[3]['type']=='int' or p[3]['type']=='num' )):
		print("ERROR: variable", p[1],'is not type of num or int')
		TAC.error = True
	else:
		print("ERROR: variable", p[1],'and',p[3],'are not type of num or int')
		TAC.error = True

def p_comparison_statement_3(p):
	'''comparison_statement : BR_LCIR if_cond BR_RCIR '''
	p[0] = p[2]

def p_logop_1(p):
    '''logop : OP_LOGAND'''
    p[0] = p[1]
        
def p_logop_2(p):
    '''logop : OP_LOGOR'''
    p[0]=p[1]

def p_bitop_1(p):
    '''bitop : OP_BITAND'''
    p[0]=p[1]

def p_bitop_2(p):
    '''bitop : OP_BITOR'''
    p[0]=p[1]

def p_comop_definition_1(p):
    '''compop : OP_GREAT'''
    p[0] = p[1]

def p_comop_definition_2(p):
    '''compop : OP_LESS'''
    p[0] = p[1]
    
def p_comop_definition_3(p):
    '''compop : OP_LEEQ'''
    p[0] = p[1]
    
def p_comop_definition_4(p):
    '''compop : OP_GREQ'''
    p[0] = p[1]

def p_comop_definition_5(p):
    '''compop : OP_NOEQ'''
    p[0] = p[1]

def p_comop_definition_6(p):
    '''compop : OP_COMP'''
    p[0] = p[1]

def p_expression_math_0(p):
    '''expression : IDENTIFIER BR_LCSR rightside BR_RCSR OP_ASGN rightside'''
    temp_name1 = ST.newtemp({"type":"int"})
    temp_name2 = ST.newtemp({"type":"int"})
    temp_name = ST.newtemp({"type":"int"})
    TAC.emit('Assignment',[temp_name1,p[3]['place']])
    TAC.emit('Arithmetic',['*',temp_name2,temp_name1,'4'])
    TAC.emit('member',[temp_name,p[1],temp_name2])
    TAC.emit('Assignment',[temp_name,p[6]['place']])
    p[0] = {'place':temp_name,'type':'int'}

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
    '''expression : IDENTIFIER OP_ASGN vector_definition M_16'''
    var_dict = ST.varlookup(p[1])
    if(var_dict == False):
        var_dict = globalST.varlookup(p[1])
        if (var_dict == False):
            ST.varinsert(p[1], {"type":'vector', "declare": True})
            var_dict = {"type":'vector', "declare": True}
    p[0] = {"place":p[1], "type": var_dict["type"]}

def p_M_16(p):
    '''M_16 : '''
    TAC.emit('vector', [p[-3], len(p[-1])])
    for i in range(len(p[-1])):
        TAC.emit('Arithmetic', ['=', p[-3], str(i),p[-1][i]])
# def p_expression_math_3(p):
#     '''expression : jump_statements'''
#     p[0] = p[1]

def p_expression_math_4(p):
    '''expression : KEYWORD_PRINT BR_LCIR rightside BR_RCIR'''
    TAC.emit('print',[p[3]['place']])

def p_expression_math_5(p):
    '''expression : KEYWORD_RETURN BR_LCIR rightside BR_RCIR'''
    TAC.emit('return',[p[3]['place']]) 
def p_vector_2(p):
    '''vector_definition : KEYWORD_VECTOR BR_LCIR SEP_COMMA TYPE_INTEGER BR_RCIR'''
    p[0] = []
    for i in range(p[4]):
        p[0] = p[0] + [0]
def p_vector_4(p):
    '''vector_definition : KEYWORD_VECTOR_CONSTRUCTOR BR_LCIR vector_elements BR_RCIR'''
    p[0] = p[3]
    # print p[0]
def p_vector_elements(p):
    '''vector_elements : vector_elements SEP_COMMA TYPE_INTEGER
                        | TYPE_INTEGER'''
    if(len(p)==2):
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

# def p_jump_statements_1(p):
#     '''jump_statements :  KEYWORD_BREAK'''

# def p_jump_statements_2(p):
#     '''jump_statements :  KEYWORD_NEXT'''

def p_math_rightside_1(p):
    '''rightside : rightside math rightside'''
    if(p[3]["type"] != "num" and p[3]["type"] != "int"):
        print("TYPE ERROR: variable", p[1]['place'],'and',p[3]["type"], 'not matching type.')
    temp_name = ST.newtemp({"type" : "num"})
    TAC.emit('Arithmetic',[p[2],temp_name,p[1]['place'],p[3]["place"]])
    p[0] = {"place": temp_name, "type": "num"}

# def p_math_rightside_2(p):
#     '''rightside : TYPE_INTEGER math rightside'''
#     if(p[3]["type"] != "num" and p[3]["type"] != "int"):
#         print("TYPE ERROR: variable", p[1],'and',p[3], 'not matching type.')
#     temp_name = ST.newtemp({"type" : p[3]["type"]})
#     TAC.emit('Arithmetic',[p[2],temp_name,p[1],p[3]["place"]])
#     p[0] = {"place": temp_name, "type": p[3]["type"]}

def p_math_rightside_3(p):
    '''rightside : IDENTIFIER math rightside '''
    var_dict = ST.varlookup(p[1])
    # print var_dict
    if(var_dict == False):
        var_dict = globalST.varlookup(p[1])
        if (var_dict == False):
            print("ERROR: variable", p[1],'is not defined.')
            TAC.error = True
    temp_name = ST.newtemp({"type" : p[3]["type"]})
    TAC.emit('Arithmetic',[p[2],temp_name, p[1], p[3]["place"]])
    p[0] = {"place": temp_name, "type": p[3]["type"]}

def p_math_rightside_4(p):
    '''rightside : BR_LCIR rightside BR_RCIR'''
    p[0] = p[2]

def p_math_rightside_5(p):
    '''rightside : any_type bitop rightside'''
    if(p[3]["type"] != "num" and p[3]["type"] != "int"):
        print("TYPE ERROR: variable", p[1],'and',p[3], 'not matching type.')
    temp_name = ST.newtemp({"type" : p[3]["type"]})
    TAC.emit('Arithmetic',[p[2],temp_name,p[1],p[3]["place"]])
    p[0] = {"place": temp_name, "type": p[3]["type"]}

def p_math_rightside_6(p):
    '''rightside : any_type logop rightside'''
    if(p[3]["type"] != "num" and p[3]["type"] != "int"):
        print("TYPE ERROR: variable", p[1],'and',p[3], 'not matching type.')
    temp_name = ST.newtemp({"type" : p[3]["type"]})
    TAC.emit('Arithmetic',[p[2],temp_name,p[1],p[3]["place"]])
    p[0] = {"place": temp_name, "type": p[3]["type"]}

def p_math_rightside_8(p):
    '''rightside : IDENTIFIER bitop rightside'''
    var_dict = ST.varlookup(p[1])
    # print var_dict
    if(var_dict == False):
        var_dict = globalST.varlookup(p[1])
        if (var_dict == False):
            print("ERROR: variable", p[1],'is not defined.')
            TAC.error = True
    temp_name = ST.newtemp({"type" : p[3]["type"]})
    TAC.emit('Arithmetic',[p[2],temp_name, p[1], p[3]["place"]])
    p[0] = {"place": temp_name, "type": p[3]["type"]}

def p_math_rightside_9(p):
    '''rightside : IDENTIFIER logop rightside'''
    var_dict = ST.varlookup(p[1])
    # print var_dict
    if(var_dict == False):
        var_dict = globalST.varlookup(p[1])
        if (var_dict == False):
            print("ERROR: variable", p[1],'is not defined.')
            TAC.error = True
    temp_name = ST.newtemp({"type" : p[3]["type"]})
    TAC.emit('Arithmetic',[p[2],temp_name, p[1], p[3]["place"]])
    p[0] = {"place": temp_name, "type": p[3]["type"]}
    
def p_math_rightside_10(p):
    '''rightside : IDENTIFIER'''
    var_dict = ST.varlookup(p[1])
    # print var_dict
    if(var_dict == False):
        var_dict = globalST.varlookup(p[1])
        if (var_dict == False):
            print("ERROR: variable", p[1],'is not defined.')
            TAC.error = True
    p[0] = {"place":p[1], "type": var_dict["type"]} 

def p_math_rightside_11(p):
    '''rightside : any_type'''
    p[0] = p[1]
def p_math_rightside_12(p):
    '''rightside : function_call'''
    p[0] = p[1]
def p_math_rightside_13(p):
    '''rightside : IDENTIFIER BR_LCSR rightside BR_RCSR'''
    temp_name1 = ST.newtemp({"type":"int"})
    temp_name2 = ST.newtemp({"type":"int"})
    temp_name = ST.newtemp({"type":"int"})
    TAC.emit('Assignment',[temp_name1,p[3]['place']])
    TAC.emit('Arithmetic',['*',temp_name2,temp_name1,'4'])
    TAC.emit('member',[temp_name,p[1],temp_name2])
    p[0] = {'place':temp_name,'type':'int'}
    # print p[0]
# def p_math_rightside_14(p):
#     '''rightside : IDENTIFIER BR_LCSR TYPE_INTEGER BR_RCSR'''
#     temp_name1 = ST.newtemp({"type":"int"})
#     temp_name2 = ST.newtemp({"type":"int"})
#     temp_name = ST.newtemp({"type":"int"})
#     TAC.emit('Assignment',[temp_name1,p[3]])
#     TAC.emit('Arithmetic',['*',temp_name2,temp_name1,'4'])
#     TAC.emit('member',[temp_name,p[1],temp_name2])
#     p[0] = {'place':temp_name,'type':'int'}
#     print p[0]
# def p_math_rightside_16(p):
#     '''rightside : vector_definition'''

def p_math_1(p):
    '''math : OP_PLUS'''
    p[0] = p[1]
        
def p_math_2(p):
    '''math : OP_MINUS'''
    p[0] = p[1]
        
def p_math_3(p):
    '''math : OP_MULT'''
    p[0] = p[1]
        
def p_math_4(p):
    '''math : OP_DIVIDE'''
    p[0] = p[1]
        
def p_math_5(p):
    '''math : OP_EXPO'''
    p[0] = p[1]
        
def p_math_6(p):
    '''math : OP_REMDR'''
    p[0] = p[1]

def p_for_range(p):
    '''for_range : for_range_variables SEP_COLON for_range_variables
    '''
    p[0] = [p[1],p[3]]

def p_for_range_variables(p):
    ''' for_range_variables : IDENTIFIER'''
    var_dict = ST.varlookup(p[1])
    # print p[1]
    # print var_dict
    if (var_dict["declare"] == False):
    	var_dict = globalST.varlookup(p[1])
    	if (var_dict["declare"] == False):
    		print("DECLARATION ERROR: variable", p[1], 'not declared.')
    		TAC.error = True
    	if (var_dict["type"] != "int"):
            print(p[1], 'not int type.')
            TAC.error = True
    p[0] = p[1]

def p_for_range_variables_0(p):
    ''' for_range_variables : TYPE_INTEGER'''
    temp_name = ST.newtemp({"type":"int"})
    TAC.emit('Assignment', [temp_name, p[1]])
    p[0] = {"place": temp_name, "type": "int"} 
    p[0] = temp_name
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
    print p.lineno
    TAC.error = True

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
myfile.close()

# print "global symboltable";
# print ST.vardict
# print ST.funcdict
if (TAC.error == False):
    TAC.printTAC()