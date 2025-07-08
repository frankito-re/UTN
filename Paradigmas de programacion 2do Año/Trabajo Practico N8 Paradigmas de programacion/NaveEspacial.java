// Nombre alumno: Franco Genaro Reyes
public class NaveEspacial {
    private final String nombre;
    // int capacidad_pasajeros;
    // double velocidad_maxima;
    private double combustible_actual;

    public NaveEspacial(String nombre, double combustible_actual) {
        this.nombre = nombre;
        this.combustible_actual = combustible_actual;
    }

    public void despegar() {
        System.out.println("La nave " + nombre + " despega!");
    }

    public void reabastecer(int cantidad) {
        System.out.println("Cantidad de combustible actual: " + combustible_actual);
        combustible_actual = combustible_actual + cantidad;
        System.out.println("La cantidad de combustible aumento a: " + combustible_actual);
    }

    public static void main(String[] args) {
        NaveEspacial nueva_nave = new NaveEspacial("Nave de Franco", 3);
        nueva_nave.despegar();
        nueva_nave.reabastecer(3);
    }
}
