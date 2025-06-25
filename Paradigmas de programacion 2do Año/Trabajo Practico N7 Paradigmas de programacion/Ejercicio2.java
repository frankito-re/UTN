
// Nombre alumno: Franco Genaro Reyes
import java.util.Scanner;

public class Ejercicio2 {
    @SuppressWarnings("ConvertToTryWithResources")
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Ingresa el peso de la persona: ");
        int peso = input.nextInt();
        System.out.println("El peso de la persona en Marte es: " + peso * 0.38);
        input.close();
    }
}