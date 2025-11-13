package dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import model.Medico;
import util.JdbcUtil;

public class MedicoDao {

    private final Connection conn;

    public MedicoDao() {
        this.conn = JdbcUtil.getConnection();
    }

    public void guardar(Medico medico) throws SQLException {
        String sql = "INSERT INTO Medico (matricula, nombre, especialidad_id, consultorio_id) VALUES (?, ?, ?, ?)";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, medico.getMatricula());
            pstmt.setString(2, medico.getNombre());
            pstmt.setInt(3, medico.getEspecialidadId());
            pstmt.setInt(4, medico.getConsultorioId());
            pstmt.executeUpdate();
        }
    }

    public Medico buscarPorId(Integer matricula) throws SQLException {
        String sql = "SELECT * FROM Medico WHERE matricula = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, matricula);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    return medicoMapper(rs);
                }
            }
        }
        return null;
    }

    public List<Medico> buscarTodos() throws SQLException {
        String sql = "SELECT * FROM Medico";
        List<Medico> medicos = new ArrayList<>();
        try (Statement stmt = conn.createStatement();
                ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                medicos.add(medicoMapper(rs));
            }
        }
        return medicos;
    }

    public void actualizar(Medico medico) throws SQLException {
        String sql = "UPDATE Medico SET nombre = ?, especialidad_id = ?, consultorio_id = ? WHERE matricula = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, medico.getNombre());
            pstmt.setInt(2, medico.getEspecialidadId());
            pstmt.setInt(3, medico.getConsultorioId());
            pstmt.setInt(4, medico.getMatricula());
            pstmt.executeUpdate();
        }
    }

    public void eliminar(Integer matricula) throws SQLException {
        String sql = "DELETE FROM Medico WHERE matricula = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, matricula);
            pstmt.executeUpdate();
        }
    }

    private Medico medicoMapper(ResultSet rs) throws SQLException {
        return new Medico(
                rs.getInt("matricula"),
                rs.getString("nombre"),
                rs.getInt("especialidad_id"),
                rs.getInt("consultorio_id"));
    }
}
