// Para una partida de un juego de rol, Dungeons & Dragons, cada jugador empieza por
// generar un personaje con el cual jugaran. Este personaje que debe generar,
// tiene que tener 6 habilidades, a saber: fuerza, destreza, constitucion, inteligencia, sabiduria y carisma
// (simplificando).
// Estas seis habilidades tienen cada una, un puntaje determinado de modo aleatorio. Esto
// se consigue tirando 4 dados de rol, de 6 caras. Y calculando la suma de los tres dados de
// mayor numero (descartando el dado menor). Este proceso de tirar los 4 dados y calcular
// dicha suma de los mayores, se repite para cada habilidad, hasta poder completar el personaje.
// Ademas, tu personaje tendra una sangre o salud de 10 puntos iniciales sumado a un modificador que dependera de la constitucion de dicho personaje particular.
// Ese modificador se determina sustrayendo 10 de su constitucion, dividiendo luego por 2,
// y redondeando hacia abajo.
// Teniendo en cuenta todos esos requisitos, crear un Generador de Personaje de Dungeons
// y Dragons, aleatorio.

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