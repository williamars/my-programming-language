%{
# include "Parser.tab.h"
%}
%%

"+"       { return ADD; }
"-"       { return SUB; }
"*"       { return MUL; }
"/"       { return DIV; }
"="       { return EQUAL; }
"=="      { return EQUALEQUAL; }
"int"     { return TYPE; }
"str"     { return TYPE; }
"("       { return OPEN_PAREN; }
")"       { return CLOSE_PAREN; }
"{"       { return OPEN_BRACKET; }
"}"       { return CLOSE_BRACKET; }
";"       { return SEMICOLON; }
","       { return COMMA; }
"."       { return POINT; }
"if"      { return IF; }
"else"    { return ELSE; }
"while"   { return WHILE; }
"printf"  { return PRINTF; }
"scanf"   { return SCANF; }
"||"      { return OR; }
"&&"      { return AND; }
"!"       { return NOT; }
">"       { return GREATER_THAN; }
"<"       { return LESS_THAN; }
[0-9]+    { yylval = atoi(yytext); return NUMBER; }
[a-zA-Z]+ { return IDENTIFIER; }
\n        { /* ignore breakline */ }
[ \t]     { /* ignore whitespace */ }
.         { /* printf("Mystery character %c\n", *yytext); */ }
%%