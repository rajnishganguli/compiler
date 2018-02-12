#!/usr/bin/python
import sys
import os

if len(sys.argv) == 2:
	filename = str(sys.argv[1])
else:
	print("usage: python codegen.py irfile")
	exit()

def integer(number):
		if number.isdigit() or (number[1:].isdigit() and (number[0] == "-" or number[0] == "+")):
			return 1
		else:
			return 0

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