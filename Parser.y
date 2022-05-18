/* simplest version of calculator */
%{
#include <stdio.h>
void yyerror(char *c);
int yylex();

%}
/* declare tokens */
%token ADD SUB MUL DIV ABS OPEN_PAREN CLOSE_PAREN SEMICOLON POINT IF ELSE WHILE PRINTF SCANF OR AND NOT GREATER_THAN LESS_THAN OPEN_BRACKET CLOSE_BRACKET EQUAL
%token NUMBER EQUALEQUAL TYPE COMMA STRING
%token IDENTIFIER

%token EOL

%%

block:
 | OPEN_BRACKET statement CLOSE_BRACKET 
 ;

statement: SEMICOLON
 | IDENTIFIER EQUAL relexpression SEMICOLON { $$ = $3; }
 | PRINTF OPEN_PAREN relexpression CLOSE_PAREN { printf("%d\n", $3); }
 | block
 | WHILE OPEN_PAREN relexpression CLOSE_PAREN statement
 | IF OPEN_PAREN relexpression CLOSE_PAREN statement
 | IF OPEN_PAREN relexpression CLOSE_PAREN statement ELSE statement
 | TYPE IDENTIFIER SEMICOLON
 ;

relexpression: expression
 | relexpression EQUALEQUAL expression { $$ = $1 == $3; }
 | relexpression GREATER_THAN expression { $$ = $1 > $3; }
 | relexpression LESS_THAN expression { $$ = $1 < $3; }
 ;

expression: term
 | expression ADD term { $$ = $1 + $3; } 
 | expression SUB term { $$ = $1 - $3; }
 | expression OR term { $$ = $1 || $3; }
 | expression POINT term { $$ = $1 + $3; }
;

term: factor
 | term MUL factor { $$ = $1 * $3; } 
 | term DIV factor { $$ = $1 / $3; }
 | term AND factor { $$ = $1 && $3; }
 ;

factor:
 | NUMBER { $$ = $1; }
 | STRING { $$ = $1; }
 | IDENTIFIER
 | ADD factor { $$ = $2; }
 | SUB factor { $$ = - $2; }
 | OPEN_PAREN expression CLOSE_PAREN { $$ = $2; }
 | SCANF OPEN_PAREN CLOSE_PAREN { $$ = scanf("%d"); }
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