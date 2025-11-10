%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>
    #include "parser.tab.h"
%}

%option noyywrap

%%

[ \t\n]+           { /* Ignorar espacios */ }

"utn"              { return UTN; }
"finutn"           { return FINUTN; }
"leer"             { return LEER; }
"escribir"         { return ESCRIBIR; }
"si"               { return SI; }
"entonces"         { return ENTONCES; }
"finsi"            { return FINSI; }
"repetir"          { return REPETIR; }
"veces"            { return VECES; }

":="               { return ASIGNACION; }
"+"                { return SUMA; }
"-"                { return RESTA; }
"*"                { return MULTIPLICACION; }
">"                { return MAYOR; }
"<"                { return MENOR; }
"="                { return IGUAL; }
"."                { return PUNTO; }
"("                { return PAREN_IZQ; }
")"                { return PAREN_DER; }

[0-9]+             { 
                       yylval.ival = atoi(yytext); 
                       return NUMERO; 
                   }

[a-zA-Z][a-zA-Z0-9]* { 
                       yylval.sval = strdup(yytext); 
                       return ID; 
                   }

.                  { printf("Error Léxico: '%s'\n", yytext); }
%%