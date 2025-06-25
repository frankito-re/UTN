// Permita ingresar una palabra al usuario, y una letra. Reemplace las letras a que encuentre
// en la frase ingresada, por el simbolo de numeral.

// Nombre alumno: Franco Genaro Reyes

import java.util.Scanner;

public class Ejercicio9 {
    @SuppressWarnings("ConvertToTryWithResources")
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Ingrese una palabra: ");
        String word = input.nextLine();

        System.out.print("Ingrese una letra: ");
        char letter = input.nextLine().charAt(0); // Toma el primer carácter de la línea ingresada

        String newWord = "";

        for (int i = 0; i < word.length(); i++) {
            if (word.charAt(i) == letter) {
                newWord += "#";
            } else {
                newWord += word.charAt(i);
            }
        }

        System.out.println("Resultado: " + newWord);
        input.close();
    }
}
