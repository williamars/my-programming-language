/* simplest version of calculator */
%{
#include <stdio.h>

void yyerror(char *c);
int yylex();

%}

/* declare tokens */
%token NUMBER
%token ADD SUB MUL DIV ABS OPEN_PAREN CLOSE_PAREN SEMICOLON POINT IF ELSE WHILE PRINTF SCANF OR AND NOT GREATER_THAN LESS_THAN OPEN_BRACKET CLOSE_BRACKET EQUAL IDENTIFIER
%token EOL

%%

block:
 | OPEN_BRACKET expression CLOSE_BRACKET { printf("= %d\n", $2); }
 ;

expression: term
 | expression ADD term { $$ = $1 + $3; printf("ADD"); } 
 | expression SUB term { $$ = $1 - $3; printf("SUB"); } 
 ;

term: factor
 | term MUL factor { $$ = $1 * $3; printf("MUL"); } 
 | term DIV factor { $$ = $1 / $3; printf("DIV"); }
 ;

factor: NUMBER
 | ADD factor { $$ = $2; printf("PLUS");}
 | SUB factor { $$ = - $2; printf("SUB");}
 | OPEN_PAREN expression CLOSE_PAREN { $$ = $2; printf("OPEN_PARENT"); }
;
%%

int main(int argc, char **argv)
{
  yyparse();
  return 0;
}

void yyerror(char *s)
{
  fprintf(stderr, "error: %s\n", s);
}