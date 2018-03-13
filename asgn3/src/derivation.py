import re
from sys import argv
import os
import os.path
def make_html(file_name) :
	file_name = file_name.split('/')[1]
	file_name = file_name.split('.')[0]
	file_name = file_name + ".html"
	outfile = open('derivation.txt', 'w')
	f = open('parser_output.txt','r')
	a = re.compile("Action : Reduce rule")
	
	for line in reversed(f.readlines()):
		if (a.match(line)):
			line = line.split(']')[0]
			line = line.split('[')[1]
			outfile.write(line + '\n')
	outfile.close()
	f.close()

	fin = open('derivation.txt','r')
	fout = open(file_name,'a')

	fout.write("<!DOCTYPE html>\n<html>\n<body>")
	fout.write("<p><b> start </b> </p>")
	line1 = fin.readline()
	if line1 :
		print "Successfully Parsed"
	
	line1_indata = line1.split()
	k = 1
	file_len = len(line1)
	
	while True:
	    
	    line2 = fin.readline()
	    line2_indata = line2.split()
	    if not line2 :
	        for k in range(2,len(line1_indata)):
	                fout.write(" "+line1_indata[k]+" ")
	        fout.write("</p>")
	        break
	    fout.write('<p>')
	    
	    count1 = len(line1_indata)
	    count2 = len(line2_indata)
	    for i in range(len(line1_indata)-1,1,-1):
	        if(line1_indata[i] == line2_indata[0]):
	            line1_right=""
	            for j in range(2,count2):
	                line1_right+=(line2_indata[j])+ " "
	            for k in range(2,i):
	                fout.write(" "+line1_indata[k]+" ")
	            fout.write("<b> "+line1_indata[i]+" </b>")
	            for k in range(i+1,len(line1_indata)):
	                fout.write(" "+line1_indata[k]+" ")
	            fout.write("</p>")
	            line1_indata[i] = line1_right
	            break
	    line1=' '.join(line1_indata)
	    line1_indata = line1.split()
	       
	fout.write("</body>\n</html>\n")
	fout.close()
	return