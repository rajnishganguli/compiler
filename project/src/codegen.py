#!/usr/bin/python
import sys
import os
import numpy as np

if len(sys.argv) == 2:
	filename = str(sys.argv[1])
else:
	print("usage: python codegen.py irfile")
	exit()

reg = ['%eax','%ebx','%ecx', '%edx']
registerDescriptor={}
registerDescriptor = registerDescriptor.fromkeys(reg)
regalwaysinuse={'%esp':None,"%ebp":None}
addressDescriptor = {}
operators = ['+','-','*','/','=','==','<=','>=','>','<','%',"&&","||",'&','|',"!=",'!',"ifgoto","goto","call","return","label","print","endOfCode","function","funcarg","param","pop","retval","vector","member","update","read"]
varlist=[]
vectorlist=[]
global asmout
asmout = ""

global relcount
relcount = 1

def integer(number):
		if number.isdigit() or (number[1:].isdigit() and (number[0] == "-" or number[0] == "+")):
			return 1
		else:
			return 0

def getReg(var, lineno):
	global asmout
	if var in registerDescriptor.values():
		for register in registerDescriptor.keys():
			if registerDescriptor[register] == var:
				return register
	for register in registerDescriptor.keys():
		if registerDescriptor[register] == None:
			return register	
	instrvardict = nextuseTable[lineno-1]
	farthestnextuse = max(instrvardict.keys())
	for var in instrvardict:
		if instrvardict[var] == farthestnextuse:
			break;
	for regspill in registerDescriptor.keys():
		if registerDescriptor[regspill] == var:
			break;
	asmout = asmout + "movl " + regspill + ", " + var + "\n"
	addressDescriptor[var] = "mem"
	return regspill

def getlocation(var):
	return addressDescriptor[var]

def setlocation(var, loc):
	addressDescriptor[var] = loc

def nextuse(var, line):
	return nextuseTable[line-1][var]


