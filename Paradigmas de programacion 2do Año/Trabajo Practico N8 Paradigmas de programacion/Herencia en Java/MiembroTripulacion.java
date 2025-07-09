// Nombre alumno: Franco Genaro Reyes
public class MiembroTripulacion {
    private final String nombre;
    private final String rango;
    private final int anosExperiencia;

    public MiembroTripulacion(String nombre, String rango, int anosExperiencia) {
        this.nombre = nombre;
        this.rango = rango;
        this.anosExperiencia = anosExperiencia;
    }

    public String getRango() {
        return rango;
    }

    public int getAnosExperiencia() {
        return anosExperiencia;
    }

    public void realizarTarea() {
        System.out.println(nombre + " está realizando una tarea general de la tripulación.");
    }

    public static void main(String[] args) {
        CientificoEspacial cientifico = new CientificoEspacial("Laura", "Teniente", 5, "Astrobiología");
        IngenieroNave ingeniero = new IngenieroNave("Carlos", "Mayor", 8, "Sistemas de Propulsión");

        cientifico.realizarTarea();
        ingeniero.realizarTarea();
    }
}

class CientificoEspacial extends MiembroTripulacion {
    private final String areaEspecializacion;

    public CientificoEspacial(String nombre, String rango, int anosExperiencia, String areaEspecializacion) {
        super(nombre, rango, anosExperiencia);
        this.areaEspecializacion = areaEspecializacion;
    }

    @Override
    public void realizarTarea() {
        super.realizarTarea();
        System.out.println("Realiza investigación en el área de " + areaEspecializacion + ".");
    }
}

class IngenieroNave extends MiembroTripulacion {
    private final String certificacionMantenimiento;

    public IngenieroNave(String nombre, String rango, int anosExperiencia, String certificacionMantenimiento) {
        super(nombre, rango, anosExperiencia);
        this.certificacionMantenimiento = certificacionMantenimiento;
    }

    @Override
    public void realizarTarea() {
        super.realizarTarea();
        System.out.println("Mantiene los sistemas usando su certificación en " + certificacionMantenimiento + ".");
    }
}
