
// Nombre alumno: Franco Genaro Reyes
import java.util.Scanner;

public class Ejercicio3 {
    @SuppressWarnings("ConvertToTryWithResources")
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Ingresa el peso de la persona: ");
        int edad = input.nextInt();
        System.out.println("Cantidad de dias que representa: " + edad * 365);
        input.close();
    }
}