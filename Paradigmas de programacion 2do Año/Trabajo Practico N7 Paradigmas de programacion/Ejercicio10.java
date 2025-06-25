
// Nombre alumno: Franco Genaro Reyes
import java.util.Scanner;

public class Ejercicio10 {
    @SuppressWarnings("ConvertToTryWithResources")
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Ingrese una palabra: ");
        String word = input.nextLine();

        // For que pide la actividad
        for (int i = 0; i < word.length(); i++) {
            char c = Character.toLowerCase(word.charAt(i));
            if (Character.isLetter(c) && "aeiou".indexOf(c) == -1) {
                System.out.println(c);
            }
        }

        // Llamamos a la funcion
        String resultado = generar_cadena(word);
        System.out.println("Cadena de consonantes: " + resultado);
        input.close();
    }

    static String generar_cadena(String word) {
        String consonantes_en_palabra = "";
        for (int i = 0; i < word.length(); i++) {
            char c = Character.toLowerCase(word.charAt(i));
            if (Character.isLetter(c) && "aeiou".indexOf(c) == -1) {
                // Genera la cadena uniendo las consonantes
                consonantes_en_palabra += c;
            }
        }
        return consonantes_en_palabra;
    }
}