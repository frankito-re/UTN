// Nombre alumno: Franco Genaro Reyes
public class Conjuro {
    private final String nombre;
    private final String efecto;
    // private final int manaRequerido;
    private final String nivelDificultad;

    public Conjuro(String nombre, String efecto, int manaRequerido, String nivelDificultad) {
        this.nombre = nombre;
        this.efecto = efecto;
        // this.manaRequerido = manaRequerido;
        this.nivelDificultad = nivelDificultad;
    }

    public void lanzar() {
        System.out.println("✨ Efecto del conjuro '" + nombre + "': " + efecto);
    }

    public void aprender() {
        System.out.println("📖 Has aprendido el conjuro '" + nombre + "' de dificultad " + nivelDificultad + "!");
    }

    public static void main(String[] args) {
        Conjuro c1 = new Conjuro("Fuego Infernal", "Invoca una explosión de fuego", 50, "Difícil");
        c1.aprender();
        c1.lanzar();
    }
}