// Nombre alumno: Franco Genaro Reyes
public class Ejercicio21 {
    public static void main(String[] args) {
        int[][] matriz = new int[20][20];
        int max = Integer.MIN_VALUE;

        for (int i = 0; i < 20; i++) {
            for (int j = 0; j < 20; j++) {
                matriz[i][j] = (int) (Math.random() * 100); // valores entre 0 y 99
                if (matriz[i][j] > max) {
                    max = matriz[i][j];
                }
            }
        }

        System.out.println("El valor máximo de la matriz es: " + max);
    }
}