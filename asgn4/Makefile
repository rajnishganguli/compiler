.PHONY: clean
all:
	chmod +x src/parser.py
	cp src/parser.py bin
	mv bin/parser.py bin/irgen
	chmod +x src/Lexer.py
	cp src/Lexer.py bin/lexer.py
	cp src/TAC.py bin
	cp src/SymbolTable.py bin
	
clean:
	rm -rf bin/*