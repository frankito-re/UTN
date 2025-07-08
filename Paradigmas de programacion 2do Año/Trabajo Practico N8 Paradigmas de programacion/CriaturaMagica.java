// Nombre alumno: Franco Genaro Reyes
public class CriaturaMagica {
    private final String nombre;
    private final String tipo_elemento;
    // int nivel_poder;
    private boolean esta_domesticada;

    public CriaturaMagica(String nombre, String tipoElemento, int nivelPoder) {
        this.nombre = nombre;
        this.tipo_elemento = tipoElemento;
        // this.nivel_poder = nivelPoder;
        this.esta_domesticada = false;
    }

    public void lanzarHechizo() {
        System.out.println(nombre + " lanza un hechizo de " + tipo_elemento + "!");
    }

    public void intentarDomesticar() {
        if (!esta_domesticada) {
            esta_domesticada = true;
            System.out.println(nombre + " ha sido domesticada.");
        } else {
            System.out.println(nombre + " ya está domesticada.");
        }
    }
}