// Nombre alumno: Franco Genaro Reyes
public class ProductoVending {
    private final String nombre;
    // int precio_creditos;
    private int cantidad_disponible;

    public ProductoVending(String nombre, int precio_creditos, int cantidad_disponible) {
        this.nombre = nombre;
        // this.precio_creditos = precio_creditos;
        this.cantidad_disponible = cantidad_disponible;
    }

    public void comprar() {
        if (cantidad_disponible > 0) {
            cantidad_disponible--;
            System.out.println("Producto comprado: " + nombre);
        } else {
            System.out.println("No hay stock de " + nombre);
        }
    }

    public void reponer(int cantidad) {
        if (cantidad > 0) {
            cantidad_disponible += cantidad;
            System.out.println("Se repusieron " + cantidad + " unidades de " + nombre);
        }
    }

    public static void main(String[] args) {
        ProductoVending producto = new ProductoVending("Galletitas", 5, 3);
        producto.comprar(); // Compra 1
        producto.reponer(2); // Reponer 2
        producto.comprar(); // Compra 1
    }
}
