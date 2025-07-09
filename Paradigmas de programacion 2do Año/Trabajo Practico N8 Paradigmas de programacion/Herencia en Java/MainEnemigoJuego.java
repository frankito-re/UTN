// Nombre alumno: Franco Genaro Reyes
class EnemigoJuego {
    protected String nombre;
    protected int salud;
    protected int danioAtaque;

    public EnemigoJuego(String nombre, int salud, int danioAtaque) {
        this.nombre = nombre;
        this.salud = salud;
        this.danioAtaque = danioAtaque;
    }

    public void recibirDanio(int cantidad) {
        salud -= cantidad;
        System.out.println(nombre + " recibió " + cantidad + " de daño. Salud restante: " + salud);
    }

    public void atacar(EnemigoJuego objetivo) {
        System.out.println(nombre + " ataca a " + objetivo.nombre + " causando " + danioAtaque + " de daño.");
        objetivo.recibirDanio(danioAtaque);
    }
}

class Goblin extends EnemigoJuego {
    private final String tipoArma;

    public Goblin(String nombre, int salud, int danioAtaque, String tipoArma) {
        super(nombre, salud, danioAtaque);
        this.tipoArma = tipoArma;
    }

    @Override
    public void atacar(EnemigoJuego objetivo) {
        System.out.println(nombre + " ataca con su " + tipoArma + " causando " + danioAtaque + " de daño.");
        objetivo.recibirDanio(danioAtaque);
    }
}

class Dragon extends EnemigoJuego {
    private final String alientoElemento;

    public Dragon(String nombre, int salud, int danioAtaque, String alientoElemento) {
        super(nombre, salud, danioAtaque);
        this.alientoElemento = alientoElemento;
    }

    @Override
    public void atacar(EnemigoJuego objetivo) {
        System.out
                .println(nombre + " lanza un aliento de " + alientoElemento + " causando " + danioAtaque + " de daño.");
        objetivo.recibirDanio(danioAtaque);
    }
}

public class MainEnemigoJuego {
    public static void main(String[] args) {
        Goblin goblin = new Goblin("Grunt", 100, 15, "espada");
        Dragon dragon = new Dragon("Smaug", 200, 30, "fuego");

        goblin.atacar(dragon);
        dragon.atacar(goblin);
    }
}
