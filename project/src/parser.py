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

def varType(var):
    try:
        if int(var) == float(var):
            return 'int'
    except:
        try:
            float(var)
            return 'float'
        except:
            return 'str'

def p_program(p):
    '''program : start'''
    TAC.emit('EndOfCode', [])

def p_start(p):
    '''start    : expression_statements
                | loop_statements
                | conditional_statements
                | functions_statements
                | '''

def p_expression_statements(p):
    '''expression_statements : expression start'''

def p_loop_statements(p):
    '''loop_statements  : while_loop start
                        | for_loop start'''

def p_functions_statements(p):
    '''functions_statements : function_definition start
                            | function_call start'''

def p_conditional_statements(p):
    '''conditional_statements   : if_else_statement start
                                | if_statement start'''

def p_if_else_statement(p):
    '''if_else_statement : KEYWORD_IF BR_LCIR if_cond BR_RCIR M_1 compound_statement KEYWORD_ELSE M_2 compound_statement M_3'''

def p_if_statement(p):
    '''if_statement : KEYWORD_IF BR_LCIR if_cond BR_RCIR M_1 compound_statement M_3'''

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

def p_while_loop(p):
    '''while_loop : KEYWORD_WHILE BR_LCIR M_4 if_cond BR_RCIR M_5 compound_statement M_6'''

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

def p_for_loop(p):
    '''for_loop : KEYWORD_FOR BR_LCIR IDENTIFIER KEYWORD_IN for_range BR_RCIR M_7 compound_statement M_8'''

def p_for_range(p):
    '''for_range : for_range_variables SEP_COLON for_range_variables
    '''
    p[0] = [p[1],p[3]]

def p_for_range_variables(p):
    ''' for_range_variables : IDENTIFIER
                            | any_type'''
    if (isinstance(p[1],dict)):
        if(p[1]['type'] != 'int'):
            print("range in for loop only accepts integer values")
            TAC.error = True
        p[0] = p[1]['place']
    else:
        var_dict = ST.varlookup(p[1])
        if(var_dict == False):
            var_dict = globalST.varlookup(p[1])
            if (var_dict == False):
                print("ERROR: variable", p[1],'is not defined.')
                TAC.error = True
            if (var_dict["type"] != "int"):
                print(p[1], 'not int type.')
                TAC.error = True
        p[0] = p[1]

def p_M_7(p):
    '''M_7 : '''
    temp_name = ST.newtemp({'type' : 'int'})
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

def p_function_definition_1(p):
    '''function_definition : fname OP_FUNC_ASGN KEYWORD_FUNCTION BR_LCIR arg_list M_10 BR_RCIR compound_statement M_11
                           | fname OP_FUNC_ASGN KEYWORD_FUNCTION BR_LCIR BR_RCIR M_12 compound_statement M_13'''
    global ST
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
    ST.varinsert(p[-1], {"type":'int', "declare":True})
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
    indexoffuncdef = TAC.code.index('function,'+p[-8]["fname"])
    no_of_args = 0
    indices = [i for i, x in enumerate(TAC.code) if x == 'call,'+p[-8]["fname"]]
    for indexoffunccall in indices:
        index1 = indexoffunccall + 1 + no_of_args
        index2 = indexoffuncdef
        index2 = index2 + 1
        while (TAC.code[index2].startswith('funcarg')):
            TAC.code.insert(index1,TAC.code[index2])
            index1 = index1 + 1
            index2 = index2 + 1
            no_of_args += 1
    TAC.emit("label", [p[-8]["label"]])

def p_M_13(p):
    '''M_13 : '''
    TAC.emit("return", [0])
    TAC.emit("label", [p[-7]["label"]])


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

def p_arg_to_pass(p):
    '''arg_to_pass  : arg_to_pass SEP_COMMA arg M_15
                    | arg M_15
                    | '''
    if(len(p)==5):
        p[0] = p[1] + 1
    elif(len(p)==3):
        p[0] = 1
    else:
        p[0] = 0
    
def p_arg(p):
    '''arg : rightside'''
    p[0] = p[1]

def p_M_15(p):
    '''M_15 : '''
    TAC.emit("param", [p[-1]["place"]])

