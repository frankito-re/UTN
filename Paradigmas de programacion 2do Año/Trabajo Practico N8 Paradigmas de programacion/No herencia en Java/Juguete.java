// Nombre alumno: Franco Genaro Reyes
public class Juguete {
    private final String nombre;
    private final String material;
    private boolean defectuoso;
    // private final double precio;

    public Juguete(String nombre, String material, double precio) {
        this.nombre = nombre;
        this.material = material;
        // this.precio = precio;
        this.defectuoso = false;
    }

    public void inspeccionar() {
        if (material.equalsIgnoreCase("plástico") && nombre.equalsIgnoreCase("robot")) {
            defectuoso = true;
        }
    }

    public void reparar() {
        defectuoso = false;
    }

    public static void main(String[] args) {
        // Crear un juguete
        Juguete juguete1 = new Juguete("Robot", "Plástico", 100.0);

        // Inspeccionar el juguete
        juguete1.inspeccionar();

        // Verificar si es defectuoso
        juguete1.inspeccionar();

        if (juguete1.defectuoso) {
            System.out.println("El juguete está defectuoso. Se va a reparar.");
            juguete1.reparar();
        } else {
            System.out.println("El juguete está en buenas condiciones.");
        }

        // Verificar estado final
        System.out.println("¿Está defectuoso? " + juguete1.defectuoso);
    }
}
