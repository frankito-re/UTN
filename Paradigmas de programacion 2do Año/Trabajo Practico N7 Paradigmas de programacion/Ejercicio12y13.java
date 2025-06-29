// Nombre alumno: Franco Genaro Reyes
public class Ejercicio12y13 {
    public static String kebabToCamel(String texto) {
        StringBuilder resultado = new StringBuilder();
        boolean mayuscula = false;

        for (int i = 0; i < texto.length(); i++) {
            char c = texto.charAt(i);
            if (c == '-') {
                mayuscula = true;
            } else {
                if (mayuscula) {
                    resultado.append(Character.toUpperCase(c));
                    mayuscula = false;
                } else {
                    resultado.append(c);
                }
            }
        }

        return resultado.toString();
    }

    public static String soloLetras(String texto) {
        StringBuilder resultado = new StringBuilder();

        for (int i = 0; i < texto.length(); i++) {
            char c = texto.charAt(i);
            if (Character.isLetter(c)) {
                resultado.append(c);
            }
        }

        return resultado.toString();
    }
}
