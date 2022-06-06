executavel: Lexico.l Parser.y
		bison -d Parser.y
		flex Lexico.l 
		cc -o $@ Parser.tab.c lex.yy.c -lfl