package dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import model.Especialidad;
import util.JdbcUtil;

/**
 * DAO (Clase) para Especialidad.
 */
public class EspecialidadDao {

    private final Connection conn;

    public EspecialidadDao() {
        this.conn = JdbcUtil.getConnection();
    }

    public Especialidad buscarPorId(Integer id) throws SQLException {
        String sql = "SELECT * FROM Especialidad WHERE id_especialidad = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, id);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    return new Especialidad(rs.getInt("id_especialidad"), rs.getString("nombre"));
                }
            }
        }
        return null;
    }

    public List<Especialidad> buscarTodos() throws SQLException {
        String sql = "SELECT * FROM Especialidad";
        List<Especialidad> lista = new ArrayList<>();
        try (Statement stmt = conn.createStatement();
                ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                lista.add(new Especialidad(rs.getInt("id_especialidad"), rs.getString("nombre")));
            }
        }
        return lista;
    }
}
