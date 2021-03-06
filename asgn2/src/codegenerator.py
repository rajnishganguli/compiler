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
			   	destreg=getreg(dest,instruction[0])
			   	asmout = asmout + "\t movl $" + operand1 + ", " + destreg + "\n"
			   	#reg[destreg]=int(operand1)
			   	asmout= asmout + "\t addl $" + operand2 +" , " + destreg + "\n"
			   	asmout = asmout + "\t movl " + destreg + ", " + dest + "\n"
			   	reg[destreg]=dest
			elif not integer(operand1) and not integer(operand2):
			   	destreg=getreg(dest,instruction[0])
			   	#regop1 = getreg(operand1)
			   	#regop2 = getreg(operand2)
			   	#reg[regop2]=operand2
			   	asmout = asmout + "\t movl " + operand1 + " , " + destreg+ "\n"
			   	reg[destreg]=operand1
			   	#asmout = asmout + "\t movl " + operand2 + " , " + regop2 + "\n"
			   	asmout = asmout + "\t addl " + operand2 + " , " + destreg + "\n"
			   	asmout = asmout + "\t movl " + destreg + ", " + dest + "\n"
			   	reg[destreg]= dest 
			elif not integer(operand1) and integer(operand2):
			   	destreg=getreg(dest,instruction[0])
			   	asmout = asmout + "\t movl " + operand1 + " , " + destreg+ "\n"
			   	reg[destreg]=operand1
			   	asmout = asmout + "\t addl $" + operand2 + " , " + destreg + "\n"
			   	asmout = asmout + "\t movl " + destreg + ", " + dest + "\n"
			   	reg[destreg]= dest
			else: #op1 integer and op2 not integer
			   	destreg=getreg(dest,instruction[0])
			   	asmout = asmout + "\t movl " + operand2 + " , " + destreg+ "\n"
			   	reg[destreg]=operand2
			   	asmout = asmout + "\t addl $" + operand1 + " , " + destreg + "\n"
			   	asmout = asmout + "\t movl " + destreg + ", " + dest + "\n"
			   	reg[destreg]= dest

		elif operator == '-':

		 	dest = instruction[2]
			operand1 = instruction[3]
			operand2 = instruction[4]

			if integer(operand1) and integer(operand2):
			   	destreg=getreg(dest,instruction[0])
			   	asmout = asmout + "\t movl $" + operand1 + " , " + destreg + "\n"
			   	#reg[destreg]=int(operand1)
			   	asmout= asmout + "\t subl $" + operand2 +" , " + destreg + "\n"
			   	asmout = asmout + "\t movl " + destreg + ", " + dest + "\n"
			   	reg[destreg]=dest
			elif not integer(operand1) and not integer(operand2):
			   	#regop1 = getreg(operand1)
			   	destreg=getreg(dest,instruction[0])
			   	#regop2 = getreg(operand2)

			   	#reg[regop2]=operand2
			   	asmout = asmout + "\t movl " + operand1 + " , " + destreg+ "\n"
			   	reg[destreg]=operand1
			   	#asmout = asmout + "\t movl " + operand2 + " , " + regop2 + "\n"
			   	asmout = asmout + "\t subl " + operand2 + " , " + destreg + "\n"
			   	asmout = asmout + "\t movl " + destreg + ", " + dest + "\n"
			   	reg[destreg]= dest 
			elif not integer(operand1) and integer(operand2):
			   	destreg=getreg(dest,instruction[0])
			   	asmout = asmout + "\t movl " + operand1 + " , " + destreg+ "\n"
			   	reg[destreg]=operand1
			   	asmout = asmout + "\t subl $" + operand2 + " , " + destreg + "\n"
			   	asmout = asmout + "\t movl " + destreg + ", " + dest + "\n"
			   	reg[destreg]= dest
			else: #op1 integer and op2 not integer
			   	destreg=getreg(dest,instruction[0])
			   	#regop2 = getreg(operand2)
			   	#asmout = asmout + "\t movl " + operand2 + " , " + regop2+ "\n"
			   	#reg[regop2]=operand2
			   	asmout = asmout + "\t movl $"+ operand1 + " , " + destreg
			   	asmout = asmout + "\t subl " + operand2 + " , " + destreg + "\n"
			   	asmout = asmout + "\t movl " + destreg + ", " + dest + "\n"
			   	reg[destreg]= dest
		       
		       
		elif (operator == '/' or operator == '%/%' or operator =='%%'):

			dest = instruction[2]
			operand1 = instruction[3]
			operand2 = instruction[4]

			# we have to free registers rax and edx 

			if reg['%eax'] != None: 
			   	asmout = asmout + freereg('%eax')		#function to free a register
			if reg['%edx'] != None:
			   	asmout = asmout + freereg('%edx')
			if reg['%ebx'] != None:
			   	asmout = asmout + freereg('%ebx')

			if integer(operand1):
			   	asmout = asmout + "\t movl $" + operand1 + " , %eax\n"
			   	#reg['%eax']=int(operand1)
			else:
			   	asmout = asmout + "\t movl " + operand1+ " , %eax\n"
			   	reg['%eax']=operand1
			if integer(operand2):
			   	asmout = asmout + "\t movl $" + operand2 + " , %ebx\n"
			   	#reg['%ebx']=int(operand2)
			   	asmout = asmout + "\t xorl %edx , %edx \n"
				reg['%edx']= 0
				asmout=asmout + "\t idiv %ebx\n"
			else:
			   	asmout = asmout + "\t movl " + operand2 + " , %ebx\n"
			   	reg['%ebx']=operand2
				asmout = asmout + "\t xorl %edx , %edx \n"
				reg['%edx']= 0
				asmout=asmout + "\t idiv %ebx\n"

			if operator == '%%':
				asmout = asmout + "\t movl %edx , " + dest + "\n"
			   	#reg['%eax'] = "Quotient for the modulus operation"
				reg['%edx'] = dest
			else:
				asmout = asmout + "\t movl %eax , " + dest + "\n"
			   	reg['%eax'] = dest
			   	#reg['%edx'] = "Reminder of division" 


		elif operator == '*':

		        	dest = instruction[2]
				operand1 = instruction[3]
				operand2 = instruction[4]
				if integer(operand1) and integer(operand2):
				   	destreg=getreg(dest,instruction[0])
				   	asmout = asmout + "\t movl $" + operand1 + " , " + destreg + "\n"
				   	reg[destreg]=operand1
				   	regop2 = getreg(operand2,instruction[0])
				   	asmout = asmout + "\t movl $" + operand2 + " , " + regop2 + "\n"
				   	#reg[regop2]=int(operand2)
				   	asmout= asmout + "\t imul " + regop2 +" , " + destreg + "\n"
				   	asmout = asmout + "\t movl " + destreg + ", " + dest + "\n"
				   	reg[destreg]=dest
				elif not integer(operand1) and not integer(operand2):
				   	#regop1 = getreg(operand1)
				   	destreg=getreg(dest,instruction[0])
				   	regop2 = getreg(operand2,instruction[0])
				   	reg[regop2]=operand2
				   	asmout = asmout + "\t movl " + operand1 + " , " + destreg+ "\n"
				   	reg[destreg]=operand1
				   	asmout = asmout + "\t movl " + operand2 + " , " + regop2 + "\n"
				   	asmout = asmout + "\t imul " + regop2 + " , " + destreg + "\n"
				   	asmout = asmout + "\t movl " + destreg + ", " + dest + "\n"
				   	reg[destreg]= dest 
				elif not integer(operand1) and integer(operand2):
				   	destreg=getreg(dest,instruction[0])
				   	asmout = asmout + "\t movl " + operand1 + " , " + destreg+ "\n"
				   	reg[destreg]=operand1
				   	regop2 = getreg(operand2,instruction[0])
				   	asmout = asmout + "\t movl $" + operand2 + " , " + regop2 + "\n"
				   	reg[regop2]=int(operand2)
				   	asmout= asmout + "\t imul " + regop2 +" , " + destreg + "\n"
				   	asmout = asmout + "\t movl " + destreg + ", " + dest + "\n"
				   	reg[destreg]= dest
				else: #op1 integer and op2 not integer
				   	destreg=getreg(dest,instruction[0])
				   	regop2 = getreg(operand2,instruction[0])
				   	asmout = asmout + "\t movl " + operand2 + " , " + regop2+ "\n"
				   	reg[regop2]=operand2
				   	asmout = asmout + "\t movl $"+ operand1 + " , " + destreg
				   	asmout = asmout + "\t imul " + regop2 + " , " + destreg + "\n"
				   	asmout = asmout + "\t movl " + destreg + ", " + dest + "\n"
				   	reg[destreg]= dest
 

			
		elif operator == "=":

				dest = instruction[2]
				src = instruction[3]
				destreg=getreg(dest,instruction[0])
				reg[destreg]= dest
				if integer(src):
				   	asmout = asmout + "\t movl $"+ src +" , " + destreg +'\n'
				   	reg[destreg]=src
				else:
				   	asmout = asmout + "\t movl "+ src+" , "+destreg+'\n'
				   	reg[destreg]=src

				asmout = asmout + "\t movl " + destreg + " , "+ dest +'\n'
				reg[destreg]=dest



	        elif operator == "ifgoto":

		        	operatorin = instruction[2]
				


				if operatorin =="==" or operatorin==">=" or operatorin == "<=" or operatorin == ">" or operatorin == "<" or operatorin == "!=":
				   operand1 = instruction[3]
				   operand2 = instruction[4]
				   gotoloc = instruction[5]
				   if integer(operand1) and integer(operand2):
				   	destreg=getreg(operand1,instruction[0])
				   	asmout = asmout + "\t movl $" + operand1 + ", " + destreg + "\n"
				   	#reg[destreg]=int(operand1)
				   	asmout= asmout + "\t cmpl $" + operand2 +", " + destreg + "\n"
				   	reg[destreg]=operand1
				   elif not integer(operand1) and not integer(operand2):
				   	destreg=getreg(operand1,instruction[0])
				   	#regop1 = getreg(operand1)
				   	regop2 = getreg(operand2,instruction[0])
				   	reg[regop2]=operand2
				   	asmout = asmout + "\t movl " + operand1 + "," + destreg+ "\n"
				   	reg[destreg]=operand1
				   	asmout = asmout + "\t movl " + operand2 + "," + regop2 + "\n"
				   	asmout = asmout + "\t cmpl " + regop2 + "," + destreg + "\n"
				   	reg[destreg]= operand1 
				   elif not integer(operand1) and integer(operand2):
				   	destreg=getreg(operand1,instruction[0])
				   	asmout = asmout + "\t movl " + operand1 + "," + destreg+ "\n"
				   	reg[destreg]=operand1
				   	asmout = asmout + "\t cmpl $" + operand2 + "," + destreg + "\n"
				   	reg[destreg]= operand1
				   else: #op1 integer and op2 not integer
				   	destreg=getreg(operand2,instruction[0])
				   	asmout = asmout + "\t movl " + operand2 + "," + destreg+ "\n"
				   	reg[destreg]=operand2
				   	asmout = asmout + "\t cmpl $" + operand1 + "," + destreg + "\n"
				   	reg[destreg]= operand1
				   if operatorin == "==":
				   	asmout=asmout+"\t je  Loop"+gotoloc +"\n"

				   elif operatorin == "<=":
				   	asmout=asmout+"\t jle  Loop"+gotoloc +"\n"

				   elif operatorin == "<":
				   	asmout=asmout+"\t jl  Loop"+gotoloc +"\n"
				   
				   elif operatorin == ">=":
				   	asmout=asmout+"\t jge  Loop"+gotoloc +"\n"
				
				   elif operatorin == ">":
				   	asmout=asmout+"\t jg  Loop"+gotoloc +"\n"
				
				   elif operatorin == "!=":
				   	asmout=asmout+"\t jne  Loop"+gotoloc +"\n"

			 	elif operatorin == '&&'or operatorin == '&' :

			 	   operand1 = instruction[3]
				   operand2 = instruction[4]
				   gotoloc = instruction[5]
			 	   #dest = instruction[2]
				   #operand1 = instruction[3]
				   #operand2 = instruction[4]
				   if integer(operand1) and integer(operand2):
				   	destreg=getreg(operand1,instruction[0])
				   	asmout = asmout + "\t movl $" + operand1 + ", " + destreg + "\n"
				   	#reg[destreg]=int(operand1)
				   	asmout= asmout + "\t andl $" + operand2 +", " + destreg + "\n"
				   	reg[destreg]=operand1
				   elif not integer(operand1) and not integer(operand2):
				   	destreg=getreg(operand1,instruction[0])
				   	#regop1 = getreg(operand1)
				   	regop2 = getreg(operand2,instruction[0])
				   	reg[regop2]=operand2
				   	asmout = asmout + "\t movl " + operand1 + "," + destreg+ "\n"
				   	reg[destreg]=operand1
				   	asmout = asmout + "\t movl " + operand2 + "," + regop2 + "\n"
				   	asmout = asmout + "\t andl " + regop2 + "," + destreg + "\n"
				   	reg[destreg]= operand1 
				   elif not integer(operand1) and integer(operand2):
				   	destreg=getreg(operand1,instruction[0])
				   	asmout = asmout + "\t movl " + operand1 + "," + destreg+ "\n"
				   	reg[destreg]=operand1
				   	asmout = asmout + "\t andl $" + operand2 + "," + destreg + "\n"
				   	reg[destreg]= operand1
				   else: #op1 integer and op2 not integer
				   	destreg=getreg(operand2,instruction[0])
				   	asmout = asmout + "\t movl " + operand2 + "," + destreg+ "\n"
				   	reg[destreg]=operand2
				   	asmout = asmout + "\t andl $" + operand1 + "," + destreg + "\n"
				   	reg[destreg]= operand1
				   asmout=asmout+"\t jnz  Loop"+gotoloc +"\n"

			 	elif operatorin == '||' or operatorin == '|':

			 	   operand1 = instruction[3]
				   operand2 = instruction[4]
				   gotoloc = instruction[5]

			 	   if (integer(operand1) and integer(operand2)):
				   		destreg=getreg(operand1,instruction[0])
				   		asmout = asmout + "\t movl $" + operand1 + ", " + destreg + "\n"
				   		#reg[destreg]=int(operand1)
				   		asmout= asmout + "\t orl $" + operand2 +", " + destreg + "\n"
				   		reg[destreg]=operand1
				   elif not integer(operand1) and not integer(operand2):
				   		destreg=getreg(operand1,instruction[0])
				   		#regop1 = getreg(operand1)
				   		regop2 = getreg(operand2,instruction[0])
				   		reg[regop2]=operand2
				   		asmout = asmout + "\t movl " + operand1 + "," + destreg+ "\n"
				   		reg[destreg]=operand1
				   		asmout = asmout + "\t movl " + operand2 + "," + regop2 + "\n"
				   		asmout = asmout + "\t orl " + regop2 + "," + destreg + "\n"
				   		reg[destreg]= operand1 
				   elif not integer(operand1) and integer(operand2):
				   		destreg=getreg(operand1,instruction[0])
					   	asmout = asmout + "\t movl " + operand1 + "," + destreg+ "\n"
					   	reg[destreg]=operand1
					   	asmout = asmout + "\t orl $" + operand2 + "," + destreg + "\n"
				   		reg[destreg]= operand1
				   else: #op1 integer and op2 not integer
				   		destreg=getreg(operand2,instruction[0])
				   		asmout = asmout + "\t movl " + operand2 + "," + destreg+ "\n"
				   		reg[destreg]=operand2
				   		asmout = asmout + "\t orl $" + operand1 + "," + destreg + "\n"
				   		reg[destreg]= operand1

				   asmout=asmout+"\t jnz  Loop"+gotoloc +"\n"

		        	elif operatorin == '!':

		        	   operand1 = instruction[3]
				   #operand2 = instruction[4]
				   gotoloc = instruction[4]

			     	   #dest=instruction[2]
		        	   destreg = getreg(operand1,instruction[0]) 
		        	   if integer(operand1):
		        	   	asmout = asmout + "\t movl $" + operand1 + " , " + destreg + "\n"
			 		asmout = asmout + "\t notl " + destreg + "\n"
			 	   else:
			 	   	asmout = asmout + "\t movl " + operand1 + " , " + destreg + "\n"
			 		asmout = asmout + "\t notl " + destreg + "\n"
			 	   reg[destreg]=operand1
			 	   asmout=asmout+"\t jnz  Loop"+gotoloc +"\n"
			
		elif operator == "goto":

				destloc = instruction[2]
				asmout=asmout+"\t jmp  Loop"+destloc +"\n"

		elif operator == "call":

				funcname = instruction[2]

				
				#if (instruction[3] != NULL and integer(instruction[3]):
				#	asmout = asmout + "pushl $" int(instruction[3])
				#elif (instruction[3] !=NULL):
				#	asmout = asmout + "pushl " + instruction[3]
				#asmout = asmout +"\t pushl %ebp\n\t movl %ebp, %esp\n"
				asmout = asmout + "\t call "+funcname + '\n'
				asmout = asmout + "\t addl $0, %esp\n"

		elif operator == 'return':

			 	#return value is supposed to be in rax register

			 	#asmout = asmout + "\t movl %ebp, %esp\n\t popl %ebp \n"
			 	asmout = asmout + "\t ret \n"

		elif operator == "label":

			 	funcstart = instruction[2]

				asmout = asmout +  funcstart + ":\n"
				#asmout = asmout + "\t pushl %ebp\n \t movl %esp, %ebp\n"

		elif operator == 'endOfCode':

				asmout = asmout + "\t movl $1, %eax \n\t movl $0, %ebx \n\t int $0x80 \n"

		else: # operator == "print"

				tobeprint=instruction[2]
				if integer(tobeprint):

					asmout = asmout + "\t pushl $"+ tobeprint +"\n"
					asmout = asmout + "\t call _printf \n"
					asmout = asmout + "\t pushl $fmtstr \n"
					asmout = asmout + "\t addl $8,%esp \n"
					#asmout = asmout + "\t movl $"+ tobeprint +", (%esp)\n"
					#asmout = asmout + "\t call printf \n"
					#asmout = asmout + "movl $4 , %eax\n"
					#asmout = asmout + "movl $1, %ebx\n"
					#asmout = asmout + "movl $"+tobeprint+ " , %ecx\n"
					#asmout = asmout + "movl $4 , %edx\n"

				else:
					destreg = getreg(tobeprint,instruction[0])
					

					#asmout = asmout + "\t movl " + tobeprint + ", "+ destreg+"\n"
					#asmout = asmout + "\t movl " + destreg +", (%esp)\n"
					#if (reg['%eax'] != None):
					#asmout = asmout + "\t pushl %eax\n"
					#if (reg['%ecx'] != None):
					#asmout = asmout + "\t pushl %ecx\n"
					#if (reg['%edx'] != None):
					#asmout = asmout + "\t pushl %ebx\n"
					#destreg = getreg()
					#asmout = asmout + "\t movl " + tobeprint + ", "+ destreg+"\n"
					#asmout =asmout+"\t movl $format , "+formatreg+"\n"
					#asmout = asmout + "\t movl " + destreg + ", "+ destreg+"\n"
					#asmout = asmout +"\t xorl "+ destreg+" , "+ destreg +"\n"
					asmout = asmout + "\t movl " + tobeprint + ", " + destreg +"\n"
					asmout = asmout + "\t pushl " + destreg +"\n"
					asmout = asmout + "\t pushl $prtsrt \n"
					asmout = asmout + "\t call printf \n"
					asmout = asmout + "\t addl $8,%esp \n"
					#asmout = asmout + "\t int $0x80\n\n"

					#asmout = asmout + "\t call printf \n"
					#asmout = asmout +"\t popl %edx\n"
					#asmout = asmout + "\t popl %ecx\n"
					#asmout = asmout + "\t popl %eax\n"
					#asmout = asmout + "\t movl $0 , "+ destreg +"\n"					
		   
		#return asmout

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

data_section = ".section .data\n"
for var in var_list:
	data_section = data_section + var + ":\t" + ".int 0\n"
data_section = data_section +'\n'
	#bss_section = ".section .bss\n\n"
text_section = ".section .text\n\n" + "inptstr: .asciz \"%d\" \n " + "prtsrt:  .asciz \"%d\\n\" \n .globl main\n\n" +  "main:\n"

for node in node_block:
	#print "***",node
	if node:
		text_section = text_section + "Loop" + str(node[0]) + ":\n"
		for i in node:
		#print i
		#print data[int(i)-1][0]
		#print node
		
			prodAsm(data[int(i)-1])
			text_section = text_section + asmout

# Priniting the final output
# print("Assembly Code (x86) for: [" + filename + "]")
assemblycode = data_section + text_section
print(assemblycode) 

# Save the x86 code in a file here as out.s
# outputfile = open('out.s', 'w+')
# outputfile.write(assemblycode)
# outputfile.close()