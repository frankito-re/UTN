%{
    #include <stdio.h>
    #include <stdlib.h>
    #include <string.h>

    int yylex();
    void yyerror(const char *s);

    #define MAX_SIMBOLOS 100
    char* g_tabla_nombres[MAX_SIMBOLOS];
    int   g_tabla_valores[MAX_SIMBOLOS];
    int   g_total_simbolos = 0;

    int   g_saltar_bloque = 0;

    -- strcmp (de string.h): Para comparar el nombre de la variable
    -- con los nombres que ya tiene guardados.
    -- strdup (de string.h): Para crear una copia en memoria del nombre
    -- de la variable y guardarla.
    void guardar_simbolo(char* nombre, int valor) {
        if (g_saltar_bloque) return;

        for (int i = 0; i < g_total_simbolos; i++) {
            if (strcmp(g_tabla_nombres[i], nombre) == 0) {
                g_tabla_valores[i] = valor;
                return;
            }
        }
        
        if (g_total_simbolos < MAX_SIMBOLOS) {
            g_tabla_nombres[g_total_simbolos] = strdup(nombre);
            g_tabla_valores[g_total_simbolos] = valor;
            g_total_simbolos++;
        }
    }

    -- - strcmp (de string.h): Para comparar el nombre que busca con
    -- los nombres guardados en la tabla.
    -- - printf (de stdio.h): Para imprimir un mensaje de error si
    -- no encuentra la variable.

    int buscar_simbolo(char* nombre) {
        for (int i = 0; i < g_total_simbolos; i++) {
            if (strcmp(g_tabla_nombres[i], nombre) == 0) {
                return g_tabla_valores[i];
            }
        }
        printf("Error: Variable no definida '%s'.\n", nombre);
        return 0;
    }
%}

%union {
    int   valor_entero;
    char* valor_cadena;
}

%token UTN FINUTN LEER ESCRIBIR SI ENTONCES FINSI REPETIR VECES
%token ASIGNACION SUMA RESTA MULTIPLICACION MAYOR MENOR IGUAL PUNTO
%token PAREN_IZQ PAREN_DER

%token <valor_entero> NUMERO
%token <valor_cadena> ID

%type <valor_entero> expresion

%left MAYOR MENOR IGUAL
%left SUMA RESTA
%left MULTIPLICACION

%%

programa: UTN lista_sentencias FINUTN { 
            printf(">> Programa 'MiUtn' ejecutado con éxito.\n"); 
        }
        ;

lista_sentencias: -- vacía
                | lista_sentencias sentencia
                ;

sentencia: asignacion_stmt
        | lectura_stmt
        | escritura_stmt
        | bucle_stmt
        | condicional_stmt
        ;

asignacion_stmt: ID ASIGNACION expresion PUNTO { 
                    guardar_simbolo($1, $3); 
                    -- free (de stdlib.h) se usa aquí para liberar la memoria que se reservó con 'strdup' en el scanner.
                    free($1); 
                }
            ;

lectura_stmt: LEER PAREN_IZQ ID PAREN_DER PUNTO {
                if (!g_saltar_bloque) { 
                    int valor_leido;
                    printf("Ingresa el valor de %s: ", $3);
                    -- fflush (de stdio.h) fuerza a que se imprima el 'printf' anterior antes de esperar el 'scanf'.

                    fflush(stdout);
                    
                    -- scanf (de stdio.h) se usa para leer el número que el usuario escribe en la terminal.
                    scanf("%d", &valor_leido);
                    guardar_simbolo($3, valor_leido);
                }
                free($3); -- free (de stdlib.h) libera el ID
            }
            ;

escritura_stmt: ESCRIBIR PAREN_IZQ expresion PAREN_DER PUNTO {
                    if (!g_saltar_bloque) printf("%d\n", $3);
                }
                ;

bucle_stmt: REPETIR expresion expresion VECES PUNTO {
                if (!g_saltar_bloque) {
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
                        g_saltar_bloque = 1;
                    }
                }
                lista_sentencias FINSI {
                    g_saltar_bloque = 0;
                }
                ;

expresion: NUMERO                   { $$ = $1; }
        | ID                       { $$ = buscar_simbolo($1); free($1);}
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
    -- yyparse (de bison): Esta no es de C, es la función que Bison genera para iniciar el análisis.
    yyparse();
    printf("---------------------------\n");
    return 0;
}

-- fprintf (de stdio.h): Es como 'printf', pero te permite elegir dónde escribir (en este caso, 'stderr', la salida estándar de errores).
void yyerror(const char *s) {
    fprintf(stderr, "Error Sintáctico: %s\n", s);
}