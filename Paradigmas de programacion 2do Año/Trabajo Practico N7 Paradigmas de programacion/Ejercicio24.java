
// Nombre alumno: Franco Genaro Reyes
import java.util.ArrayList;
import java.util.List;

public class Ejercicio24 {
    @SuppressWarnings("ConvertToTryWithResources")
    public static void main(String[] args) {
        ArrayList<String> palabras = new ArrayList<>(List.of("hola", "chau"));
        ArrayList<String> resultado = repetir_elemento(palabras, 2);
        System.out.println(resultado);
    }

    static ArrayList<String> repetir_elemento(ArrayList<String> array, int cantidad_veces) {
        ArrayList<String> resultado = new ArrayList<>();
        for (String elemento : array) {
            for (int i = 0; i < cantidad_veces; i++) {
                resultado.add(elemento);
            }
        }
        return resultado;
    }
}
