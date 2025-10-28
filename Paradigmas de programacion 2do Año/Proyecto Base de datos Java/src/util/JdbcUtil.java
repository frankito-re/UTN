package src.util;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public final class JdbcUtil {
    private static final String URL = "jdbc:mysql://localhost:3306/bd_centro_salud_Java_Project?useSSL=false&serverTimezone=UTC";
    private static final String USER = "root"; // <-- usuario
    private static final String PASS = ""; // <-- password

    static {
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
        } catch (ClassNotFoundException e) {
            throw new RuntimeException("Driver MySQL no encontrado", e);
        }
    }

    private JdbcUtil() {
    }

    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL, USER, PASS);
    }

    // helpers
    public static void closeQuietly(AutoCloseable c) {
        if (c != null)
            try {
                c.close();
            } catch (Exception ignored) {
            }
    }
}