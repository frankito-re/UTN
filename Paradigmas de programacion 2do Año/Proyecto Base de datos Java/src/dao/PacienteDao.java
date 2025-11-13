package dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import model.Paciente;
import util.JdbcUtil;

public class PacienteDao {

    private final Connection conn;

    public PacienteDao() {
        this.conn = JdbcUtil.getConnection();
    }

    public void guardar(Paciente paciente) throws SQLException {
        String sql = "INSERT INTO Paciente (dni, nombre, direccion, contacto, obra_social, historial_clinico) VALUES (?, ?, ?, ?, ?, ?)";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, paciente.getDni());
            pstmt.setString(2, paciente.getNombre());
            pstmt.setString(3, paciente.getDireccion());
            pstmt.setString(4, paciente.getContacto());
            pstmt.setString(5, paciente.getObraSocial());
            pstmt.setString(6, paciente.getHistorialClinico());
            pstmt.executeUpdate();
        }
    }

    public Paciente buscarPorId(Integer dni) throws SQLException {
        String sql = "SELECT * FROM Paciente WHERE dni = ?";
        Paciente paciente = null;
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, dni);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    paciente = pacienteMapper(rs);
                }
            }
        }
        return paciente;
    }

    public List<Paciente> buscarTodos() throws SQLException {
        String sql = "SELECT * FROM Paciente";
        List<Paciente> pacientes = new ArrayList<>();
        try (Statement stmt = conn.createStatement();
                ResultSet rs = stmt.executeQuery(sql)) {
            while (rs.next()) {
                pacientes.add(pacienteMapper(rs));
            }
        }
        return pacientes;
    }

    public void actualizar(Paciente paciente) throws SQLException {
        String sql = "UPDATE Paciente SET nombre = ?, direccion = ?, contacto = ?, obra_social = ?, historial_clinico = ? WHERE dni = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, paciente.getNombre());
            pstmt.setString(2, paciente.getDireccion());
            pstmt.setString(3, paciente.getContacto());
            pstmt.setString(4, paciente.getObraSocial());
            pstmt.setString(5, paciente.getHistorialClinico());
            pstmt.setInt(6, paciente.getDni());
            pstmt.executeUpdate();
        }
    }

    public void eliminar(Integer dni) throws SQLException {
        String sql = "DELETE FROM Paciente WHERE dni = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, dni);
            pstmt.executeUpdate();
        }
    }

    private Paciente pacienteMapper(ResultSet rs) throws SQLException {
        return new Paciente(
                rs.getInt("dni"),
                rs.getString("nombre"),
                rs.getString("direccion"),
                rs.getString("contacto"),
                rs.getString("obra_social"),
                rs.getString("historial_clinico"));
    }
}