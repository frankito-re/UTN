
// Nombre alumno: Franco Genaro Reyes
import java.util.ArrayList;
import java.util.Scanner;

public class Ejercicio23 {
    @SuppressWarnings("ConvertToTryWithResources")
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        ArrayList<String> colores = new ArrayList<>();
        String color = "";

        while (!"t".equals(color)) {
            color = input.nextLine();
            colores.add(color);
        }

        // Quitamos la última entrada 't'
        if (!colores.isEmpty() && colores.get(colores.size() - 1).equals("t")) {
            colores.remove(colores.size() - 1);
        }

        // Variables para contar
        String colorMasComun = "";
        int maxCantidad = 0;

        for (int i = 0; i < colores.size(); i++) {
            String actual = colores.get(i);
            int contador = 0;

            for (int j = 0; j < colores.size(); j++) {
                if (colores.get(j).equals(actual)) {
                    contador++;
                }
            }

            if (contador > maxCantidad) {
                maxCantidad = contador;
                colorMasComun = actual;
            }
        }

        if (!colorMasComun.isEmpty()) {
            System.out.println("El color más común fue: " + colorMasComun + " (" + maxCantidad + " veces)");
        } else {
            System.out.println("No se ingresaron colores.");
        }

        input.close();
    }
}