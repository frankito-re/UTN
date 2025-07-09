// Nombre alumno: Franco Genaro Reyes
public class MascotaVirtual {
    // private String nombre;
    // private String especie;
    private int nivelHambre; // 0 a 100
    private int nivelFelicidad; // 0 a 100

    public MascotaVirtual(String nombre, String especie, int nivelHambre, int nivelFelicidad) {
        // this.nombre = nombre;
        // this.especie = especie;
        this.nivelHambre = nivelHambre;
        this.nivelFelicidad = nivelFelicidad;
    }

    public void alimentar() {
        if (nivelHambre >= 10) {
            nivelHambre -= 10;
        } else {
            nivelHambre = 0;
        }
        if (nivelFelicidad <= 90) {
            nivelFelicidad += 10;
        } else {
            nivelFelicidad = 100;
        }
    }

    public void jugar() {
        if (nivelFelicidad <= 95) {
            nivelFelicidad += 5;
        } else {
            nivelFelicidad = 100;
        }
    }
}
