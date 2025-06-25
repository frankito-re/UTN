// Permita ingresar una frase al usuario, y muestre las letras en posiciones alternadas, una
// si, otra no de la misma.

// Nombre alumno: Franco Genaro Reyes
import java.util.Scanner;

public class Ejercicio7 {
    @SuppressWarnings("ConvertToTryWithResources")
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Ingrese una palabra: ");
        String phrase = input.nextLine();
        input.close();
    }
}