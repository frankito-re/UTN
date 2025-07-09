// Nombre alumno: Franco Genaro Reyes
public class ItemInventario {
    private final String nombre;
    private final String tipo;
    // private final double peso;
    // private final int valorOro;

    public ItemInventario(String nombre, String tipo, double peso, int valorOro) {
        this.nombre = nombre;
        this.tipo = tipo;
        // this.peso = peso;
        // this.valorOro = valorOro;
    }

    public void usar() {
        System.out.println("Usando " + nombre + ": ¡El ítem está siendo utilizado según su tipo (" + tipo + ")!");
    }

    public void descartar() {
        System.out.println("Descartando " + nombre + ": El ítem ha sido dejado en la mazmorra.");
    }
}