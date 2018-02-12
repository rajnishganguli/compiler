#!/usr/bin/python
import sys
import os
import numpy as np

if len(sys.argv) == 2:
	filename = str(sys.argv[1])
else:
	print("usage: python codegen.py irfile")
	exit()
	
reg={'%eax': None, '%edi': None, '%ebx': None, '%esi': None, '%ecx': None, '%edx': None}
regalwaysinuse={'%esp':None,"%ebp":None}

operators = ['+','-','*','/','=','==','<=','>=','>','<',"%%","&&","||",'&','|',"!=",'!',"ifgoto","goto","call","return","label","print","endOfCode"]
var_list=[]		# description of variables in the intermediate code - input provided
global asmout #final output of the assembly language
asmout = ""
def integer(number):
		if number.isdigit() or (number[1:].isdigit() and (number[0] == "-" or number[0] == "+")):
			return 1
		else:
			return 0

def getreg(var, lineno):
	# print 'before getreg'
	# print '\n'
	# print reg
	global asmout
	l = []
	temp = []
	temp_var = []
	flag = 0
	index= 0
	if var in reg.values():
		for register in reg.keys():
			if reg[register] == var:
				return register

	for register in reg.keys():
		if reg[register] == None:
			return register	

	for i in range(0,len(fs_table)):
		for j in range(0,len(fs_table[i])):
			if int(fs_table[i][j][0]) == int(lineno):
				index = i
				flag = 1
				break
		if flag == 1:
			break
	
	#print reg.values()
	#print fs_table

	for variable in reg.values():
		for i in range(0,len(fs_table[index])):
				if (int(fs_table[index][i][0]) > int(lineno)):
							

					if fs_table[index][i][1] == variable:
						l.append(int(fs_table[index][i][3]))
						temp_var.append(fs_table[index][i][1])
	temp = [x for x in reg.values() if x not in temp_var]			
	
	for key in reg.keys():
		if temp:
			if reg[key] in temp:
				reg_spil = key 
		else:
			variable = fs_table[index][max(l)][1]
			if reg[key] == variable:
				reg_spil = key

			
	asmout = asmout + "\t movl " + reg_spil + ", " + var + "\n"
	#print asmout
	# print 'after getreg'
	# print '\n'
	# print reg
	return reg_spil

def freereg(register_name):
	# global asmout
	# print 'before freereg'
	# print '\n'
	# print reg
	if (reg[register_name] != None) :
		asmout = "\t movl " + str(register_name) + " , "+ str(reg[register_name]) + "\n"
		reg[register_name]= "Memory"
		reg[register_name]=None
	# print 'before freereg'
	# print '\n'
	# print reg
	return asmout

def Input_Data() :
	i=0
	matrix = []
	with open(filename, "r") as fname:
		for line in fname:
			currentline = line.split(",")
			currentline = [x.strip('\n') for x in currentline]
			currentline = [x.strip(' ') for x in currentline]
			currentline = tuple(x for x in currentline if x != '')
			matrix.append([])
			for j in range(0,len(currentline)):
				matrix[i].append(currentline[j])
			i = i+1

	return matrix

data = Input_Data()

des_var_list = []
src_var_list = []

for i in range(0,len(data)):
	if data[i][1] == "ifgoto":
		l= []
		l.append(data[i][4])
		src_var_list = src_var_list + l
	elif data[i][1] in ['print','call','label','return','goto']:
		continue
	elif data[i][1] not in ['call','label','return','goto']:
		src_var_list = src_var_list + data[i][3:]

src_var_list = list(set(src_var_list))

for i in range(0,len(data)):
	if data[i][1] == "ifgoto":
		l = []
		l.append(data[i][3])
		des_var_list = des_var_list + l
	elif data[i][1] == "print":
		des_var_list.append(data[i][2])
	elif data[i][1] in ['call','label','return','endOfCode','goto']:
		continue
	elif data[i][1] not in ['call','label','return','endOfCode','goto']:
		des_var_list.append(data[i][2])

