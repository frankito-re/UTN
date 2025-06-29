// Nombre alumno: Franco Genaro Reyes
public class Ejercicio14 {
    public static String acronimo(String texto) {
        StringBuilder resultado = new StringBuilder();
        String[] palabras = texto.split("\\s+");

        for (String palabra : palabras) {
            if (!palabra.isEmpty() && Character.isLetter(palabra.charAt(0))) {
                resultado.append(Character.toUpperCase(palabra.charAt(0)));
            }
        }

        return resultado.toString();
    }

    public static void main(String[] args) {
        System.out.println(acronimo("Ciudad Autónoma de Buenos Aires"));
        System.out.println(acronimo("Banco Central de la República Argentina"));
        System.out.println(acronimo("A Todo Ritmo"));
        System.out.println(acronimo("Nada Que Ver"));
    }
}