
// Nombre alumno: Franco Genaro Reyes
import java.util.Scanner;

public class Ejercicio4 {
    @SuppressWarnings("ConvertToTryWithResources")
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Ingresar el numero: ");
        int numero = input.nextInt();
        int original = numero;
        int suma = 0;
        int digitos = String.valueOf(numero).length(); // Cantidad de dígitos

        while (numero > 0) {
            int digito = numero % 10;
            suma += Math.pow(digito, digitos);
            numero /= 10;
        }

        if (suma == original) {
            System.out.println(original + " es un número de Armstrong.");
        } else {
            System.out.println(original + " no es un número de Armstrong.");
        }
        input.close();
    }
}
