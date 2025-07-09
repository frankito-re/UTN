// Nombre alumno: Franco Genaro Reyes
public class Pocion {
    final private String nombre;
    // final private String color;
    final private String efecto;
    final private int tiempoDuracionMinutos;

    public Pocion(String nombre, String color, String efecto, int tiempoDuracionMinutos) {
        this.nombre = nombre;
        // this.color = color;
        this.efecto = efecto;
        this.tiempoDuracionMinutos = tiempoDuracionMinutos;
    }

    public void mezclarIngredientes() {
        System.out.println("Mezclando ingredientes para la pocion " + nombre + "...");
    }

    public void beberPocion() {
        System.out.println(
                nombre + " fue bebida. ¡El efecto es " + efecto + " durante " + tiempoDuracionMinutos + " minutos!");
    }

    public static void main(String[] args) {
        Pocion pocion = new Pocion("Poción de invisibilidad", "transparente", "invisibilidad", 10);
        pocion.mezclarIngredientes();
        pocion.beberPocion();
    }
}
