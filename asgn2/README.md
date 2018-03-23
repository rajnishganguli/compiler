
GROUP 1: 12551,12390,12325
Assignment 2 : Assembly Code Generator
-----------------------------------------------------------------------------------------------------------------------

How to execute :
cd asgn2
make
bin/codegen test/test1.ir
--------------------------------------------------------------------------------------------------

About:

This is a python file that translates ir code to x86 assembly code for AT&T architechture.The assembly code is displayed on the standard output.

Supports:

Mathematical Operators: + , - , * , / , %
Others: "call", "label", "return", "endOfCode"


The function produceAsm(instruction) takes in instructions line by line and returns the assembly code for it
--------------------------------------------------------------------------------------------------

Save the assembly code produced as out.s

To execute the assembly code produced on standard out use:

as --32 out.s -o out.o
gcc -m32 out.o -o out
./out
--------------------------------------------------------------------------------------------------

Note:

To install 32-bit architecture binaries run:

apt-get install gcc-multilib g++-multilib

