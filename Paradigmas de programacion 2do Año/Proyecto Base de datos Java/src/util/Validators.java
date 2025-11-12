package util;

public class Validators {

    public static boolean isNotEmpty(String s) {
        return s != null && !s.trim().isEmpty();
    }

    public static boolean isPositive(int n) {
        return n > 0;
    }

    public static boolean isNotNull(Object obj) {
        return obj != null;
    }
}