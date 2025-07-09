// Nombre alumno: Franco Genaro Reyes
public class ModuloCiudad {
    // Atributos privados
    private final String tipo;
    private final int energiaConsumida;
    private int habitantesMaximos;

    // Constructor
    public ModuloCiudad(String tipo, int energiaConsumida, int habitantesMaximos) {
        this.tipo = tipo;
        this.energiaConsumida = energiaConsumida;
        this.habitantesMaximos = habitantesMaximos;
    }

    // Método para expandir el módulo
    public void expandir() {
        System.out.println("Expandiendo módulo...");
        habitantesMaximos += 100;
    }

    // Método para generar un reporte
    public void generarReporte() {
        System.out.println("Tipo de módulo: " + tipo);
        System.out.println("Energía consumida: " + energiaConsumida + " kWh");
        System.out.println("Habitantes máximos: " + habitantesMaximos);
    }

    public static void main(String[] args) {
        ModuloCiudad modulo = new ModuloCiudad("Residencial", 500, 1000);
        modulo.expandir();
        modulo.generarReporte();
    }
}