des_var_list = list(set(des_var_list))

var_list = list(set(src_var_list + des_var_list))

var_list = [x for x in var_list if not integer(x)]

leaders = [1,]
for i in range(0,len(data)):
	if data[i][1] == "ifgoto":
		leaders.append(int(data[i][0]))
		leaders.append(int(data[i][len(data[i])-1]))
	if data[i][1] == "goto":
		leaders.append(int(data[i][0]))
		leaders.append(int(data[i][len(data[i])-1]))
	if data[i][1] == "label":
		leaders.append(int(data[i][0]))
leaders.append(len(data))
leaders.sort()

B_Block = [[] for x in range(len(leaders)-1)]
node_block=[[] for x in range(len(leaders)-1)]

for i in range(0,len(leaders)-1):
	for j in range(leaders[i],leaders[i+1]):
		B_Block[i].append(data[j-1])
		node_block[i].append(data[j-1][0])

B_Block[len(leaders)-2].append(data[len(data)-1])
node_block[len(leaders)-2].append(data[len(data)-1][0])

print leaders
print B_Block
print node_block

fs_table = []	

for i in range(0,len(B_Block)):
	Symbol_Table = [[],[],[],[]]
	rev_data = B_Block[i]
	rev_data.reverse()
	for i in range(0,len(rev_data)):
		if rev_data[i][1]  in ['=','+','-','*','/','%%']:
			if rev_data[i][2] not in Symbol_Table[1]:
				Symbol_Table[0].append(rev_data[i][0])
				Symbol_Table[1].append(rev_data[i][2])
				Symbol_Table[2].append("dead")
				Symbol_Table[3].append("None")
			else:
				values = np.array(Symbol_Table[1])
				searchval = rev_data[i][2]
				li =  np.where(values == searchval)[0]
				index = li[(len(li)-1)]
				Symbol_Table[0].append(rev_data[i][0])
				Symbol_Table[1].append(rev_data[i][2])
				Symbol_Table[2].append("dead")
				Symbol_Table[3].append(Symbol_Table[3][index])
			for j in range (3,len(rev_data[i])):
				if rev_data[i][j] in src_var_list:
					Symbol_Table[0].append(rev_data[i][0])
					Symbol_Table[1].append(rev_data[i][j])
					Symbol_Table[2].append("live")
					Symbol_Table[3].append(rev_data[i][0])
		elif rev_data[i][1] == "ifgoto":
			if rev_data[i][3] not in Symbol_Table[1]:
				Symbol_Table[0].append(rev_data[i][0])
				Symbol_Table[1].append(rev_data[i][3])
				Symbol_Table[2].append("dead")
				Symbol_Table[3].append("None")
			else:
				values = np.array(Symbol_Table[1])
				searchval = rev_data[i][3]
				li =  np.where(values == searchval)[0]
				index = li[(len(li)-1)]
				Symbol_Table[0].append(rev_data[i][0])
				Symbol_Table[1].append(rev_data[i][3])
				Symbol_Table[2].append("dead")
				Symbol_Table[3].append(Symbol_Table[3][index])
			if rev_data[i][4] in src_var_list:
				Symbol_Table[0].append(rev_data[i][0])
				Symbol_Table[1].append(rev_data[i][4])
				Symbol_Table[2].append("live")
				Symbol_Table[3].append(rev_data[i][0])
		elif rev_data[i][1] == "print":
			Symbol_Table[0].append(rev_data[i][0])
			Symbol_Table[1].append(rev_data[i][2])
			Symbol_Table[2].append("live")
			Symbol_Table[3].append(rev_data[i][0])
		elif rev_data[i][1] == "return":
			continue
	s_table = [[] for x in range(len(Symbol_Table[1]))]
	
	for j in range(0,len(Symbol_Table[1])):
		for i in range(0,4):
			s_table[j].append(Symbol_Table[i][j])
	
	# print Symbol_Table
	# print s_table
	#print "\n"
	fs_table.append(s_table)
	# print '\n'
	# print fs_table
print fs_table