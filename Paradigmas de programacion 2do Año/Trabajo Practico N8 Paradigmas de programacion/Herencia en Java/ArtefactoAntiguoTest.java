// Nombre alumno: Franco Genaro Reyes
class ArtefactoAntiguo {
    protected String nombre;
    protected String eraHistorica;
    protected double valorEstimado;

    public ArtefactoAntiguo(String nombre, String eraHistorica, double valorEstimado) {
        this.nombre = nombre;
        this.eraHistorica = eraHistorica;
        this.valorEstimado = valorEstimado;
    }

    public void examinar() {
        System.out.println("Artefacto: " + nombre + ", de la era " + eraHistorica +
                ", valuado en " + valorEstimado + " monedas.");
    }
}

class JoyeriaAntigua extends ArtefactoAntiguo {
    private final String materialPrincipal;

    public JoyeriaAntigua(String nombre, String eraHistorica, double valorEstimado, String materialPrincipal) {
        super(nombre, eraHistorica, valorEstimado);
        this.materialPrincipal = materialPrincipal;
    }

    @Override
    public void examinar() {
        System.out.println("Joyería Antigua: " + nombre + ", hecha de " + materialPrincipal +
                ", de la era " + eraHistorica + ", valuada en " + valorEstimado + " monedas.");
    }
}

class HerramientaMisteriosa extends ArtefactoAntiguo {
    private final String funcionDesconocida;

    public HerramientaMisteriosa(String nombre, String eraHistorica, double valorEstimado, String funcionDesconocida) {
        super(nombre, eraHistorica, valorEstimado);
        this.funcionDesconocida = funcionDesconocida;
    }

    @Override
    public void examinar() {
        System.out.println("Herramienta Misteriosa: " + nombre + ", de la era " + eraHistorica +
                ". Su posible función: " + funcionDesconocida +
                ". Valor estimado: " + valorEstimado + " monedas.");
    }
}

public class ArtefactoAntiguoTest {
    public static void main(String[] args) {
        JoyeriaAntigua joya = new JoyeriaAntigua("Anillo Solar", "Imperio del Fuego", 1200.5, "Oro y Rubí");
        HerramientaMisteriosa herramienta = new HerramientaMisteriosa("Llave Circular", "Edad de Bronce", 3000.0,
                "activar portales");

        joya.examinar();
        herramienta.examinar();
    }
}
