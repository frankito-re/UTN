// Nombre alumno: Franco Genaro Reyes
public class SerMagico {
    protected String nombre;
    protected int longevidad;

    public SerMagico(String nombre, int longevidad) {
        this.nombre = nombre;
        this.longevidad = longevidad;
    }

    public void emitirLuz() {
        System.out.println(nombre + " emite un resplandor mágico.");
    }

    public void interactuar() {
        System.out.println(nombre + " interactúa de manera misteriosa con el entorno.");
    }

    public static void main(String[] args) {
        Hada hada = new Hada("Luzia", 120, "Plateado");
        Ent ent = new Ent("Roblen", 300, "Roble");

        hada.emitirLuz();
        hada.interactuar();

        ent.emitirLuz();
        ent.interactuar();
    }

}

class Hada extends SerMagico {
    private final String colorAlas;

    public Hada(String nombre, int longevidad, String colorAlas) {
        super(nombre, longevidad);
        this.colorAlas = colorAlas;
    }

    @Override
    public void emitirLuz() {
        System.out.println(nombre + " emite una luz brillante de color " + colorAlas + ".");
    }
}

class Ent extends SerMagico {
    private final String especieArbol;

    public Ent(String nombre, int longevidad, String especieArbol) {
        super(nombre, longevidad);
        this.especieArbol = especieArbol;
    }

    @Override
    public void interactuar() {
        System.out.println(nombre + " el " + especieArbol + " habla lentamente con sabiduría milenaria.");
    }
}