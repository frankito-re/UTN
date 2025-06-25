
// Nombre alumno: Franco Genaro Reyes
import java.util.Arrays;
import java.util.Random;

public class Ejercicio5 {
    public static void main(String[] args) {
        String nombre = "Aldur";

        int fuerza = tirarHabilidad();
        int destreza = tirarHabilidad();
        int constitucion = tirarHabilidad();
        int inteligencia = tirarHabilidad();
        int sabiduria = tirarHabilidad();
        int carisma = tirarHabilidad();

        int modificadorConstitucion = (constitucion - 10) / 2;
        int salud = 10 + modificadorConstitucion;

        System.out.println("Nombre: " + nombre);
        System.out.println("Fuerza: " + fuerza);
        System.out.println("Destreza: " + destreza);
        System.out.println("Constitución: " + constitucion);
        System.out.println("Inteligencia: " + inteligencia);
        System.out.println("Sabiduría: " + sabiduria);
        System.out.println("Carisma: " + carisma);
        System.out.println("Salud (HP): " + salud);
    }

    public static int tirarHabilidad() {
        Random rand = new Random();
        int[] dados = new int[4];
        for (int i = 0; i < 4; i++) {
            dados[i] = rand.nextInt(6) + 1;
        }
        Arrays.sort(dados);
        return dados[1] + dados[2] + dados[3];
    }
}