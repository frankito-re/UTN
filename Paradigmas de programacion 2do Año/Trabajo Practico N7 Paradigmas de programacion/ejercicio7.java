
// Nombre alumno: Franco Genaro Reyes
import java.util.Scanner;

public class Ejercicio7 {
    @SuppressWarnings("ConvertToTryWithResources")
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Ingrese una palabra: ");
        String phrase = input.nextLine();
        input.close();
        for (int i = 0; i < phrase.length(); i++) {
            if (i % 2 == 0) {
                System.out.print(phrase.charAt(i));
            } else {
                System.out.print(" ");
            }
        }
    }
}