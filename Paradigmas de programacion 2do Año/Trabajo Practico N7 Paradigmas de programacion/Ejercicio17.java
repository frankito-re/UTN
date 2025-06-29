// Nombre alumno: Franco Genaro Reyes
public class Ejercicio17 {
    public static void main(String[] args) {
        int[][] matrix = {
                { 9, 5, 0, -3 },
                { 7, -2, 8, 1 },
                { 3, 5, 7, 8 },
                { 6, 3, 0, -1 }
        };
        int suma = 0;

        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                if (i != j) {
                    suma += matrix[i][j];
                }
            }
        }

        System.out.println("La suma de los elementos que no están en la diagonal principal es: " + suma);
    }
}