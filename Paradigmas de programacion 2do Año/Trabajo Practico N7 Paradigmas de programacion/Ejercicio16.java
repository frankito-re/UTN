
// Nombre alumno: Franco Genaro Reyes
import java.util.Random;

public class Ejercicio16 {
    public static void main(String[] args) {
        int[] arreglo = new int[20];
        Random random = new Random();

        for (int i = 0; i < arreglo.length; i++) {
            arreglo[i] = random.nextInt(2); // genera 0 o 1
        }

        // Mostrar el arreglo original
        System.out.print("Arreglo original: ");
        for (int num : arreglo) {
            System.out.print(num + " ");
        }
        System.out.println();

        int cantidadDeCeros = 0;
        for (int num : arreglo) {
            if (num == 0) {
                cantidadDeCeros++;
            }
        }

        for (int i = 0; i < arreglo.length; i++) {
            if (i < cantidadDeCeros) {
                arreglo[i] = 0;
            } else {
                arreglo[i] = 1;
            }
        }

        System.out.print("Arreglo ordenado: ");
        for (int num : arreglo) {
            System.out.print(num + " ");
        }
        System.out.println();
    }
}