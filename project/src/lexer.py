#!/usr/bin/python
from sys import argv
import os
import ply.lex as lex
import fileinput

# global ids
# ids=0
keywords = {
    'if' : 'KEYWORD_IF',
    # 'break' : 'KEYWORD_BREAK',
    # 'next': 'KEYWORD_NEXT',
    'else' : 'KEYWORD_ELSE',
    'while' : 'KEYWORD_WHILE',
    'for' : 'KEYWORD_FOR',
    'function': 'KEYWORD_FUNCTION',
    'in': 'KEYWORD_IN',
    'return':'KEYWORD_RETURN',
    'print':'KEYWORD_PRINT',
    'c':'KEYWORD_VECTOR_CONSTRUCTOR',
    'vector':'KEYWORD_VECTOR'  
    }

tokens = ['OP_FUNC_ASGN','BR_LCSR','BR_RCSR','BR_LCIR', 'BR_LCUR',  'BR_RCIR' ,'BR_RCUR',  'IDENTIFIER', 'OP_ASGN', 'OP_BITAND','OP_BITNOT', 'OP_BITOR', 'OP_COMP', 'OP_DIVIDE', 'OP_EXPO', 'OP_GREQ', 'OP_GREAT', 'OP_LEEQ', 'OP_LESS', 'OP_LOGAND', 'OP_LOGOR', 'OP_MINUS', 'OP_MULT', 'OP_NOEQ',  'OP_PLUS',  'OP_REMDR', 'SEP_COLON', 'SEP_COMMA',  'TYPE_INTEGER', 'TYPE_BOOLEAN','TYPE_STRING','TYPE_NUMERIC'] + list(keywords.values())
token_list = [[] for i in range(len(tokens))]

def t_ignore_COMMENT(t):
    r"\#[^\n]+"

def t_newline(t):
   r'\n+'
   t.lexer.lineno += len(t.value)

t_ignore = '\t'
t_ignore_blspace = r"\s+"

#Defining identifiers
def t_TYPE_BOOLEAN(t):
    r"TRUE|FALSE"
    return t
    
def t_IDENTIFIER(t):
    r'[a-zA-Z][a-zA-Z_.0-9]*|'r'[a-zA-Z.][a-zA-Z_.][a-zA-Z_.0-9]* '
    t.type = keywords.get(t.value,'IDENTIFIER')
    return t


def t_KEYWORD_IF(t):
    r'if'
    return t

def t_KEYWORD_BREAK(t):
    r'break'
    return t
def t_KEYWORD_NEXT(t):
    r'next'
    return t

def t_KEYWORD_ELSE(t):
    r'else'
    return t

def t_KEYWORD_WHILE(t):
    r'while'
    return t

def t_KEYWORD_FOR(t):
    r'for'
    return t

def t_KEYWORD_FUNCTION(t):
    r'function'
    return t

def t_KEYWORD_IN(t):
    r'in'
    return t

def t_KEYWORD_RETURN(t):
    r'return'
    return t

def t_KEYWORD_PRINT(t):
    r'print'
    return t

def t_KEYWORD_VECTOR(t):
    r'vector'
    return t

def t_TYPE_STRING(t):
	r'\"([^\\\n]|(\\.))*?\"|'r"\'([^\\\n]|(\\.))*?\'"
	return t
    	
def t_TYPE_NUMERIC(t):
	r' [-+]?(\b[0-9]+\.([0-9]+\b)?|\.[0-9]+\b) | [-+]?\b\d+\b'
	if('.' in t.value):
	    t.value = float(t.value)
	else:
	    t.value = int(t.value)
	return t

def t_TYPE_INTEGER(t):
    r'[-+]?\d+[L]+'
    if(t.value[len(t.value)-2] <= '9' and t.value[len(t.value)-2] >= '0'):
        t.value = t.value[0:-1]
        t.value = long(t.value)         
        return t
    else:
        print "\nSyntax Error:", t.value, "is not an integer"
    t.lexer.skip(1)


#Defining the operators
def t_OP_PLUS(t):
    r'\+'
    return t

def t_OP_MINUS(t):
    r'\-'
    return t

def t_OP_MULT(t):
    r'\*'
    return t

def t_OP_DIVIDE(t):
    r'/'
    return t

def t_OP_EXPO(t):
    r'\^'
    return t

def t_OP_REMDR(t):
    r'%'
    return t

def t_OP_COMP(t):
    r'=='
    return t

def t_OP_ASGN(t):
    r"="
    return t

def t_OP_FUNC_ASGN(t):
    r"<-"
    return t

def t_OP_LEEQ(t):
    r'<='
    return t

def t_OP_GREQ(t):
    r'>='
    return t

def t_OP_GREAT(t):
    r'\>'
    return t
     
def t_OP_LESS(t):
    r'\<'
    return t

def t_OP_NOEQ(t):
    r'!='
    return t
        
def t_OP_BITNOT(t):
    r"!"
    return t

def t_OP_LOGAND(t):
    r'&&'
    return t

def t_OP_LOGOR(t):
    r'\|\|'
    return t

def t_OP_BITOR(t):
    r'\|'
    return t

def t_OP_BITAND(t):
    r'\&'
    return t
 
#Defining the separators
def t_SEP_COMMA(t):
    r'\,'
    return t

def t_SEP_COLON(t):
    r'\:'
    return t

#Defining the various Brackets
def t_BR_RCUR(t):
    r'\}'
    return t

def t_BR_LCUR(t):
    r'\{'
    return t

def t_BR_RCIR(t):
    r'\)'
    return t

def t_BR_LCIR(t):
    r'\('
    return t

def t_BR_LCSR(t):
    r'\['
    return t
def t_BR_RCSR(t):
    r'\]'
    return t

def t_KEYWORD_VECTOR_CONSTRUCTOR(t):
    r'c'
    return t

# Error message
def t_error(t):
    print("Illegal Character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
# script, data = argv
# fp = open(os.path.abspath(data),"r")
# lexer.input(fp.read())

# # Tokenize
# while True:
#     tok = lexer.token()
#     if not tok: 
#         break
#     token_list[tokens.index(tok.type)].append(tok.value)
#     for tok in iter (lexer.token, None):
#         token_list[tokens.index(tok.type)].append(tok.value)

# token_list[tokens.index('IDENTIFIER')]=list(set(token_list[tokens.index('IDENTIFIER')]))
# print "Token  \t Occurance \tLexeme(s)"
# for i in range (0,len(tokens)):
#     if(len(token_list[i])> 0 and i != tokens.index('TYPE_NUMERIC') and i!=tokens.index('TYPE_INTEGER')):
#         print tokens[i] ,'\t' ,len(token_list[i]), '\t',(", ".join( repr(e) for e in (list(set(token_list[i])))))
#     elif(len(token_list[i])> 0 and (i == tokens.index('TYPE_NUMERIC') or i==tokens.index('TYPE_INTEGER'))):
#         print tokens[i] ,'\t' ,len(token_list[i]), '\t',(", ".join( repr(e) for e in (list(token_list[i]))))

# fp.close()