// Nombre alumno: Franco Genaro Reyes
public class ElementoZen {
    private final String tipo;
    private int posicionX;
    private int posicionY;

    public ElementoZen(String tipo, int posicionX, int posicionY) {
        this.tipo = tipo;
        this.posicionX = posicionX;
        this.posicionY = posicionY;
    }

    public void mover(int nuevaX, int nuevaY) {
        this.posicionX = nuevaX;
        this.posicionY = nuevaY;
    }

    public void observar() {
        System.out.println("Posición del elemento (" + tipo + "): X=" + posicionX + ", Y=" + posicionY);
    }
}
