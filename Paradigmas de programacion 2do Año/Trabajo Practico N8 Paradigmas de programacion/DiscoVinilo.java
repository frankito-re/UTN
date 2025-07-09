// Nombre alumno: Franco Genaro Reyes
public class DiscoVinilo {
    private final String tituloAlbum;
    private final String artista;
    // private final String genero;
    private final String estado;

    public DiscoVinilo(String tituloAlbum, String artista, String genero, String estado) {
        this.tituloAlbum = tituloAlbum;
        this.artista = artista;
        // this.genero = genero;
        this.estado = estado;
    }

    public void reproducirLadoA() {
        System.out.println("Reproduciendo el lado A del álbum: " + tituloAlbum + " de " + artista + ".");
    }

    public void evaluarEstado() {
        System.out.println("Estado actual del vinilo: " + estado);
    }

    public static void main(String[] args) {
        DiscoVinilo disco = new DiscoVinilo("Abbey Road", "The Beatles", "Rock", "Excelente");
        disco.reproducirLadoA();
        disco.evaluarEstado();
    }
}
