
// Nombre alumno: Franco Genaro Reyes
import java.util.Random;
import java.util.Scanner;

public class Ejercicio8 {
    @SuppressWarnings("ConvertToTryWithResources")
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Ingrese una cadena: ");
        String phrase = input.nextLine();
        Random rand = new Random();
        if (phrase.length() >= 10) {
            for (int i = 0; i < 6; i++) {
                System.out.print(phrase.charAt(rand.nextInt(phrase.length())));
            }
        } else {
            System.out.print("La longitud de la cadena es menor que 10");
        }
        input.close();
    }
}
