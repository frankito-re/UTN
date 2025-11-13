package dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import model.Consultorio;
import util.JdbcUtil;

/**
 * DAO (Clase) para Consultorio.
 */
public class ConsultorioDao {

    private final Connection conn;

    public ConsultorioDao() {
        this.conn = JdbcUtil.getConnection();
    }

    public Consultorio buscarPorId(Integer id) throws SQLException {
        String sql = "SELECT * FROM Consultorio WHERE id_consultorio = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, id);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    return new Consultorio(rs.getInt("id_consultorio"), rs.getString("ubicacion"));
                }
            }
        }
        return null;
    }

    public List<Consultorio> buscarTodos() throws SQLException {
        String sql = "SELECT * FROM Consultorio";
        List<Consultorio> lista = new ArrayList<>();
        try (Statement stmt = conn.createStatement();
                ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                lista.add(new Consultorio(rs.getInt("id_consultorio"), rs.getString("ubicacion")));
            }
        }
        return lista;
    }
}
