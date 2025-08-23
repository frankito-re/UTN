import java.sql.Connection; // Importa la clase Connection para conectarse a la base de datos
import java.sql.DriverManager; // Importa la clase DriverManager para obtener la conexión
import java.sql.SQLException; // Importa la clase PreparedStatement para ejecutar consultas SQL con parámetros

public class PedirDatosDB {
    public static void main(String[] args) { // Método principal, punto de entrada del programa
        // Datos de conexión
        String url = "jdbc:mysql://localhost:3306/bd_centro_salud_Java_Project"; // URL de conexión a la base de datos
        String usuario = "Franco"; // Usuario de la base de datos
        String contraseña = ""; // Contraseña del usuario (vacía en este caso)

        // Consulta SQL
        String sql = "SELECT * FROM Paciente"; // Consulta SQL que selecciona todos los registros de la tabla clientes

        System.out.println("CLASSPATH:\n" + System.getProperty("java.class.path"));
        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            System.out.println("Driver cargado OK");
        } catch (ClassNotFoundException e) {
            System.out.println("No encuentro el driver en el classpath");
        }

        try {
            // Establecer conexión con la base de datos
            Connection conexion = DriverManager.getConnection(url, usuario, contraseña); // Crea una conexión con la BD
            System.out.println("Conexión exitosa a la base de datos."); // Mensaje si la conexión fue exitosa

            // Preparar y ejecutar la consulta
            // PreparedStatement sentencia = conexion.prepareStatement(sql); // Prepara la
            // consulta SQL
            // ResultSet resultados = sentencia.executeQuery(); // Ejecuta la consulta y
            // guarda los resultados

            // Mostrar resultados
            // System.out.println("\nListado de clientes:"); // Encabezado para mostrar los
            // clientes
            // while (resultados.next()) { // Recorre cada fila del resultado
            // int codigo = resultados.getInt("codigo"); // Obtiene el valor de la columna
            // 'codigo'
            // String apellido = resultados.getString("apellido"); // Obtiene el valor de la
            // columna 'apellido'
            // String nombre = resultados.getString("nombre"); // Obtiene el valor de la
            // columna 'nombre'
            // String dni = resultados.getString("dni"); // Obtiene el valor de la columna
            // 'dni'
            // String fechaNacimiento = resultados.getString("fecha_nacimiento"); // Obtiene
            // el valor de
            // 'fecha_nacimiento'
            // String correo = resultados.getString("correo"); // Obtiene el valor de la
            // columna 'correo'

            // Muestra los datos del cliente en consola
            // System.out.println("Código: " + codigo + ", Nombre: " + nombre + " " +
            // apellido +
            // ", DNI: " + dni + ", Fecha Nac.: " + fechaNacimiento + ", Correo: " +
            // correo);

            // Cerrar conexiones
            // resultados.close(); // Cierra el conjunto de resultados
            // sentencia.close(); // Cierra la sentencia preparada
            conexion.close(); // Cierra la conexión con la base de datos
        } catch (

        SQLException e) { // Captura errores relacionados con SQL
            System.out.println("Error al conectar o consultar la base de datos:"); // Muestra mensaje de error
            e.printStackTrace(); // Imprime el detalle del error
        }
    }
}
