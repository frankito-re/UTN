// Realizar un programita que pida al usuario 6 palabras, y las guarde en un vector. Luego
// pedirle una palabra y verificar si esta palabra existe en el vector o no.

// Nombre alumno: Franco Genaro Reyes
import java.util.Scanner;

public class Ejercicio15 {
    @SuppressWarnings("ConvertToTryWithResources")
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String[] palabras = new String[6];

        System.out.println("Ingrese 6 palabras:");

        // Agregamos las palabras en el vector
        for (int i = 0; i < palabras.length; i++) {
            System.out.print("Palabra " + (i + 1) + ": ");
            palabras[i] = sc.nextLine();
        }

        // Verificamos si la palabra se encuentra en el vector
        System.out.print("Ingrese una palabra para buscar: ");
        String palabra_elegida = sc.nextLine();
        boolean encontrada = verificar_palabra_en_vector(palabras, palabra_elegida);
        if (encontrada) {
            System.out.println("La palabra se encuentra en el vector.");
        } else {
            System.out.println("La palabra no se encuentra en el vector.");
        }
        sc.close();
    }

    // Metodo que verifica si la palabra se encuentra en el vector
    static boolean verificar_palabra_en_vector(String[] palabras, String palabra_elegida) {
        for (String palabra : palabras) {
            if (palabra.equals(palabra_elegida)) {
                return true;
            }
        }
        return false;
    }
}