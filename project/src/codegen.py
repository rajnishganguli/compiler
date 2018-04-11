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
operators = ['+','-','*','/','=','==','<=','>=','>','<','%',"&&","||",'&','|',"!=",'!',"ifgoto","goto","call","return","label","print","endOfCode","function","funcarg","param"]
varlist=[]

global asmout
asmout = ""

def integer(number):
		if number.isdigit() or (number[1:].isdigit() and (number[0] == "-" or number[0] == "+")):
			return 1
		else:
			return 0

def getReg(var, lineno):
	# print registerDescriptor
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
	# print instrvardict
	# print farthestnextuse
	for var in instrvardict:
		if instrvardict[var] == farthestnextuse:
			break;
	for regspill in registerDescriptor.keys():
		if registerDescriptor[regspill] == var:
			break;
	# print var
	asmout = asmout + "movl " + regspill + ", " + var + "\n"
	return regspill

def getlocation(var):
	return addressDescriptor[var]

def setlocation(var, loc):
	addressDescriptor[var] = loc

def nextuse(var, line):
	return nextuseTable[line-1][var]


def prodAsm(instruction):
		global asmout
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
			   	asmout = asmout + "\t movl $" + operand1 + ", " + destreg + "\n"
			   	asmout = asmout + "\t addl $" + operand2 +" , " + destreg + "\n"
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
				# Update the register descriptor entry for destreg to say that it contains the dest
				registerDescriptor[destreg] = dest
				# Update the address descriptor entry for dest variable to say where it is stored now
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
		       
		       
		# elif (operator == '/' or operator == '%/%' or operator =='%%'):

		# 	dest = instruction[2]
		# 	operand1 = instruction[3]
		# 	operand2 = instruction[4]

		# 	# we have to free registers rax and edx 

		# 	if reg['%eax'] != None: 
		# 	   	asmout = asmout + freereg('%eax')		#function to free a register
		# 	if reg['%edx'] != None:
		# 	   	asmout = asmout + freereg('%edx')
		# 	if reg['%ebx'] != None:
		# 	   	asmout = asmout + freereg('%ebx')

		# 	if integer(operand1):
		# 	   	asmout = asmout + "\t movl $" + operand1 + " , %eax\n"
		# 	   	#reg['%eax']=int(operand1)
		# 	else:
		# 	   	asmout = asmout + "\t movl " + operand1+ " , %eax\n"
		# 	   	reg['%eax']=operand1
		# 	if integer(operand2):
		# 	   	asmout = asmout + "\t movl $" + operand2 + " , %ebx\n"
		# 	   	#reg['%ebx']=int(operand2)
		# 	   	asmout = asmout + "\t xorl %edx , %edx \n"
		# 		reg['%edx']= 0
		# 		asmout=asmout + "\t idiv %ebx\n"
		# 	else:
		# 	   	asmout = asmout + "\t movl " + operand2 + " , %ebx\n"
		# 	   	reg['%ebx']=operand2
		# 		asmout = asmout + "\t xorl %edx , %edx \n"
		# 		reg['%edx']= 0
		# 		asmout=asmout + "\t idiv %ebx\n"

		# 	if operator == '%%':
		# 		asmout = asmout + "\t movl %edx , " + dest + "\n"
		# 	   	#reg['%eax'] = "Quotient for the modulus operation"
		# 		reg['%edx'] = dest
		# 	else:
		# 		asmout = asmout + "\t movl %eax , " + dest + "\n"
		# 	   	reg['%eax'] = dest
		# 	   	#reg['%edx'] = "Reminder of division" 


		# elif operator == '*':

		#         	dest = instruction[2]
		# 		operand1 = instruction[3]
		# 		operand2 = instruction[4]
		# 		if integer(operand1) and integer(operand2):
		# 		   	destreg=getreg(dest,instruction[0])
		# 		   	asmout = asmout + "\t movl $" + operand1 + " , " + destreg + "\n"
		# 		   	reg[destreg]=operand1
		# 		   	regop2 = getreg(operand2,instruction[0])
		# 		   	asmout = asmout + "\t movl $" + operand2 + " , " + regop2 + "\n"
		# 		   	#reg[regop2]=int(operand2)
		# 		   	asmout= asmout + "\t imul " + regop2 +" , " + destreg + "\n"
		# 		   	asmout = asmout + "\t movl " + destreg + ", " + dest + "\n"
		# 		   	reg[destreg]=dest
		# 		elif not integer(operand1) and not integer(operand2):
		# 		   	#regop1 = getreg(operand1)
		# 		   	destreg=getreg(dest,instruction[0])
		# 		   	regop2 = getreg(operand2,instruction[0])
		# 		   	reg[regop2]=operand2
		# 		   	asmout = asmout + "\t movl " + operand1 + " , " + destreg+ "\n"
		# 		   	reg[destreg]=operand1
		# 		   	asmout = asmout + "\t movl " + operand2 + " , " + regop2 + "\n"
		# 		   	asmout = asmout + "\t imul " + regop2 + " , " + destreg + "\n"
		# 		   	asmout = asmout + "\t movl " + destreg + ", " + dest + "\n"
		# 		   	reg[destreg]= dest 
		# 		elif not integer(operand1) and integer(operand2):
		# 		   	destreg=getreg(dest,instruction[0])
		# 		   	asmout = asmout + "\t movl " + operand1 + " , " + destreg+ "\n"
		# 		   	reg[destreg]=operand1
		# 		   	regop2 = getreg(operand2,instruction[0])
		# 		   	asmout = asmout + "\t movl $" + operand2 + " , " + regop2 + "\n"
		# 		   	reg[regop2]=int(operand2)
		# 		   	asmout= asmout + "\t imul " + regop2 +" , " + destreg + "\n"
		# 		   	asmout = asmout + "\t movl " + destreg + ", " + dest + "\n"
		# 		   	reg[destreg]= dest
		# 		else: #op1 integer and op2 not integer
		# 		   	destreg=getreg(dest,instruction[0])
		# 		   	regop2 = getreg(operand2,instruction[0])
		# 		   	asmout = asmout + "\t movl " + operand2 + " , " + regop2+ "\n"
		# 		   	reg[regop2]=operand2
		# 		   	asmout = asmout + "\t movl $"+ operand1 + " , " + destreg
		# 		   	asmout = asmout + "\t imul " + regop2 + " , " + destreg + "\n"
		# 		   	asmout = asmout + "\t movl " + destreg + ", " + dest + "\n"
		# 		   	reg[destreg]= dest
 

			
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

	   #      elif operator == "ifgoto":

		  #       	operatorin = instruction[2]
				


				# if operatorin =="==" or operatorin==">=" or operatorin == "<=" or operatorin == ">" or operatorin == "<" or operatorin == "!=":
				#    operand1 = instruction[3]
				#    operand2 = instruction[4]
				#    gotoloc = instruction[5]
				#    if integer(operand1) and integer(operand2):
				#    	destreg=getreg(operand1,instruction[0])
				#    	asmout = asmout + "\t movl $" + operand1 + ", " + destreg + "\n"
				#    	#reg[destreg]=int(operand1)
				#    	asmout= asmout + "\t cmpl $" + operand2 +", " + destreg + "\n"
				#    	reg[destreg]=operand1
				#    elif not integer(operand1) and not integer(operand2):
				#    	destreg=getreg(operand1,instruction[0])
				#    	#regop1 = getreg(operand1)
				#    	regop2 = getreg(operand2,instruction[0])
				#    	reg[regop2]=operand2
				#    	asmout = asmout + "\t movl " + operand1 + "," + destreg+ "\n"
				#    	reg[destreg]=operand1
				#    	asmout = asmout + "\t movl " + operand2 + "," + regop2 + "\n"
				#    	asmout = asmout + "\t cmpl " + regop2 + "," + destreg + "\n"
				#    	reg[destreg]= operand1 
				#    elif not integer(operand1) and integer(operand2):
				#    	destreg=getreg(operand1,instruction[0])
				#    	asmout = asmout + "\t movl " + operand1 + "," + destreg+ "\n"
				#    	reg[destreg]=operand1
				#    	asmout = asmout + "\t cmpl $" + operand2 + "," + destreg + "\n"
				#    	reg[destreg]= operand1
				#    else: #op1 integer and op2 not integer
				#    	destreg=getreg(operand2,instruction[0])
				#    	asmout = asmout + "\t movl " + operand2 + "," + destreg+ "\n"
				#    	reg[destreg]=operand2
				#    	asmout = asmout + "\t cmpl $" + operand1 + "," + destreg + "\n"
				#    	reg[destreg]= operand1
				#    if operatorin == "==":
				#    	asmout=asmout+"\t je  Loop"+gotoloc +"\n"

				#    elif operatorin == "<=":
				#    	asmout=asmout+"\t jle  Loop"+gotoloc +"\n"

				#    elif operatorin == "<":
				#    	asmout=asmout+"\t jl  Loop"+gotoloc +"\n"
				   
				#    elif operatorin == ">=":
				#    	asmout=asmout+"\t jge  Loop"+gotoloc +"\n"
				
				#    elif operatorin == ">":
				#    	asmout=asmout+"\t jg  Loop"+gotoloc +"\n"
				
				#    elif operatorin == "!=":
				#    	asmout=asmout+"\t jne  Loop"+gotoloc +"\n"

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
			
		# elif operator == "goto":

		# 		destloc = instruction[2]
		# 		asmout=asmout+"\t jmp  Loop"+destloc +"\n"

		# elif operator == "call":

		# 		funcname = instruction[2]

				
		# 		#if (instruction[3] != NULL and integer(instruction[3]):
		# 		#	asmout = asmout + "pushl $" int(instruction[3])
		# 		#elif (instruction[3] !=NULL):
		# 		#	asmout = asmout + "pushl " + instruction[3]
		# 		#asmout = asmout +"\t pushl %ebp\n\t movl %ebp, %esp\n"
		# 		asmout = asmout + "\t call "+funcname + '\n'
		# 		asmout = asmout + "\t addl $0, %esp\n"

		# elif operator == 'return':

		# 	 	#return value is supposed to be in rax register

		# 	 	#asmout = asmout + "\t movl %ebp, %esp\n\t popl %ebp \n"
		# 	 	asmout = asmout + "\t ret \n"

		# elif operator == "label":

		# 	 	funcstart = instruction[2]

		# 		asmout = asmout +  funcstart + ":\n"
		# 		#asmout = asmout + "\t pushl %ebp\n \t movl %esp, %ebp\n"

		# elif operator == 'endOfCode':

		# 		asmout = asmout + "\t movl $1, %eax \n\t movl $0, %ebx \n\t int $0x80 \n"

		# else: # operator == "print"

		# 		tobeprint=instruction[2]
		# 		if integer(tobeprint):

		# 			asmout = asmout + "\t pushl $"+ tobeprint +"\n"
		# 			asmout = asmout + "\t call _printf \n"
		# 			asmout = asmout + "\t pushl $fmtstr \n"
		# 			asmout = asmout + "\t addl $8,%esp \n"
		# 			#asmout = asmout + "\t movl $"+ tobeprint +", (%esp)\n"
		# 			#asmout = asmout + "\t call printf \n"
		# 			#asmout = asmout + "movl $4 , %eax\n"
		# 			#asmout = asmout + "movl $1, %ebx\n"
		# 			#asmout = asmout + "movl $"+tobeprint+ " , %ecx\n"
		# 			#asmout = asmout + "movl $4 , %edx\n"

		# 		else:
		# 			destreg = getreg(tobeprint,instruction[0])
					

		# 			#asmout = asmout + "\t movl " + tobeprint + ", "+ destreg+"\n"
		# 			#asmout = asmout + "\t movl " + destreg +", (%esp)\n"
		# 			#if (reg['%eax'] != None):
		# 			#asmout = asmout + "\t pushl %eax\n"
		# 			#if (reg['%ecx'] != None):
		# 			#asmout = asmout + "\t pushl %ecx\n"
		# 			#if (reg['%edx'] != None):
		# 			#asmout = asmout + "\t pushl %ebx\n"
		# 			#destreg = getreg()
		# 			#asmout = asmout + "\t movl " + tobeprint + ", "+ destreg+"\n"
		# 			#asmout =asmout+"\t movl $format , "+formatreg+"\n"
		# 			#asmout = asmout + "\t movl " + destreg + ", "+ destreg+"\n"
		# 			#asmout = asmout +"\t xorl "+ destreg+" , "+ destreg +"\n"
		# 			asmout = asmout + "\t movl " + tobeprint + ", " + destreg +"\n"
		# 			asmout = asmout + "\t pushl " + destreg +"\n"
		# 			asmout = asmout + "\t pushl $prtsrt \n"
		# 			asmout = asmout + "\t call printf \n"
		# 			asmout = asmout + "\t addl $8,%esp \n"
		# 			#asmout = asmout + "\t int $0x80\n\n"

		# 			#asmout = asmout + "\t call printf \n"
		# 			#asmout = asmout +"\t popl %edx\n"
		# 			#asmout = asmout + "\t popl %ecx\n"
		# 			#asmout = asmout + "\t popl %eax\n"
		# 			#asmout = asmout + "\t movl $0 , "+ destreg +"\n"					
		   
		# #return asmout

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
	if data[i][1] not in ['call','label','return','endOfCode','goto','ifgoto','print','function','param','funcarg']:
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

##################################################################################
data_section = ".section .data\n"
for var in varlist:
	data_section = data_section + var + ":\t" + ".int 0\n"
data_section = data_section +'\n'
	#bss_section = ".section .bss\n\n"
text_section = ".section .text\n\n" + "inptstr: .asciz \"%d\" \n" + "prtsrt:  .asciz \"%d\\n\" \n.globl main\n\n" +  "main:\n"

for BasicBlock in BasicBlocks:
	if BasicBlock:
		text_section = text_section + "Loop" + str(BasicBlock[0]) + ":\n"
		for i in BasicBlock:		
			prodAsm(data[int(i)-1])
			text_section = text_section + asmout

#--------------------------------------------------------------------------------------------------
# Priniting the final output
# print("asmout Code (x86) for: [" + filename + "]")
# print("--------------------------------------------------------------------")
asmoutcode = data_section + text_section
# print nextuseTable
print(asmoutcode) 
# print("--------------------------------------------------------------------")
