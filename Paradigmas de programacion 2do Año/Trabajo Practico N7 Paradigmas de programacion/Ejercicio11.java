
// Nombre alumno: Franco Genaro Reyes
import java.util.Scanner;

public class Ejercicio11 {
    @SuppressWarnings("ConvertToTryWithResources")
    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);
        System.out.print("Ingrese una frase: ");
        String phrase = input.nextLine();
        String result = ParsearTexto.chauEspacios(phrase);
        System.out.println("La frase con los espacios reemplazados es: " + result);
        input.close();
    }
}

class ParsearTexto {
    public static String chauEspacios(String texto) {
        return texto.replace(" ", "_");
    }

    // Metodo sin usar replace
    // static String chauEspacios2(String phrase) {
    // StringBuilder new_phrase = new StringBuilder();
    // for (int i = 0; i < phrase.length(); i++) {
    // if (phrase.charAt(i) == ' ') {
    // new_phrase.append('_');
    // } else {
    // new_phrase.append(phrase.charAt(i));
    // }
    // }
    // return new_phrase.toString();
    // }
}