def prodAsm(instruction):
		global asmout
		global relcount
		asmout="" # final output of the assembly language
		# tac expected format 
		# < line number, operator, destination, source1, source2 > for the basic mathematical operations with the exception of ifgoto, goto etc.
		#The basic structure given in the sample input in the assignment description is followed in all cases.
		lineNo= int(instruction[0])
		operator=instruction[1]
		if not operator in operators:
		 	print " ; \t\t Operator ", operator, " is not supported.\n ;Skipping the line when writing the assembly code."
		 	#return asmout
		elif operator == '+':
		 	"""add <reg>,<reg>								# a = b + c
			   add <reg>,<mem>								# a = b + 5
			   add <mem>,<reg>								# a = 2 + 5
			   add <reg>,<con>								# a = 5 + b
			   add <mem>,<con>""" # 5 types of syntax possible
			dest = instruction[2]  
			operand1 = instruction[3]
			operand2 = instruction[4]
			if integer(operand1) and integer(operand2):
				# print '1'
			   	destreg = getReg(dest,lineNo)
			   	asmout = asmout + "movl $" + operand1 + ", " + destreg + "\n"
			   	asmout = asmout + "addl $" + operand2 +" , " + destreg + "\n"
			   	registerDescriptor[destreg] = dest
			   	setlocation(dest,destreg)
			elif not integer(operand1) and not integer(operand2):
				# print '2'
			   	destreg = getReg(dest,lineNo)
			   	location1 = getlocation(operand1)
			   	location2 = getlocation(operand2)
			   	# print dest
			   	# print destreg
			   	# print location1
			   	# print location2
			   	if location1 != "mem" and location2 != "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					asmout = asmout + "addl " + location2 + ", " + destreg + "\n"
				elif location1 == "mem" and location2 != "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "addl " + location2 + ", " + destreg + "\n"
				elif location1 != "mem" and location2 == "mem":
					# print "gfhbjn,"
					if location1 == destreg:
						asmout = asmout + "addl " + operand2 + ", " + destreg + "\n"
					else:	
						asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
						asmout = asmout + "addl " + location1 + ", " + destreg + "\n"
				elif location1 == "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "addl " + operand2 + ", " + destreg + "\n"					
				registerDescriptor[destreg] = dest
				setlocation(dest, destreg)
			elif not integer(operand1) and integer(operand2):
				# print '3'
			   	destreg = getReg(dest,lineNo)
			   	location1 = getlocation(operand1)
			   	asmout = asmout + "movl $" + operand2 + ", " + destreg + "\n"
			   	if location1 != "mem":
			   		asmout = asmout + "addl " + location1 + ", " + destreg + "\n"
			   	else:
			   		asmout = asmout + "addl " + operand1 + ", " + destreg + "\n"
			   	registerDescriptor[destreg] = dest
			   	setlocation(dest, destreg)
			elif integer(operand1) and not integer(operand2):
				# print '4'
				destreg = getReg(dest,lineNo)
			   	location2 = getlocation(operand2)
			   	asmout = asmout + "movl $" + operand1 + ", " + destreg + "\n"
			   	if location2 != "mem":
			   		asmout = asmout + "addl " + location2 + ", " + destreg + "\n"
			   	else:
			   		asmout = asmout + "addl " + operand2 + ", " + destreg + "\n"
			   	registerDescriptor[destreg] = dest
			   	setlocation(dest, destreg)
			# for var in varlist:
			# 	location = getlocation(var)
			# 	if location != 'mem':
			# 		asmout = asmout + "movl " + location + ", " + var + "\n"
			# 		setlocation(var,'mem')
			# 		registerDescriptor[location] = None
		elif operator == '-':
		 	dest = instruction[2]
			operand1 = instruction[3]
			operand2 = instruction[4]
			if integer(operand1) and integer(operand2):
			   	destreg=getReg(dest,lineNo)
			   	asmout = asmout + "\t movl $" + operand1 + " , " + destreg + "\n"
			   	asmout= asmout + "\t subl $" + operand2 +" , " + destreg + "\n"
			   	registerDescriptor[destreg]=dest
			   	setlocation(dest, destreg)
			elif not integer(operand1) and not integer(operand2):
			   	destreg = getReg(dest,lineNo)
			   	location1 = getlocation(operand1)
			   	location2 = getlocation(operand2)
			   	if location1 != "mem" and location2 != "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					asmout = asmout + "subl " + location2 + ", " + destreg + "\n"
				elif location1 == "mem" and location2 != "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "subl " + location2 + ", " + destreg + "\n"
				elif location1 != "mem" and location2 == "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					asmout = asmout + "subl " + operand2 + ", " + destreg + "\n"
				elif location1 == "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "subl " + operand2 + ", " + destreg + "\n"					
				registerDescriptor[destreg] = dest
				setlocation(dest, destreg)
			elif not integer(operand1) and integer(operand2):
			   	destreg = getReg(dest,lineNo)
			   	location1 = getlocation(operand1)
			   	if location1 != "mem":
			   		asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
			   	else:
			   		asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
			   	asmout = asmout + "subl $" + operand2 + ", " + destreg + "\n"
			   	registerDescriptor[destreg] = dest
			   	setlocation(dest, destreg)
			elif integer(operand1) and not integer(operand2): 
			   	destreg = getReg(dest,lineNo)
			   	location2 = getlocation(operand2)
			   	asmout = asmout + "movl $" + operand1 + ", " + destreg + "\n"
			   	if location2 != "mem":
			   		asmout = asmout + "subl " + location2 + ", " + destreg + "\n"
			   	else:
			   		asmout = asmout + "subl " + operand2 + ", " + destreg + "\n"
			   	registerDescriptor[destreg] = dest
			   	setlocation(dest, destreg)
			for var in varlist:
				location = getlocation(var)
				if location != 'mem':
					asmout = asmout + "movl " + location + ", " + var + "\n"
					setlocation(var,'mem')
					registerDescriptor[location] = None
		elif operator == '*':
			dest = instruction[2]
			operand1 = instruction[3]
			operand2 = instruction[4]
			if registerDescriptor['%eax'] != None:
					asmout = asmout + "movl %eax, " + registerDescriptor['%eax'] + "\n"
					setlocation(registerDescriptor['%eax'], "mem")
			if registerDescriptor['%edx'] != None:
					asmout = asmout + "movl %edx, " + registerDescriptor['%edx'] + "\n"
					setlocation(registerDescriptor['%edx'], "mem")
			if not integer(operand1):
				location1 = getlocation(operand1)
				setlocation(operand1, "mem")
			if not integer(operand2):
				location2 = getlocation(operand2)
				setlocation(operand2, "mem")
			if not integer(operand1) and not integer(operand2):
				# print "1"
				asmout = asmout + "movl " + operand1 + ", %eax \n"
				asmout = asmout + "movl " + operand2 + ", %edx \n"
				asmout = asmout + "imul %edx \n"
				setlocation(dest, '%eax')
			elif integer(operand1) and not integer(operand2):
				# print "2"
				asmout = asmout + "movl $" + (operand1) + ", %eax \n"
				asmout = asmout + "movl " + operand2 + ", %edx \n"
				asmout = asmout + "imul %edx \n"
				setlocation(dest, '%eax')
			elif not integer(operand1) and integer(operand2):
				# print "3"
				asmout = asmout + "movl " + operand1 + ", %eax \n"
				asmout = asmout + "movl $" + (operand2) + ", %edx \n"
				asmout = asmout + "imul %edx \n"
				setlocation(dest, '%eax')
			else:
				# print "4"
				asmout = asmout + "movl $" + (operand1) + ", %eax \n"
				asmout = asmout + "movl $" + (operand2) + ", %edx \n"
				asmout = asmout + "imul %edx \n"
				setlocation(dest, '%eax')
			# asmout = asmout + "movl %eax, " + dest + "\n"
			# registerDescriptor['%eax'] = None
			# addressDescriptor[dest] = 'mem'
			# for var in varlist:
			# 	location = getlocation(var)
			# 	if location != 'mem':
			# 		asmout = asmout + "movl " + location + ", " + var + "\n"
			# 		setlocation(var,'mem')
			# 		registerDescriptor[location] = None
		elif operator == '/':
			dest = instruction[2]
			operand1 = instruction[3]
			operand2 = instruction[4]
			if registerDescriptor['%eax'] != None:
				asmout = asmout + "movl %eax, " + registerDescriptor['%eax'] + "\n"
				setlocation(registerDescriptor['%eax'], "mem")
			if registerDescriptor['%edx'] != None:
				asmout = asmout + "movl %edx, " + registerDescriptor['%edx'] + "\n"
				setlocation(registerDescriptor['%edx'], "mem")
			if registerDescriptor['%ecx'] != None:
				asmout = asmout + "movl %ecx, " + registerDescriptor['%ecx'] + "\n"
				setlocation(registerDescriptor['%ecx'], "mem")
			if not integer(operand1):
				location1 = getlocation(operand1)
				setlocation(operand1, "mem")
			if not integer(operand2):
				location2 = getlocation(operand2)
				setlocation(operand2, "mem")
			asmout = asmout + "movl $0, %edx \n"
			if not integer(operand1) and not integer(operand2):
				asmout = asmout + "movl " + operand1 + ", %eax \n"
				asmout = asmout + "movl " + operand2 + ", %ecx \n"
				asmout = asmout + "idiv %ecx \n"
				setlocation(dest, '%eax')
			elif integer(operand1) and not integer(operand2):
				asmout = asmout + "movl $" + (operand1) + ", %eax \n"
				asmout = asmout + "movl " + operand2 + ", %ecx \n"
				asmout = asmout + "idiv %ecx \n"
				setlocation(dest, '%eax')
			elif not integer(operand1) and integer(operand2):
				location1 = getlocation(operand1)
				asmout = asmout + "movl " + operand1 + ", %eax \n"
				asmout = asmout + "movl $" + (operand2) + ", %ecx \n"
				asmout = asmout + "idiv %ecx \n"
				setlocation(dest, '%eax')
			else:
				ansdiv = int(int(operand1)/int(operand2))
				asmout = asmout + "movl $" + str(ansdiv) + ", %eax \n"
				setlocation(dest, '%eax')
			# asmout = asmout + "movl %eax, " + dest + "\n"
			# registerDescriptor['%eax'] = None
			# addressDescriptor[dest] = 'mem'
			for var in varlist:
				location = getlocation(var)
				if location != 'mem':
					asmout = asmout + "movl " + location + ", " + var + "\n"
					setlocation(var,'mem')
					registerDescriptor[location] = None
		elif operator == '%':
			dest = instruction[2]
			operand1 = instruction[3]
			operand2 = instruction[4]
			if registerDescriptor['%eax'] != None:
				asmout = asmout + "movl %eax, " + registerDescriptor['%eax'] + "\n"
				setlocation(registerDescriptor['%eax'], "mem")
			if registerDescriptor['%edx'] != None:
				asmout = asmout + "movl %edx, " + registerDescriptor['%edx'] + "\n"
				setlocation(registerDescriptor['%edx'], "mem")
			if registerDescriptor['%ecx'] != None:
				asmout = asmout + "movl %ecx, " + registerDescriptor['%ecx'] + "\n"
				setlocation(registerDescriptor['%ecx'], "mem")
			if not integer(operand1):
				location1 = getlocation(operand1)
				setlocation(operand1, "mem")
			if not integer(operand2):
				location2 = getlocation(operand2)
				setlocation(operand2, "mem")
			asmout = asmout + "movl $0, %edx \n"
			if not integer(operand1) and not integer(operand2):
				asmout = asmout + "movl " + operand1 + ", %eax \n"
				asmout = asmout + "movl " + operand2 + ", %ecx \n"
				asmout = asmout + "idiv %ecx \n"
				setlocation(dest, '%edx')
			elif integer(operand1) and not integer(operand2):
				asmout = asmout + "movl $" + (operand1) + ", %eax \n"
				asmout = asmout + "movl " + operand2 + ", %ecx \n"
				asmout = asmout + "idiv %ecx \n"
				setlocation(dest, '%edx')
			elif not integer(operand1) and integer(operand2):
				location1 = getlocation(operand1)
				asmout = asmout + "movl " + operand1 + ", %eax \n"
				asmout = asmout + "movl $" + (operand2) + ", %ecx \n"
				asmout = asmout + "idiv %ecx \n"
				setlocation(dest, '%edx')
			else:
				ansdiv = int(int(operand1)%int(operand2))
				asmout = asmout + "movl $" + str(ansdiv) + ", %edx \n"
				setlocation(dest, '%edx')
			# asmout = asmout + "movl %edx, " + dest + "\n"
			# registerDescriptor['%edx'] = None
			# addressDescriptor[dest] = 'mem'
			for var in varlist:
				location = getlocation(var)
				if location != 'mem':
					asmout = asmout + "movl " + location + ", " + var + "\n"
					setlocation(var,'mem')
					registerDescriptor[location] = None
		elif operator == "=":
			dest = instruction[2]
			src = instruction[3]
			location1 = getlocation(dest)
			if integer(src):
				if location1 == "mem":
					asmout = asmout + "movl $" + src + ", " + dest + "\n"
				else:
					asmout = asmout + "movl $" + src + ", " + location1 + "\n"
			else:
				location2 = getlocation(src)
				if location1 == "mem" and location2 == "mem":				
					destreg = getReg(dest, lineNo)
					asmout = asmout + "movl " + src + ", " + destreg + "\n"
					registerDescriptor[destreg] = dest
					setlocation(dest, destreg)			
				elif location1 == "mem" and location2 != "mem":
					destreg = getReg(dest, lineNo)
					asmout = asmout + "movl " + location2 + ", " + destreg + "\n"
					registerDescriptor[destreg] = dest
					setlocation(dest, destreg)
				elif location1 != "mem" and location2 == "mem":
					asmout = asmout + "movl " + src + ", " + location1 + "\n"
				elif location1 != "mem" and location2 != "mem":
					asmout = asmout + "movl " + location2 + ", " + location1 + "\n"
			for var in varlist:
				location = getlocation(var)
				if location != 'mem':
					asmout = asmout + "movl " + location + ", " + var + "\n"
					setlocation(var,'mem')
					registerDescriptor[location] = None
		elif operator == "ifgoto":
			for var in varlist:
				location = getlocation(var)
				if location != "mem":
					asmout = asmout + "movl " + location + ", " + var + "\n"
					setlocation(var, "mem")
			operatorin = instruction[2]	
			if operatorin == "==" or operatorin == ">=" or operatorin == "<=" or operatorin == ">" or operatorin == "<" or operatorin == "!=":
				operand1 = instruction[3]
				operand2 = instruction[4]
				gotolocation = instruction[5]
				if integer(operand1) and integer(operand2):
				   	asmout = asmout + "cmp $" + operand2 + ", $" + operand1 + "\n"
				elif not integer(operand1) and not integer(operand2):
					location1 = getlocation(operand1)
					location2 = getlocation(operand2)
					destreg = getReg(operand1, lineNo)
					if location1 != "mem":
						asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					else:
						asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					if location2 != "mem":
						asmout = asmout + "cmp " + location2 + ", " + destreg + "\n"
					else:
						asmout = asmout + "cmp " + operand2 + ", " + destreg + "\n"
					registerDescriptor[destreg] = operand1
					setlocation(operand1, destreg)
				elif not integer(operand1) and integer(operand2):
				   	location1 = getlocation(operand1)
					if location1 != "mem":
						asmout = asmout + "cmp $" + operand2 + ", " + location1 + "\n"
					else:
						asmout = asmout + "cmp $" + operand2 + ", " + operand1 + "\n"
				else:
				   	location2 = getlocation(operand2)
					if location2 != "mem":
						asmout = asmout + "cmp $" + location2 + ", " + operand1 + "\n"
					else:
						asmout = asmout + "cmp $" + operand2 + ", " + operand1 + "\n"
				
				for var in varlist:
					location = getlocation(var)
					if location != "mem":
						asmout = asmout + "movl " + location + ", " + var + "\n"
						setlocation(var, "mem")
				if operatorin == "==":
				   	if(integer(gotolocation)):
						asmout = asmout + "je  Loop" + gotolocation +"\n" 
					else:
						asmout = asmout + "je " + gotolocation +"\n"
				elif operatorin == "<=":
				   	if(integer(gotolocation)):
						asmout = asmout + "jle  Loop" + gotolocation +"\n" 
					else:
						asmout = asmout + "jle " + gotolocation +"\n"
				elif operatorin == "<":
					if(integer(gotolocation)):
						asmout = asmout + "jl  Loop" + gotolocation +"\n" 
					else:
						asmout = asmout + "jl " + gotolocation +"\n"
				elif operatorin == ">=":
				   	if(integer(gotolocation)):
						asmout = asmout + "jge  Loop" + gotolocation +"\n" 
					else:
						asmout = asmout + "jge " + gotolocation +"\n"
				elif operatorin == ">":
				   	if(integer(gotolocation)):
						asmout = asmout + "jg  Loop" + gotolocation +"\n" 
					else:
						asmout = asmout + "jg " + gotolocation +"\n"
				elif operatorin == "!=":
				   	if(integer(gotolocation)):
						asmout = asmout + "jne  Loop" + gotolocation +"\n" 
					else:
						asmout = asmout + "jne " + gotolocation +"\n"	
		elif operator == "goto":
			destlocation = instruction[2]
			for var in varlist:
				location = getlocation(var)
				if location != "mem":
					asmout = asmout + "movl " + location + ", " + var + "\n"
					setlocation(var, "mem")
			if(integer(destlocation)):
				asmout = asmout + "jmp  Loop" + destlocation +"\n"
			else:
				asmout = asmout + "jmp  " + destlocation +"\n"
		elif operator == "label":
			label = instruction[2]
			asmout = asmout +  label + ":\n"
		elif operator == '>':
			for var in varlist:
				location = getlocation(var)
				if location != "mem":
					asmout = asmout + "movl " + location + ", " + var + "\n"
					setlocation(var, "mem")
					registerDescriptor[location] = None
			dest = instruction[2]
			operand1 = instruction[3]
			operand2 = instruction[4]
			LT = "LT"+str(relcount)
			NLT = "NLT"+str(relcount)
			if integer(operand1) and integer(operand2):
				#case: dest = 4 < 5
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				asmout = asmout + "movl $" + str(int(int(operand1)>int(operand2))) + ", " + destreg + "\n"
				# Update the address descriptor entry for dest variable to say where it is stored no
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)
			elif integer(operand1) and not integer(operand2):
				#case: dest = 5 < x
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location2 = getlocation(operand2)
				# Move the first operand to the destination register
				asmout = asmout + "movl $" + operand1 + ", " + destreg + "\n"
				if location2 != "mem":
					asmout = asmout + "cmpl " + destreg + ", " + location2 + "\n"
				else:
					asmout = asmout + "cmpl " + destreg + ", " + operand2 + "\n"
				asmout = asmout + "jg " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and integer(operand2):
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location1 = getlocation(operand1)
				# Move the first operand to the destination register
				asmout = asmout + "movl $" + operand2 + ", " + destreg + "\n"
				# Add the other operand to the register content
				if location1 != "mem":
					asmout = asmout + "cmpl " + destreg + ", " + location1 + "\n"
				else:
					asmout = asmout + "cmpl " + destreg + ", " + operand1 + "\n"
				asmout = asmout + "jg " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and not integer(operand2):
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				# Get the locations of the operands
				location1 = getlocation(operand1)
				location2 = getlocation(operand2)
				if location1 != "mem" and location2 != "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + destreg + ", " + location2 + "\n"
				elif location1 == "mem" and location2 != "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + destreg + ", " + location2 + "\n"
				elif location1 != "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + destreg + ", " + location1 + "\n"
				elif location1 == "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + destreg + ", " + operand1 + "\n"					
				# Update the register descriptor entry for destreg to say that it contains the dest
				asmout = asmout + "jg " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				# Update the address descriptor entry for dest variable to say where it is stored now
				setlocation(dest, destreg)
			relcount = relcount + 1



			 # 	elif operatorin == '&&'or operatorin == '&' :

			 # 	   operand1 = instruction[3]
				#    operand2 = instruction[4]
				#    gotoloc = instruction[5]
			 # 	   #dest = instruction[2]
				#    #operand1 = instruction[3]
				#    #operand2 = instruction[4]
				#    if integer(operand1) and integer(operand2):
				#    	destreg=getreg(operand1,instruction[0])
				#    	asmout = asmout + "\t movl $" + operand1 + ", " + destreg + "\n"
				#    	#reg[destreg]=int(operand1)
				#    	asmout= asmout + "\t andl $" + operand2 +", " + destreg + "\n"
				#    	reg[destreg]=operand1
				#    elif not integer(operand1) and not integer(operand2):
				#    	destreg=getreg(operand1,instruction[0])
				#    	#regop1 = getreg(operand1)
				#    	regop2 = getreg(operand2,instruction[0])
				#    	reg[regop2]=operand2
				#    	asmout = asmout + "\t movl " + operand1 + "," + destreg+ "\n"
				#    	reg[destreg]=operand1
				#    	asmout = asmout + "\t movl " + operand2 + "," + regop2 + "\n"
				#    	asmout = asmout + "\t andl " + regop2 + "," + destreg + "\n"
				#    	reg[destreg]= operand1 
				#    elif not integer(operand1) and integer(operand2):
				#    	destreg=getreg(operand1,instruction[0])
				#    	asmout = asmout + "\t movl " + operand1 + "," + destreg+ "\n"
				#    	reg[destreg]=operand1
				#    	asmout = asmout + "\t andl $" + operand2 + "," + destreg + "\n"
				#    	reg[destreg]= operand1
				#    else: #op1 integer and op2 not integer
				#    	destreg=getreg(operand2,instruction[0])
				#    	asmout = asmout + "\t movl " + operand2 + "," + destreg+ "\n"
				#    	reg[destreg]=operand2
				#    	asmout = asmout + "\t andl $" + operand1 + "," + destreg + "\n"
				#    	reg[destreg]= operand1
				#    asmout=asmout+"\t jnz  Loop"+gotoloc +"\n"

			 # 	elif operatorin == '||' or operatorin == '|':

			 # 	   operand1 = instruction[3]
				#    operand2 = instruction[4]
				#    gotoloc = instruction[5]

			 # 	   if (integer(operand1) and integer(operand2)):
				#    		destreg=getreg(operand1,instruction[0])
				#    		asmout = asmout + "\t movl $" + operand1 + ", " + destreg + "\n"
				#    		#reg[destreg]=int(operand1)
				#    		asmout= asmout + "\t orl $" + operand2 +", " + destreg + "\n"
				#    		reg[destreg]=operand1
				#    elif not integer(operand1) and not integer(operand2):
				#    		destreg=getreg(operand1,instruction[0])
				#    		#regop1 = getreg(operand1)
				#    		regop2 = getreg(operand2,instruction[0])
				#    		reg[regop2]=operand2
				#    		asmout = asmout + "\t movl " + operand1 + "," + destreg+ "\n"
				#    		reg[destreg]=operand1
				#    		asmout = asmout + "\t movl " + operand2 + "," + regop2 + "\n"
				#    		asmout = asmout + "\t orl " + regop2 + "," + destreg + "\n"
				#    		reg[destreg]= operand1 
				#    elif not integer(operand1) and integer(operand2):
				#    		destreg=getreg(operand1,instruction[0])
				# 	   	asmout = asmout + "\t movl " + operand1 + "," + destreg+ "\n"
				# 	   	reg[destreg]=operand1
				# 	   	asmout = asmout + "\t orl $" + operand2 + "," + destreg + "\n"
				#    		reg[destreg]= operand1
				#    else: #op1 integer and op2 not integer
				#    		destreg=getreg(operand2,instruction[0])
				#    		asmout = asmout + "\t movl " + operand2 + "," + destreg+ "\n"
				#    		reg[destreg]=operand2
				#    		asmout = asmout + "\t orl $" + operand1 + "," + destreg + "\n"
				#    		reg[destreg]= operand1

				#    asmout=asmout+"\t jnz  Loop"+gotoloc +"\n"

		  #       	elif operatorin == '!':

		  #       	   operand1 = instruction[3]
				#    #operand2 = instruction[4]
				#    gotoloc = instruction[4]

			 #     	   #dest=instruction[2]
		  #       	   destreg = getreg(operand1,instruction[0]) 
		  #       	   if integer(operand1):
		  #       	   	asmout = asmout + "\t movl $" + operand1 + " , " + destreg + "\n"
			 # 		asmout = asmout + "\t notl " + destreg + "\n"
			 # 	   else:
			 # 	   	asmout = asmout + "\t movl " + operand1 + " , " + destreg + "\n"
			 # 		asmout = asmout + "\t notl " + destreg + "\n"
			 # 	   reg[destreg]=operand1
			 # 	   asmout=asmout+"\t jnz  Loop"+gotoloc +"\n"
		elif operator == '<':
			for var in varlist:
				location = getlocation(var)
				if location != "mem":
					asmout = asmout + "movl " + location + ", " + var + "\n"
					setlocation(var, "mem")
					registerDescriptor[location] = None
			dest = instruction[2]
			operand1 = instruction[3]
			operand2 = instruction[4]
			LT = "LT"+str(relcount)
			NLT = "NLT"+str(relcount)
			if integer(operand1) and integer(operand2):
				#case: dest = 4 < 5
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				asmout = asmout + "movl $" + str(int(int(operand1)<int(operand2))) + ", " + destreg + "\n"
				# Update the address descriptor entry for dest variable to say where it is stored no
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)
			elif integer(operand1) and not integer(operand2):
				#case: dest = 5 < x
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location2 = getlocation(operand2)
				# Move the first operand to the destination register
				asmout = asmout + "movl $" + operand1 + ", " + destreg + "\n"
				if location2 != "mem":
					asmout = asmout + "cmpl " + destreg + ", " + location2 + "\n"
				else:
					asmout = asmout + "cmpl " + destreg + ", " + operand2 + "\n"
				asmout = asmout + "jl " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and integer(operand2):
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location1 = getlocation(operand1)
				# Move the first operand to the destination register
				asmout = asmout + "movl $" + operand2 + ", " + destreg + "\n"
				# Add the other operand to the register content
				if location1 != "mem":
					asmout = asmout + "cmpl " + destreg + ", " + location1 + "\n"
				else:
					asmout = asmout + "cmpl " + destreg + ", " + operand1 + "\n"
				asmout = asmout + "jl " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and not integer(operand2):
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				# Get the locations of the operands
				location1 = getlocation(operand1)
				location2 = getlocation(operand2)
				if location1 != "mem" and location2 != "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + destreg + ", " + location2 + "\n"
				elif location1 == "mem" and location2 != "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + destreg + ", " + location2 + "\n"
				elif location1 != "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + destreg + ", " + location1 + "\n"
				elif location1 == "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + destreg + ", " + operand1 + "\n"				
				# Update the register descriptor entry for destreg to say that it contains the dest
				asmout = asmout + "jl " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				# Update the address descriptor entry for dest variable to say where it is stored now
				setlocation(dest, destreg)
			relcount = relcount + 1			
		elif operator == '>=':
			for var in varlist:
				location = getlocation(var)
				if location != "mem":
					asmout = asmout + "movl " + location + ", " + var + "\n"
					setlocation(var, "mem")
					registerDescriptor[location] = None
			dest = instruction[2]
			operand1 = instruction[3]
			operand2 = instruction[4]
			LT = "LT"+str(relcount)
			NLT = "NLT"+str(relcount)
			if integer(operand1) and integer(operand2):
				#case: dest = 4 < 5
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				asmout = asmout + "movl $" + str(int(int(operand1)>=int(operand2))) + ", " + destreg + "\n"
				# Update the address descriptor entry for dest variable to say where it is stored no
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)
			elif integer(operand1) and not integer(operand2):
				#case: dest = 5 < x
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location2 = getlocation(operand2)
				# Move the first operand to the destination register
				asmout = asmout + "movl $" + operand1 + ", " + destreg + "\n"
				if location2 != "mem":
					asmout = asmout + "cmpl " + destreg + ", " + location2 + "\n"
				else:
					asmout = asmout + "cmpl " + destreg + ", " + operand2 + "\n"
				asmout = asmout + "jge " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and integer(operand2):
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location1 = getlocation(operand1)
				# Move the first operand to the destination register
				asmout = asmout + "movl $" + operand2 + ", " + destreg + "\n"
				# Add the other operand to the register content
				if location1 != "mem":
					asmout = asmout + "cmpl " + destreg + ", " + location1 + "\n"
				else:
					asmout = asmout + "cmpl " + destreg + ", " + operand1 + "\n"
				asmout = asmout + "jge " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and not integer(operand2):
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				# Get the locations of the operands
				location1 = getlocation(operand1)
				location2 = getlocation(operand2)
				if location1 != "mem" and location2 != "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + destreg + ", " + location2 + "\n"
				elif location1 == "mem" and location2 != "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + destreg + ", " + location2 + "\n"
				elif location1 != "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + destreg + ", " + location1 + "\n"
				elif location1 == "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + destreg + ", " + operand1 + "\n"					
				# Update the register descriptor entry for destreg to say that it contains the dest
				asmout = asmout + "jge " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				# Update the address descriptor entry for dest variable to say where it is stored now
				setlocation(dest, destreg)
			relcount = relcount + 1
		elif operator == '<=':
			for var in varlist:
				location = getlocation(var)
				if location != "mem":
					asmout = asmout + "movl " + location + ", " + var + "\n"
					setlocation(var, "mem")
					registerDescriptor[location] = None
			dest = instruction[2]
			operand1 = instruction[3]
			operand2 = instruction[4]
			LT = "LT"+str(relcount)
			NLT = "NLT"+str(relcount)
			if integer(operand1) and integer(operand2):
				#case: dest = 4 < 5
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				asmout = asmout + "movl $" + str(int(int(operand1)<=int(operand2))) + ", " + destreg + "\n"
				# Update the address descriptor entry for dest variable to say where it is stored no
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)
			elif integer(operand1) and not integer(operand2):
				#case: dest = 5 < x
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location2 = getlocation(operand2)
				# Move the first operand to the destination register
				asmout = asmout + "movl $" + operand1 + ", " + destreg + "\n"
				if location2 != "mem":
					asmout = asmout + "cmpl " + destreg + ", " + location2 + "\n"
				else:
					asmout = asmout + "cmpl " + destreg + ", " + operand2 + "\n"
				asmout = asmout + "jle " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp" + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and integer(operand2):
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location1 = getlocation(operand1)
				# Move the first operand to the destination register
				asmout = asmout + "movl $" + operand2 + ", " + destreg + "\n"
				# Add the other operand to the register content
				if location1 != "mem":
					asmout = asmout + "cmpl " + destreg + ", " + location1 + "\n"
				else:
					asmout = asmout + "cmpl " + destreg + ", " + operand1 + "\n"
				asmout = asmout + "jle " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and not integer(operand2):
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				# Get the locations of the operands
				location1 = getlocation(operand1)
				location2 = getlocation(operand2)
				if location1 != "mem" and location2 != "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + destreg + ", " + location2 + "\n"
				elif location1 == "mem" and location2 != "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + destreg + ", " + location2 + "\n"
				elif location1 != "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + destreg + ", " + location1 + "\n"
				elif location1 == "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + destreg + ", " + operand1 + "\n"					
				# Update the register descriptor entry for destreg to say that it contains the dest
				asmout = asmout + "jle " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				# Update the address descriptor entry for dest variable to say where it is stored now
				setlocation(dest, destreg)
			relcount = relcount + 1
		elif operator == '==':
			dest = instruction[2]
			operand1 = instruction[3]
			operand2 = instruction[4]
			LT = "LT"+str(relcount)
			NLT = "NLT"+str(relcount)
			if integer(operand1) and integer(operand2):
				#case: dest = 4 < 5
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				asmout = asmout + "movl $" + str(int(int(operand1)==int(operand2))) + ", " + destreg + "\n"
				# Update the address descriptor entry for dest variable to say where it is stored no
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)
			elif integer(operand1) and not integer(operand2):
				#case: dest = 5 < x
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location2 = getlocation(operand2)
				# Move the first operand to the destination register
				asmout = asmout + "movl $" + operand1 + ", " + destreg + "\n"
				if location2 != "mem":
					asmout = asmout + "cmpl " + location2 + ", " + destreg + "\n"
				else:
					asmout = asmout + "cmpl " + operand2 + ", " + destreg + "\n"
				asmout = asmout + "je " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp" + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and integer(operand2):
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location1 = getlocation(operand1)
				# Move the first operand to the destination register
				asmout = asmout + "movl $" + operand2 + ", " + destreg + "\n"
				# Add the other operand to the register content
				if location1 != "mem":
					asmout = asmout + "cmpl " + location1 + ", " + destreg + "\n"
				else:
					asmout = asmout + "cmpl " + operand1 + ", " + destreg + "\n"
				asmout = asmout + "je " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and not integer(operand2):
				destreg = getReg(dest, lineNo)
				location1 = getlocation(operand1)
				location2 = getlocation(operand2)
				if location1 != "mem" and location2 != "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + location2 + ", " + destreg + "\n"
				elif location1 == "mem" and location2 != "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + location2 + ", " + destreg + "\n"
				elif location1 != "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + location1 + ", " + destreg + "\n"
				elif location1 == "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + operand1 + ", " + destreg + "\n"
				asmout = asmout + "je " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)
			relcount = relcount + 1
			for var in varlist:
				location = getlocation(var)
				if location != "mem":
					asmout = asmout + "movl " + location + ", " + var + "\n"
					setlocation(var, "mem")
					registerDescriptor[location] = None
		elif operator == '!=':
			for var in varlist:
				location = getlocation(var)
				if location != "mem":
					asmout = asmout + "movl " + location + ", " + var + "\n"
					setlocation(var, "mem")
					registerDescriptor[location] = None			
			dest = instruction[2]
			operand1 = instruction[3]
			operand2 = instruction[4]
			LT = "LT"+str(relcount)
			NLT = "NLT"+str(relcount)
			if integer(operand1) and integer(operand2):
				#case: dest = 4 < 5
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				asmout = asmout + "movl $" + str(int(int(operand1)!=int(operand2))) + ", " + destreg + "\n"
				# Update the address descriptor entry for dest variable to say where it is stored no
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)
			elif integer(operand1) and not integer(operand2):
				#case: dest = 5 < x
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location2 = getlocation(operand2)
				# Move the first operand to the destination register
				asmout = asmout + "movl $" + operand1 + ", " + destreg + "\n"
				if location2 != "mem":
					asmout = asmout + "cmpl " + location2 + ", " + destreg + "\n"
				else:
					asmout = asmout + "cmpl " + operand2 + ", " + destreg + "\n"
				asmout = asmout + "jne " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and integer(operand2):
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location1 = getlocation(operand1)
				# Move the first operand to the destination register
				asmout = asmout + "movl $" + operand2 + ", " + destreg + "\n"
				# Add the other operand to the register content
				if location1 != "mem":
					asmout = asmout + "cmpl " + location1 + ", " + destreg + "\n"
				else:
					asmout = asmout + "cmpl " + operand1 + ", " + destreg + "\n"
				asmout = asmout + "jne " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and not integer(operand2):
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				# Get the locations of the operands
				location1 = getlocation(operand1)
				location2 = getlocation(operand2)
				if location1 != "mem" and location2 != "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + location2 + ", " + destreg + "\n"
				elif location1 == "mem" and location2 != "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + location2 + ", " + destreg + "\n"
				elif location1 != "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + location1 + ", " + destreg + "\n"
				elif location1 == "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
					asmout = asmout + "cmpl " + operand1 + ", " + destreg + "\n"					
				# Update the register descriptor entry for destreg to say that it contains the dest
				asmout = asmout + "jne " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				# Update the address descriptor entry for dest variable to say where it is stored now
				setlocation(dest, destreg)
			relcount = relcount + 1
		elif operator == "&":
			#LineNo, &&, dest, op1, op2
			dest = instruction[2]
			operand1 = instruction[3]		#num
			operand2 = instruction[4]		#count
			if integer(operand1) and integer(operand2):
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				asmout = asmout + "movl $" + str(int(operand1) and int(operand2)) + ", " + destreg + "\n"
				# Update the address descriptor entry for dest variable to say where it is stored no
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)
			elif integer(operand1) and not integer(operand2):
				#case dest = 0 && x
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location1 = getlocation(operand2)
				# Move 5 to dest, dest = 5
				asmout = asmout + "movl $" + operand1 + ", " + destreg + "\n"
				#perform logical and, dest = dest >> x
				if location1 != "mem":
					asmout = asmout + "and " + location1 + ", " + destreg + "\n"
				else:
					asmout = asmout + "and " + operand2 + ", " + destreg + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and integer(operand2):
				#case dest = a && 2
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location1 = getlocation(operand1)
				# Move a to destreg, dest = a
				if location1 != "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
				else:
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
				# Perform Logical and dest = dest && 2
				asmout = asmout + "and $" + destreg + ", " + operand2 + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and not integer(operand2):
				#case dest = a && b
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				# Get the locations of the operands
				location1 = getlocation(operand1)
				location2 = getlocation(operand2)
				if location1 != "mem" and location2 != "mem":
					#dest = a and dest = dest && b
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					asmout = asmout + "and " + location2 + ", " + destreg + "\n"
				elif location1 == "mem" and location2 != "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "and " + location2 + ", " + destreg + "\n"
				elif location1 != "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "and " + location2 + ", " + destreg + "\n"
				elif location1 == "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "and " + operand2 + ", " + destreg + "\n"					
				# Update the register descriptor entry for destreg to say that it contains the dest
				registerDescriptor[destreg]=dest
				# Update the address descriptor entry for dest variable to say where it is stored now
				setlocation(dest, destreg)
		elif operator == "|":
			#LineNo, ||, dest, op1, op2
			dest = instruction[2]
			operand1 = instruction[3]		#op1
			operand2 = instruction[4]		#op2
			if integer(operand1) and integer(operand2):
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				asmout = asmout + "movl $" + str(int(operand1) or int(operand2)) + ", " + destreg + "\n"
				# Update the address descriptor entry for dest variable to say where it is stored no
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)
			elif integer(operand1) and not integer(operand2):
				#case dest = 0 || x
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location1 = getlocation(operand2)
				# Move 5 to dest, dest = 5
				asmout = asmout + "movl $" + operand1 + ", " + destreg + "\n"
				#perform logical and, dest = dest || x
				if location1 != "mem":
					asmout = asmout + "or " + destreg + ", " + location1 + "\n"
				else:
					asmout = asmout + "or " + operand2 + ", " + destreg + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and integer(operand2):
				#case dest = a || 2
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location1 = getlocation(operand1)
				# Move a to destreg, dest = a
				if location1 != "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
				else:
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
				# Perform Logical and dest = dest || 2
				asmout = asmout + "or $" + operand2 + ", " + destreg + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and not integer(operand2):
				#case dest = a || b
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				# Get the locations of the operands
				location1 = getlocation(operand1)
				location2 = getlocation(operand2)
				if location1 != "mem" and location2 != "mem":
					#dest = a and dest = dest || b
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					asmout = asmout + "or " + location2 + ", " + destreg + "\n"
				elif location1 == "mem" and location2 != "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					asmout = asmout + "or " + operand2 + ", " + destreg + "\n"
				elif location1 != "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "or " + location2 + ", " + destreg + "\n"
				elif location1 == "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "or " + operand2 + ", " + destreg + "\n"					
				# Update the register descriptor entry for destreg to say that it contains the dest
				registerDescriptor[destreg]=dest
				# Update the address descriptor entry for dest variable to say where it is stored now
				setlocation(dest, destreg)
		elif operator == '&&':
			dest = instruction[2]
			operand1 = instruction[3]
			operand2 = instruction[4]
			LT = "LT"+str(relcount)
			NLT = "NLT"+str(relcount)
			if integer(operand1) and integer(operand2):
				destreg = getReg(dest, lineNo)
				asmout = asmout + "movl $" + str(int(int(operand1) and int(operand2))) + ", " + destreg + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)
			elif integer(operand1) and not integer(operand2):
				destreg = getReg(dest, lineNo)
				location2 = getlocation(operand2)
				asmout = asmout + "movl $" + operand1 + ", " + destreg + "\n"
				asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
				asmout = asmout + "je " + LT + "\n"
				if location2 != "mem":
					asmout = asmout + "movl " + location2 + ", " + destreg + "\n"
				else:
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
				asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
				asmout = asmout + "je " + LT + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and integer(operand2):
				destreg = getReg(dest, lineNo)
				location1 = getlocation(operand1)
				if location1 != "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
				else:
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
				asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
				asmout = asmout + "je " + LT + "\n"
				asmout = asmout + "movl $" + operand2 + ", " + destreg + "\n"
				asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
				asmout = asmout + "je " + LT + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and not integer(operand2):
				destreg = getReg(dest, lineNo)
				location1 = getlocation(operand1)
				location2 = getlocation(operand2)
				if location1 != "mem" and location2 != "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
					asmout = asmout + "je " + LT + "\n"
					asmout = asmout + "movl " + location2 + ", " + destreg + "\n"
					asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
					asmout = asmout + "je " + LT + "\n"
					asmout = asmout + "movl $1, " + destreg + "\n"
					asmout = asmout + "jmp " + NLT + "\n"
					asmout = asmout + LT + ":" + "\n"
					asmout = asmout + "movl $0, " + destreg + "\n"
					asmout = asmout + NLT + ":" + "\n"
				elif location1 == "mem" and location2 != "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
					asmout = asmout + "je " + LT + "\n"
					asmout = asmout + "movl " + location2 + ", " + destreg + "\n"
					asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
					asmout = asmout + "je " + LT + "\n"
					asmout = asmout + "movl $1, " + destreg + "\n"
					asmout = asmout + "jmp " + NLT + "\n"
					asmout = asmout + LT + ":" + "\n"
					asmout = asmout + "movl $0, " + destreg + "\n"
					asmout = asmout + NLT + ":" + "\n"
				elif location1 != "mem" and location2 == "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
					asmout = asmout + "je " + LT + "\n"
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
					asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
					asmout = asmout + "je " + LT + "\n"
					asmout = asmout + "movl $1, " + destreg + "\n"
					asmout = asmout + "jmp " + NLT + "\n"
					asmout = asmout + LT + ":" + "\n"
					asmout = asmout + "movl $0, " + destreg + "\n"
					asmout = asmout + NLT + ":" + "\n"
				elif location1 == "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
					asmout = asmout + "je " + LT + "\n"
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
					asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
					asmout = asmout + "je " + LT + "\n"
					asmout = asmout + "movl $1, " + destreg + "\n"
					asmout = asmout + "jmp " + NLT + "\n"
					asmout = asmout + LT + ":" + "\n"
					asmout = asmout + "movl $0, " + destreg + "\n"
					asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)
			relcount = relcount + 1
			for var in varlist:
				location = getlocation(var)
				if location != "mem":
					asmout = asmout + "movl " + location + ", " + var + "\n"
					setlocation(var, "mem")
					registerDescriptor[location]=None
		elif operator == '||':
			dest = instruction[2]
			operand1 = instruction[3]
			operand2 = instruction[4]
			LT = "LT"+str(relcount)
			NLT = "NLT"+str(relcount)
			if integer(operand1) and integer(operand2):
				destreg = getReg(dest, lineNo)
				asmout = asmout + "movl $" + str(int(int(operand1) or int(operand2))) + ", " + destreg + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)
			elif integer(operand1) and not integer(operand2):
				destreg = getReg(dest, lineNo)
				location2 = getlocation(operand2)
				asmout = asmout + "movl $" + operand1 + ", " + destreg + "\n"
				asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
				asmout = asmout + "jne " + LT + "\n"
				if location2 != "mem":
					asmout = asmout + "movl " + location2 + ", " + destreg + "\n"
				else:
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
				asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
				asmout = asmout + "jne " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and integer(operand2):
				destreg = getReg(dest, lineNo)
				location1 = getlocation(operand1)
				if location1 != "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
				else:
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
				asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
				asmout = asmout + "jne " + LT + "\n"
				asmout = asmout + "movl $" + operand2 + ", " + destreg + "\n"
				asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
				asmout = asmout + "jne " + LT + "\n"
				asmout = asmout + "movl $0, " + destreg + "\n"
				asmout = asmout + "jmp " + NLT + "\n"
				asmout = asmout + LT + ":" + "\n"
				asmout = asmout + "movl $1, " + destreg + "\n"
				asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)				
			elif not integer(operand1) and not integer(operand2):
				destreg = getReg(dest, lineNo)
				location1 = getlocation(operand1)
				location2 = getlocation(operand2)
				if location1 != "mem" and location2 != "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
					asmout = asmout + "jne " + LT + "\n"
					asmout = asmout + "movl " + location2 + ", " + destreg + "\n"
					asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
					asmout = asmout + "jne " + LT + "\n"
					asmout = asmout + "movl $0, " + destreg + "\n"
					asmout = asmout + "jmp " + NLT + "\n"
					asmout = asmout + LT + ":" + "\n"
					asmout = asmout + "movl $1, " + destreg + "\n"
					asmout = asmout + NLT + ":" + "\n"
				elif location1 == "mem" and location2 != "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
					asmout = asmout + "jne " + LT + "\n"
					asmout = asmout + "movl " + location2 + ", " + destreg + "\n"
					asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
					asmout = asmout + "jne " + LT + "\n"
					asmout = asmout + "movl $0, " + destreg + "\n"
					asmout = asmout + "jmp " + NLT + "\n"
					asmout = asmout + LT + ":" + "\n"
					asmout = asmout + "movl $1, " + destreg + "\n"
					asmout = asmout + NLT + ":" + "\n"
				elif location1 != "mem" and location2 == "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
					asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
					asmout = asmout + "jne " + LT + "\n"
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
					asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
					asmout = asmout + "jne " + LT + "\n"
					asmout = asmout + "movl $0, " + destreg + "\n"
					asmout = asmout + "jmp " + NLT + "\n"
					asmout = asmout + LT + ":" + "\n"
					asmout = asmout + "movl $1, " + destreg + "\n"
					asmout = asmout + NLT + ":" + "\n"
				elif location1 == "mem" and location2 == "mem":
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
					asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
					asmout = asmout + "jne " + LT + "\n"
					asmout = asmout + "movl " + operand2 + ", " + destreg + "\n"
					asmout = asmout + "cmp " + '$0' + ", " + destreg + "\n"
					asmout = asmout + "jne " + LT + "\n"
					asmout = asmout + "movl $0, " + destreg + "\n"
					asmout = asmout + "jmp " + NLT + "\n"
					asmout = asmout + LT + ":" + "\n"
					asmout = asmout + "movl $1, " + destreg + "\n"
					asmout = asmout + NLT + ":" + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)
			relcount = relcount + 1
			for var in varlist:
				location = getlocation(var)
				if location != "mem":
					asmout = asmout + "movl " + location + ", " + var + "\n"
					setlocation(var, "mem")
					registerDescriptor[location]=None
		elif operator == "!":
			#LineNo, not, dest, op1
			dest = instruction[2]
			operand1 = instruction[3]
			if integer(operand1):
				#Case : dest = !(1)
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				asmout = asmout + "movl $" + str(not(int(operand1))) + ", " + destreg + "\n"
				# Update the address descriptor entry for dest variable to say where it is stored no
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)
			elif not integer(operand1):
				#case dest = !(a)
				# Get the register to store the dest
				destreg = getReg(dest, lineNo)
				location1 = getlocation(operand1)
				# Move a to destreg, dest = a
				if location1 != "mem":
					asmout = asmout + "movl " + location1 + ", " + destreg + "\n"
				else:
					asmout = asmout + "movl " + operand1 + ", " + destreg + "\n"
				# Perform Logical and dest = !(dest)
				asmout = asmout + "not " + destreg + "\n"
				registerDescriptor[destreg]=dest
				setlocation(dest, destreg)
		elif operator == "function":
			funcname = instruction[2]
			asmout = asmout + ".globl " + funcname + "\n"
			asmout = asmout + ".type "  + funcname + ", @function\n"
			asmout = asmout + funcname + ":\n"
			asmout = asmout + "pushl %ebp\n"
			asmout = asmout + "movl %esp, %ebp\n"
		elif operator == "call":
			for var in varlist:
				location = getlocation(var)
				if location != "mem":
					asmout = asmout + "movl " + location + ", " + var + "\n"
					setlocation(var, "mem")
					registerDescriptor[location] = None
			funcname = instruction[2]
			asmout = asmout + "call "+ funcname + '\n'
		elif operator == "param":
			#lineNo,param,val
			val = instruction[2]
			if integer(val):
				val = "$" + val
			else:
				location = getlocation(val)
				if location != "mem":
					val = addressDescriptor[val]
			asmout = asmout + "pushl " + val + "\n"
		elif operator == "funcarg":
			#linNo,funcarg,a,i
			a = instruction[2]
			i = instruction[3]
			displacement = 4*(int(i)+1) + 4
			location = getlocation(a)
			if location == 'mem':
				destreg = getReg(a, lineNo)
				registerDescriptor[destreg] = a
				setlocation(a, destreg)
				location = destreg

			asmout = asmout + "movl " + str(displacement) + "(%ebp), " + location + "\n"
			asmout = asmout + "movl " + location + ", " + a + "\n"
			registerDescriptor[location] = None
			addressDescriptor[a] = 'mem'
		elif operator == "pop":
			#lineNo, pop, n
			n = instruction[2]
			asmout = asmout + "movl $4, %edi\n"
			for i in range(int(n)):
				asmout = asmout + "addl %edi, %esp\n"
		elif operator == 'retval':
			#lineNo, retval, n
			val = instruction[2]
			asmout = asmout + "movl %eax, " + val + "\n"
		elif operator == 'return':
			val = instruction[2]
			for var in varlist:
				location = getlocation(var)
				if location == "%eax":
					asmout = asmout + "movl " + location + ", " + var + "\n"
					setlocation(var, "mem")
					break
			if integer(val):
				val = "$" + val
			asmout = asmout + "movl " + val + ", %eax\n"
			asmout = asmout + "movl %ebp, %esp\n"
			asmout = asmout + "popl %ebp\n"
			asmout = asmout + "ret\n"
			setlocation(val, '%eax')
		elif operator == 'endOfCode':
			asmout = asmout + "movl $1, %eax \nmovl $0, %ebx \nint $0x80"	
		elif operator == "print":
			tobeprint = instruction[2]
			if integer(tobeprint):
				asmout = asmout + "pushl $"+ tobeprint +"\n"
				asmout = asmout + "pushl $prtsrt \n"
				asmout = asmout + "call printf \n"
			else:	
				location = getlocation(tobeprint)
				if not location == "mem":
					asmout = asmout + "pushl " + location + "\n"
					asmout = asmout + "pushl $prtsrt\n"
					asmout = asmout + "call printf\n"
				else:
					asmout = asmout + "pushl " + tobeprint + "\n"
					asmout = asmout + "pushl $prtsrt\n"
					asmout = asmout + "call printf\n"					
		elif operator == "vector":
			#lineNo,vector,vectorname,vectorlength
			name = instruction[2]
			length = instruction[3]
			vectorlist.append((name,int(length)))
		elif operator == "member":
			#lineNo,member,dest,vectorname,offset
			dest = instruction[2]
			name = instruction[3]
			offset = instruction[4]
			destreg = getReg(dest, lineNo)
			off = getReg(offset, lineNo)

			asmout = asmout + "movl " + name + "(%eax), " + destreg +"\n"

			registerDescriptor[off] = offset
			setlocation(offset, off)
			registerDescriptor[destreg] = dest
			setlocation(dest, destreg)

			asmout = asmout + "movl " + destreg + ", " + dest + "\n"
			registerDescriptor[destreg] = None
			addressDescriptor[dest] = 'mem'

		elif operator == "update":
			#lineNo,update,assignvalue,vectorname,offset
			assignvalue = instruction[2]
			name = instruction[3]
			offset = instruction[4]
			off = getReg(offset, lineNo)
			
			if(integer(assignvalue)):
				asmout = asmout + "movl $" + assignvalue + ", " + name + "(%eax)\n"
			else:
				loc2 = getlocation(assignvalue)
				if(loc2 != "mem"):
					asmout = asmout + "movl " + loc2 + ", " + name + "(%eax)\n"
				else:
					regdest = getReg(assignvalue, lineNo)
					asmout = asmout + "movl " + assignvalue + ", " + regdest + "\n"
					registerDescriptor[regdest] = assignvalue

					setlocation(assignvalue, regdest)
					asmout = asmout + "movl " + regdest + ", " + name + "(%eax)\n"

			registerDescriptor[off]= offset
			setlocation(offset, off)
		elif operator == "read":
			for var in varlist:
				loc = getlocation(var)
				if loc != "mem":
					asmout = asmout + "movl " + loc + ", " + var + "\n"
					setlocation(var, "mem")
			dest = instruction[2]
			asmout = asmout + "pushl $"+ dest +"\n"
			asmout = asmout + "pushl $inptstr \n"
			asmout = asmout + "call scanf \n"
		# #return asmout
