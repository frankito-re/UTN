package dao;

import java.sql.SQLException;
import java.util.List;

/**
 * Interfaz CRUD genérica (Contrato).
 * Define las operaciones básicas que todo DAO debe tener.
 * <T> es el tipo de objeto (Modelo)
 * <K> es el tipo de la clave primaria (Integer, Long, String)
 */
public interface CrudDao<T, K> {

    // CREATE
    void guardar(T entidad) throws SQLException;

    // READ (one)
    T buscarPorId(K id) throws SQLException;

    // READ (all)
    List<T> buscarTodos() throws SQLException;

    // UPDATE
    void actualizar(T entidad) throws SQLException;

    // DELETE
    void eliminar(K id) throws SQLException;
}
