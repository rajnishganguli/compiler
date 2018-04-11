.PHONY: clean
all:
	chmod +x src/parser.py
	cp src/parser.py bin
	cp src/irgen bin
	chmod +x bin/irgen
	chmod +x src/Lexer.py
	cp src/Lexer.py bin/lexer.py
	cp src/TAC.py bin
	cp src/SymbolTable.py bin
	
clean:
	rm -rf bin/*
	# rm -f *.ir