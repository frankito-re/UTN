// Nombre alumno: Franco Genaro Reyes
class GlitcheDigital {
    protected String tipo;
    protected int gravedad;

    public GlitcheDigital(String tipo, int gravedad) {
        this.tipo = tipo;
        this.gravedad = gravedad;
    }

    public void manifestarse() {
        System.out.println("El glitch digital de tipo " + tipo + " se manifiesta con gravedad " + gravedad + ".");
    }

    public static void main(String[] args) {
        GlitcheGrafico glitch1 = new GlitcheGrafico("Pixelado", 7, "Rojo");
        GlitcheSonoro glitch2 = new GlitcheSonoro("Distorsión", 5, 440);

        glitch1.manifestarse();
        glitch2.manifestarse();
    }
}

class GlitcheGrafico extends GlitcheDigital {
    private final String color_dominante;

    public GlitcheGrafico(String tipo, int gravedad, String color_dominante) {
        super(tipo, gravedad);
        this.color_dominante = color_dominante;
    }

    @Override
    public void manifestarse() {
        System.out.println("Glitch gráfico de tipo " + tipo + " con gravedad " + gravedad +
                " se manifiesta con un color dominante " + color_dominante + ".");
    }
}

class GlitcheSonoro extends GlitcheDigital {
    private final int frecuenciaHz;

    public GlitcheSonoro(String tipo, int gravedad, int frecuenciaHz) {
        super(tipo, gravedad);
        this.frecuenciaHz = frecuenciaHz;
    }

    @Override
    public void manifestarse() {
        System.out.println("Glitch sonoro de tipo " + tipo + " con gravedad " + gravedad +
                " se manifiesta con una frecuencia de " + frecuenciaHz + " Hz.");
    }
}