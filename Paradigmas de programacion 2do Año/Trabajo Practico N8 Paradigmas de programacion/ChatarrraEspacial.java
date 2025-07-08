// Nombre alumno: Franco Genaro Reyes
public class ChatarrraEspacial {
    String tipo_chatarra;
    double peso_kg;
    int valor_monedas;

    public ChatarrraEspacial(String tipo_chatarra, double peso_kg, int valor_monedas) {
        this.tipo_chatarra = tipo_chatarra;
        this.peso_kg = peso_kg;
        this.valor_monedas = valor_monedas;
    }

    public void recolectar() {
        System.out.println("Se ha recolectado chatarra de tipo: " + tipo_chatarra);
        System.out.println("Peso: " + peso_kg + " kg");
        System.out.println("Valor: " + valor_monedas + " monedas");
    }

    public static void main(String[] args) {
        ChatarrraEspacial chatarra1 = new ChatarrraEspacial("Metal", 12.5, 100);
        chatarra1.recolectar();
    }
}
