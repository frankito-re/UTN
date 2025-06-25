
// Nombre alumno: Franco Genaro Reyes
import java.util.Scanner;

public class ejercicio6 {
    @SuppressWarnings("ConvertToTryWithResources")
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Ingrese la longitud de la base: ");
        int longitud = input.nextInt();

        for (int i = 0; i < longitud; i++) {
            int numX = 2 * i + 1;
            int numEspacios = longitud - i - 1;

            for (int j = 0; j < numEspacios; j++) {
                System.out.print(" ");
            }
            for (int j = 0; j < numX; j++) {
                System.out.print("X");
            }
            System.out.println();
        }
        input.close();
    }
}
