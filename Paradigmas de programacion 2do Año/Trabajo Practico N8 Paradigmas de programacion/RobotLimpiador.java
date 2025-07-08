// Nombre alumno: Franco Genaro Reyes
public class RobotLimpiador {
    String nombre;
    int nivelBateria;
    String areaActual;
    boolean estaLimpiando;

    public RobotLimpiador(String nombre) {
        this.nombre = nombre;
        this.nivelBateria = 100;
        this.areaActual = "Base";
        this.estaLimpiando = false;
    }

    public void cargarBateria() {
        nivelBateria = 100;
    }

    public void limpiarHabitacion(String nombreHabitacion) {
        areaActual = nombreHabitacion;
        estaLimpiando = true;
    }

    public void detenerLimpieza() {
        estaLimpiando = false;
    }

    public static void main(String[] args) {
        RobotLimpiador robot = new RobotLimpiador("R2-D2");

        System.out.println("Nombre del robot: " + robot.nombre);
        System.out.println("Nivel de batería inicial: " + robot.nivelBateria);
        System.out.println("Área actual: " + robot.areaActual);
        System.out.println("¿Está limpiando?: " + robot.estaLimpiando);

        robot.limpiarHabitacion("Cocina");
        System.out.println("\nDespués de comenzar limpieza:");
        System.out.println("Área actual: " + robot.areaActual);
        System.out.println("¿Está limpiando?: " + robot.estaLimpiando);

        robot.detenerLimpieza();
        System.out.println("\nDespués de detener limpieza:");
        System.out.println("¿Está limpiando?: " + robot.estaLimpiando);

        robot.cargarBateria();
        System.out.println("\nDespués de cargar batería:");
        System.out.println("Nivel de batería: " + robot.nivelBateria);
    }
}