def p_compound_statement(p):
    '''compound_statement : BR_LCUR statement_list BR_RCUR'''
    p[0] = p[2]

def p_statement_list(p):
    '''statement_list   : statement_list statement
                        | statement'''
        
def p_statement_definition(p):
    '''statement    : expression
                    | for_loop
                    | while_loop
                    | if_statement
                    | if_else_statement'''
    p[0] = p[1]

def p_if_cond(p):
    '''if_cond :  comparison_statement
                | OP_BITNOT if_cond
                | comparison_statement logop if_cond
                | comparison_statement bitop if_cond'''
    if(len(p)==2):
        p[0] = p[1]

    elif(len(p)==3):
        temp_name = ST.newtemp({"type" : p[2]["type"]})
        TAC.emit('logicalNOT',[p[1],temp_name, p[2]['place']])
        p[0] = {"place": temp_name, "type": p[2]["type"]}
    else:
        temp_name = ST.newtemp({"type" : p[3]["type"]})
        TAC.emit('Arithmetic',[p[2],temp_name, p[1]['place'], p[3]['place']])
        p[0] = {"place": temp_name, "type": p[3]["type"]}    

def p_comparison_statement(p):
    '''comparison_statement : comparison_operand compop comparison_operand
                            | BR_LCIR if_cond BR_RCIR
                            | comparison_operand'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        if p[1] == '(':
            p[0] = p[2]
        else:
            temp_name = ST.newtemp({"type" : p[3]["type"]})
            TAC.emit('Arithmetic',[p[2],temp_name, p[1]['place'], p[3]['place']])
            p[0] = {"place": temp_name, "type": p[3]["type"]}

def p_comparison_operand(p):
    '''comparison_operand : IDENTIFIER
                            | any_type'''
    global ST
    if (isinstance(p[1],dict)):
        p[0] = p[1]
    else:
        var_dict = ST.varlookup(p[1])
        if(var_dict == False):
            var_dict = globalST.varlookup(p[1])
            if (var_dict == False):
                print("ERROR: variable", p[1],'is not defined.')
                TAC.error = True
        p[0] = {"place": p[1], "type": var_dict["type"]}

def p_logop(p):
    '''logop    :   OP_LOGAND
                |   OP_LOGOR'''
    p[0] = p[1]
        
def p_bitop(p):
    '''bitop    :    OP_BITAND
                |   OP_BITOR'''
    p[0] = p[1]

def p_comop(p):
    '''compop   : OP_GREAT
                | OP_LESS
                | OP_LEEQ
                | OP_GREQ
                | OP_NOEQ
                | OP_COMP'''
    p[0] = p[1]

def p_expression(p):
    '''expression   : IDENTIFIER BR_LCSR rightside BR_RCSR OP_ASGN rightside
                    | IDENTIFIER OP_ASGN rightside
                    | IDENTIFIER OP_ASGN vector_definition M_16
                    | KEYWORD_PRINT BR_LCIR rightside BR_RCIR
                    | KEYWORD_RETURN BR_LCIR rightside BR_RCIR'''
    if(len(p)==7):
        temp_name1 = ST.newtemp({"type":"int"})
        temp_name2 = ST.newtemp({"type":"int"})
        temp_name = ST.newtemp({"type":"int"})
        TAC.emit('Assignment',[temp_name1,p[3]['place']])
        TAC.emit('Arithmetic',['*',temp_name2,temp_name1,'4'])
        TAC.emit('update',[p[6]['place'],p[1],temp_name2])
    elif(len(p)==4):
        var_dict = ST.varlookup(p[1])
        if(var_dict == False):
            var_dict = globalST.varlookup(p[1])
            if (var_dict == False):
                ST.varinsert(p[1], {"type":p[3]['type'], "declare": True})
                var_dict = {"type":p[3]['type'], "declare": True}
        TAC.emit('Assignment', [p[1], p[3]['place']])
        p[0] = {"place":p[1], "type": var_dict["type"]}      
    else:
        if(p[1]=='print'):
            TAC.emit('print',[p[3]['place']])
        elif(p[1]=='return'):
            TAC.emit('return',[p[3]['place']])
        else:
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
        temp_name1 = ST.newtemp({'type':'int'})
        temp_name2 = ST.newtemp({'type':'int'})
        TAC.emit('Assignment', [temp_name1, i])
        TAC.emit('Arithmetic', ['*', temp_name2, temp_name1,'4'])
        TAC.emit('update', [p[-1][i], p[-3],temp_name2])     

def p_vector_definition(p):
    '''vector_definition    : KEYWORD_VECTOR BR_LCIR SEP_COMMA TYPE_INTEGER BR_RCIR
                            | KEYWORD_VECTOR_CONSTRUCTOR BR_LCIR vector_elements BR_RCIR'''
    if(len(p)==6):
        p[0] = []
        for i in range(p[4]):
            p[0] = p[0] + [0]
    else:
        p[0] = p[3]
    
def p_vector_elements(p):
    '''vector_elements : vector_elements SEP_COMMA TYPE_INTEGER
                        | TYPE_INTEGER'''
    if(len(p)==2):
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_rightside(p):
    '''rightside    : leftside math rightside
                    | leftside logop rightside
                    | leftside bitop rightside
                    | leftside
                    | function_call'''
    if(len(p)==2):
        p[0] = p[1]
    else:
        if(p[3]["type"] != "num" and p[3]["type"] != "int"):
            print("TYPE ERROR: variable", p[1]['place'],'and',p[3]["type"], 'not matching type.')
        temp_name = ST.newtemp({"type" : "num"})
        TAC.emit('Arithmetic',[p[2],temp_name,p[1]['place'],p[3]["place"]])
        p[0] = {"place": temp_name, "type": "num"}

def p_leftside(p):
    '''leftside : BR_LCIR rightside BR_RCIR
                | any_type
                | IDENTIFIER
                | IDENTIFIER BR_LCSR rightside BR_RCSR'''
    if(len(p)==5):
        temp_name1 = ST.newtemp({"type":"int"})
        temp_name2 = ST.newtemp({"type":"int"})
        temp_name = ST.newtemp({"type":"int"})
        TAC.emit('Assignment',[temp_name1,p[3]['place']])
        TAC.emit('Arithmetic',['*',temp_name2,temp_name1,'4'])
        TAC.emit('member',[temp_name,p[1],temp_name2])
        p[0] = {'place':temp_name,'type':'int'}
    elif(len(p)==4):
        p[0] = p[2]
    else:
        if (isinstance(p[1],dict)):
            p[0] = p[1]
        else:
            var_dict = ST.varlookup(p[1])
            if(var_dict == False):
                var_dict = globalST.varlookup(p[1])
                if (var_dict == False):
                    print("ERROR: variable", p[1],'is not defined.')
                    TAC.error = True
            p[0] = {"place": p[1], "type": var_dict["type"]}

def p_math(p):
    '''math : OP_PLUS
            | OP_MINUS
            | OP_MULT
            | OP_DIVIDE
            | OP_REMDR
            | OP_EXPO'''
    p[0] = p[1]

def p_any_type(p):
    '''any_type : TYPE_NUMERIC
                | TYPE_INTEGER
                | TYPE_STRING
                | TYPE_BOOLEAN'''
    if(p[1]=='TRUE'):
        temp_name = ST.newtemp({"type" : "bool"})
        TAC.emit('Assignment', [temp_name, '1'])
        p[0] = {"place": temp_name, "type": "bool"}
    elif p[1] == 'FALSE':
        temp_name = ST.newtemp({"type" : "bool"})
        TAC.emit('Assignment', [temp_name, '0'])
        p[0] = {"place": temp_name, "type": "bool"} 
    else:
        if (varType(p[1])=='int'):
            temp_name = ST.newtemp({"type" : "int"})
            p[0] = {"place": temp_name, "type": "int"}
            TAC.emit('Assignment',[temp_name, p[1]])
        elif (varType(p[1])=='num'):
            temp_name = ST.newtemp({"type" : "num"})
            p[0] = {"place": temp_name, "type": "num"}
            TAC.emit('Assignment',[temp_name, p[1]])
        else:
            temp_name = ST.newtemp({"type" : "str"})
            p[0] = {"place": temp_name, "type": "str"}
            TAC.emit('Assignment',[temp_name, p[1]])

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
if (TAC.error == False):
    TAC.printTAC()