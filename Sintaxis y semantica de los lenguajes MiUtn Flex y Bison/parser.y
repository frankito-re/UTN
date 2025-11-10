%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

    int yylex();
    void yyerror(const char *s);

    #define MAX_SYMBOLS 100
    char* g_sym_names[MAX_SYMBOLS];
    int   g_sym_values[MAX_SYMBOLS];
    int   g_sym_count = 0;

    int g_skip_block = 0;

    void store_symbol(char* name, int value) {
        if (g_skip_block) return;

        for (int i = 0; i < g_sym_count; i++) {
            if (strcmp(g_sym_names[i], name) == 0) {
                g_sym_values[i] = value;
                return;
            }
        }
        if (g_sym_count < MAX_SYMBOLS) {
            g_sym_names[g_sym_count] = strdup(name);
            g_sym_values[g_sym_count] = value;
            g_sym_count++;
        }
    }

    int lookup_symbol(char* name) {
        for (int i = 0; i < g_sym_count; i++) {
            if (strcmp(g_sym_names[i], name) == 0) {
                return g_sym_values[i];
            }
        }
        printf("Error: Variable no definida '%s'. Se usará 0.\n", name);
        return 0;
    }

%}

%union {
    int ival;
    char *sval;
}

%token UTN FINUTN LEER ESCRIBIR SI ENTONCES FINSI REPETIR VECES
%token ASIGNACION SUMA RESTA MULTIPLICACION MAYOR MENOR IGUAL PUNTO
%token PAREN_IZQ PAREN_DER

%token <ival> NUMERO
%token <sval> ID

%type <ival> expresion

%left MAYOR MENOR IGUAL
%left SUMA RESTA
%left MULTIPLICACION

%%

programa: UTN lista_sentencias FINUTN { 
            printf(">> Programa 'MiUtn' ejecutado con éxito.\n"); 
        }
        ;

lista_sentencias:
                | lista_sentencias sentencia
                ;

sentencia: asignacion_stmt
        | lectura_stmt
        | escritura_stmt
        | bucle_stmt
        | condicional_stmt
        ;

asignacion_stmt: ID ASIGNACION expresion PUNTO { 
                    store_symbol($1, $3);
                    free($1); 
                }
            ;

lectura_stmt: LEER PAREN_IZQ ID PAREN_DER PUNTO {
                if (!g_skip_block) {
                    int val;
                    printf("Ingresa el valor de %s: ", $3);
                    fflush(stdout);
                    scanf("%d", &val);
                    store_symbol($3, val);
                }
                free($3);
            }
            ;

escritura_stmt: ESCRIBIR PAREN_IZQ expresion PAREN_DER PUNTO {
                    if (!g_skip_block) printf("%d\n", $3);
                }
                ;

bucle_stmt: REPETIR expresion expresion VECES PUNTO {
                if (!g_skip_block) {
                    int valor_a_repetir = $2;
                    int numero_de_veces = $3;
                    for (int i = 0; i < numero_de_veces; i++) {
                        printf("%d\n", valor_a_repetir);
                    }
                }
            }
            ;

condicional_stmt: SI PAREN_IZQ expresion PAREN_DER ENTONCES {
                    if ($3 == 0) {
                        g_skip_block = 1;
                    }
                }
                lista_sentencias FINSI {
                    g_skip_block = 0;
                }
                ;
expresion: NUMERO                   { $$ = $1; }
        | ID                       { $$ = lookup_symbol($1); free($1); }
        | expresion SUMA expresion { $$ = $1 + $3; }
        | expresion RESTA expresion { $$ = $1 - $3; }
        | expresion MULTIPLICACION expresion { $$ = $1 * $3; }
        | expresion MAYOR expresion { $$ = $1 > $3; }
        | expresion MENOR expresion { $$ = $1 < $3; }
        | expresion IGUAL expresion { $$ = $1 == $3; }
        | PAREN_IZQ expresion PAREN_DER { $$ = $2; }
        ;

%%
int main() {
    printf("--- Intérprete 'MiUtn' ---\n");
    yyparse();
    printf("---------------------------\n");
    return 0;
}

void yyerror(const char *s) {
    fprintf(stderr, "Error Sintáctico: %s\n", s);
}