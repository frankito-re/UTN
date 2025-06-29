
// Nombre alumno: Franco Genaro Reyes
import java.util.Random;

public class Ejercicio19 {
    public static void main(String[] args) {
        int[][] matriz = new int[6][6];
        Random rand = new Random();

        // Llenar matriz con valores aleatorios y mostrarla
        System.out.println("Matriz generada:");
        for (int i = 0; i < 6; i++) {
            for (int j = 0; j < 6; j++) {
                matriz[i][j] = rand.nextInt(100) + 1;
                System.out.print(matriz[i][j] + "\t");
            }
            System.out.println();
        }

        // Calcular promedio de las filas pares
        int suma = 0;
        int cantidad = 0;

        for (int i = 0; i < 6; i += 2) { // filas 0, 2, 4
            for (int j = 0; j < 6; j++) {
                suma += matriz[i][j];
                cantidad++;
            }
        }

        double promedio = (double) suma / cantidad;
        System.out.println("Promedio de las filas pares: " + promedio);
    }
}
