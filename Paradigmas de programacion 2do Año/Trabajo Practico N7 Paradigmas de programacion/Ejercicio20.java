// Nombre alumno: Franco Genaro Reyes
public class Ejercicio20 {
    public static void main(String[] args) {
        // Fragmento 1 usando while
        int suma = 0;
        int i = 0;
        while (i < 500) {
            suma = suma + i;
            System.out.println(suma + " " + i);
            i++;
        }

        // Fragmento 2 usando while
        int[] arraySillas = { 1, 0, 1, 1, 0, 0, 1 }; // ejemplo de arreglo
        int sillas = 0;
        int j = 0;
        while (j < arraySillas.length) {
            if (arraySillas[j] == 1) {
                sillas = sillas + 1;
            }
            j++;
        }
        System.out.println(sillas);
    }
}
