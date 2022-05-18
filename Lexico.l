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
"pua"     { return TYPE; }
"zay"     { return TYPE; }
"("       { return OPEN_PAREN; }
")"       { return CLOSE_PAREN; }
"h"       { return OPEN_BRACKET; }
"j"       { return CLOSE_BRACKET; }
";"       { return SEMICOLON; }
","       { return COMMA; }
"."       { return POINT; }
"pm"      { return IF; }
"lszl"    { return ELSE; }
"dopsl"   { return WHILE; }
"wypuam"  { return PRINTF; }
"zjhum"   { return SCANF; }
"ii"      { return OR; }
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