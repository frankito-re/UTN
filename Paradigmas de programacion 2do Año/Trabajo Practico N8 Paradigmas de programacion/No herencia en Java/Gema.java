// Nombre alumno: Franco Genaro Reyes
public class Gema {
    // private final String nombre;
    // private final String color;
    private final double quilates;
    private int pureza; // Rango de 1 a 100

    public Gema(String nombre, String color, double quilates, int pureza) {
        // this.nombre = nombre;
        // this.color = color;
        this.quilates = quilates;
        this.pureza = pureza;
    }

    public void tallar() {
        if (pureza > 1 && pureza < 100) {
            pureza++;
        }
    }

    public double vender(double precio_por_quilates) {
        double valor_total = precio_por_quilates * quilates;
        return valor_total;
    }

    public static void main(String[] args) {
        Gema gema = new Gema("Diamante", "azul", 20, 30);
        gema.tallar();
        System.out.println("La nueva pureza de la gema es: " + gema.pureza);
        System.out.println("La ganancia de la venta de esta gema es: " + gema.vender(3.68));
    }
}
