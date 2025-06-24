// Nombre alumno: Franco Genaro Reyes

import java.util.Scanner;

public class Ejercicio1 {

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);  // Paso 1
        System.out.print("Ingrese una palabra: ");
        String palabra = input.nextLine();       // Leer palabra

        for (int i = 0; i < palabra.length(); i++) {  // Paso 2
            // Paso 3: imprimir espacios
            for (int j = 0; j < i; j++) {
                System.out.print(" ");
            }
            // Paso 4: imprimir letra
            System.out.println(palabra.charAt(i));
        }

        input.close();
    }
}
