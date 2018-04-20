GROUP 1: 12551,12390,12325
Project:
	Source Language : R
	Implementation Langauge : Python
	Architecture : X86
-----------------------------------------------------------------------------------------------------------------------

How to execute :
cd project
./compile test/test1.R
./a.out
--------------------------------------------------------------------------------------------------

About:
We are useing ply.lex and ply.yacc
We are using emit based technique to generate 3AC.
The codegen file produces 32-bit x86 AT&T
-----------------------------------------------------------

Features: 
* if else
* for loop
* while loop
* functions and argument passing
* Recursion
* vector(like array)
* Logical operators(&&, ||)
* Bitwise operators(&, |, !)
* Relational operators(>, >=, <, <=, ==, !=)
* Arithmatic operators(+, -, *, /, %)
