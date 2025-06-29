// Nombre alumno: Franco Genaro Reyes
public class Ejercicio18 {
    public static void main(String[] args) {
        // Crear una matriz 10x10
        int[][] matriz = new int[10][10];
        int sumaDiagonal = 0;

        // Llenar la matriz
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 10; j++) {
                if (i == j) {
                    matriz[i][j] = i;
                    sumaDiagonal += i;
                } else {
                    matriz[i][j] = 0;
                }
            }
        }

        // Imprimir la matriz
        for (int i = 0; i < 10; i++) {
            for (int j = 0; j < 10; j++) {
                System.out.print(matriz[i][j] + " ");
            }
            System.out.println();
        }

        // Mostrar la suma de la diagonal
        System.out.println("Suma de los elementos de la diagonal: " + sumaDiagonal);
    }
}
