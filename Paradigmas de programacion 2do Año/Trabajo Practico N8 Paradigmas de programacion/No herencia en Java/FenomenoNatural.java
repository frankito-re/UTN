// Nombre alumno: Franco Genaro Reyes
public class FenomenoNatural {
    private final String tipo;
    private final int intensidad;
    private final int duracionHoras;

    public FenomenoNatural(String tipo, int intensidad, int duracionHoras) {
        this.tipo = tipo;
        this.intensidad = intensidad;
        this.duracionHoras = duracionHoras;
    }

    public void desencadenar() {
        System.out.println("¡Alerta! Un fenómeno de tipo " + tipo + " ha comenzado con una intensidad de " + intensidad
                + " y una duración estimada de " + duracionHoras + " horas.");
    }

    public void evaluarImpacto() {
        int impacto = intensidad * duracionHoras;
        if (impacto >= 50) {
            System.out.println("Impacto: Catastrófico.");
        } else if (impacto >= 20) {
            System.out.println("Impacto: Grave.");
        } else {
            System.out.println("Impacto: Moderado.");
        }
    }
}