#---------------------------------------------------------------------------------------------------------
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
nextuseTable = [None for i in range(len(data))]
# print nextuseTable

for i in range(0,len(data)):
	if data[i][1] not in ['call','label','return','endOfCode','goto','ifgoto','function','vector','member','update']:
		varlist = varlist + data[i]

varlist = list(set(varlist))
varlist = [x for x in varlist if not integer(x)]
for word in operators:
	if word in varlist:
		varlist.remove(word)
# print varlist

addressDescriptor = addressDescriptor.fromkeys(varlist, "mem")
symbolTable = addressDescriptor.fromkeys(varlist, ["live", None])

leaders = [1,]
for i in range(0,len(data)):
	if data[i][1] == "ifgoto":
		leaders.append(int(data[i][0])+1)
		if(data[i][len(data[i])-1].startswith('l')):
			for j in range(0,len(data)):
				if data[i][len(data[i])-1] in data[j]:
					leaders.append(int(data[j][0]))
		else:
			leaders.append(int(data[i][len(data[i])-1]))
		
	if data[i][1] == "goto":
		leaders.append(int(data[i][0])+1)
		if(data[i][len(data[i])-1].startswith('l')):
			for j in range(0,len(data)):
				if data[i][len(data[i])-1] in data[j]:
					leaders.append(int(data[j][0]))
		else:
			leaders.append(int(data[i][len(data[i])-1]))
		# leaders.append(int(data[i][len(data[i])-1]))
	if data[i][1] == "label":
		leaders.append(int(data[i][0]))	
	if data[i][1] == "function":
		leaders.append(int(data[i][0]))
leaders = list(set(leaders))
leaders.sort()
# print leaders

BasicBlocks = []
i = 0
while i < len(leaders)-1:
	BasicBlocks.append(list(range(leaders[i],leaders[i+1])))
	i = i + 1
BasicBlocks.append(list(range(leaders[i],len(data)+1)))
# print BasicBlocks
for BasicBlock in BasicBlocks:
	revData = BasicBlock[:]
	revData.reverse()
	for instrnumber in revData:
		instr = data[instrnumber-1]
		operator = instr[1]
		variables = [x for x in instr if x in varlist]
		nextuseTable[instrnumber-1] = {var:symbolTable[var] for var in varlist}
		if operator in ['+','-','*','/','%']:
			z = instr[2]
			x = instr[3]
			y = instr[4]
			if z in variables:
				symbolTable[z] = ["dead", None]
			if x in variables:
				symbolTable[x] = ["live", instrnumber]
			if y in variables:
				symbolTable[y] = ["live", instrnumber]
		elif operator == "ifgoto":
			x = instr[3]
			y = instr[4]
			if x in variables:
				symbolTable[x] = ["live", instrnumber]
			if y in variables:
				symbolTable[y] = ["live", instrnumber]
		elif operator == "print":
			x = instr[2]
			if x in variables:
				symbolTable[x] = ["live", instrnumber]			
		elif operator == "=":
			x = instr[2]
			y = instr[3]
			if x in variables:
				symbolTable[x] = ["dead", None]
			if y in variables:
				symbolTable[y] = ["live", instrnumber]

#-----------------------------------------------------------------------------------------------------------------------

data_section = ".section .data\n"
for var in varlist:
	data_section = data_section + var + ":\t" + ".int 0\n"
data_section = data_section +'\n'

text_section = ".section .text\n\n" + "inptstr: .asciz \"%d\" \n" + "prtsrt:  .asciz \"%d\\n\" \n.globl main\n\n" +  "main:\n"

for BasicBlock in BasicBlocks:
	if BasicBlock:
		text_section = text_section + "Loop" + str(BasicBlock[0]) + ":\n"
		for i in BasicBlock:		
			prodAsm(data[int(i)-1])
			text_section = text_section + asmout
for (var, length) in vectorlist:
	data_section = data_section + var + ":\n.int " 
	for i in range(1,(length+1)):
		if(i != length):
			data_section = data_section + "0, "
		else:
			data_section = data_section + "0\n"

asmoutcode = data_section + text_section
print(asmoutcode)