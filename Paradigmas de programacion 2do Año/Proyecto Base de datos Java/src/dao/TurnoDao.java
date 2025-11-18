package dao;

import java.sql.Connection;
import java.sql.Date;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

import model.Turno;
import util.JdbcUtil;

public class TurnoDao {

    private final Connection conn;

    public TurnoDao() {
        this.conn = JdbcUtil.getConnection();
    }

    public void guardar(Turno turno) throws SQLException {
        String sql = "INSERT INTO Turno (fecha, hora, estado, dni_paciente, matricula_medico, consultorio_id) VALUES (?, ?, ?, ?, ?, ?)";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setDate(1, turno.getFecha());
            pstmt.setTime(2, turno.getHora());
            pstmt.setString(3, turno.getEstado());
            pstmt.setInt(4, turno.getDniPaciente());
            pstmt.setInt(5, turno.getMatriculaMedico());
            pstmt.setInt(6, turno.getConsultorioId());
            pstmt.executeUpdate();
        }
    }

    public List<Turno> buscarTodos() throws SQLException {
        String sql = "SELECT * FROM Turno";
        List<Turno> turnos = new ArrayList<>();
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            try (ResultSet rs = pstmt.executeQuery()) {
                while (rs.next()) {
                    turnos.add(turnoMapper(rs));
                }
            }
        }
        return turnos;
    }

    public List<Turno> buscarPorMedicoYFecha(int matriculaMedico, Date fecha) throws SQLException {
        String sql = "SELECT * FROM Turno WHERE matricula_medico = ? AND fecha = ?";
        List<Turno> turnos = new ArrayList<>();
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, matriculaMedico);
            pstmt.setDate(2, fecha);
            try (ResultSet rs = pstmt.executeQuery()) {
                while (rs.next()) {
                    turnos.add(turnoMapper(rs));
                }
            }
        }
        return turnos;
    }

    public Turno buscarPorId(int idTurno) throws SQLException {
        String sql = "SELECT * FROM Turno WHERE id_turno = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, idTurno);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    return turnoMapper(rs);
                }
            }
        }
        return null;
    }

    public void cancelarTurno(int idTurno) throws SQLException {
        String sql = "UPDATE Turno SET estado = 'cancelado' WHERE id_turno = ?";
        try (PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, idTurno);
            pstmt.executeUpdate();
        }
    }

    private Turno turnoMapper(ResultSet rs) throws SQLException {
        Turno t = new Turno();
        t.setId(rs.getInt("id_turno"));
        t.setFecha(rs.getDate("fecha"));
        t.setHora(rs.getTime("hora"));
        t.setEstado(rs.getString("estado"));
        t.setDniPaciente(rs.getInt("dni_paciente"));
        t.setMatriculaMedico(rs.getInt("matricula_medico"));
        t.setConsultorioId(rs.getInt("consultorio_id"));
        return t;
    }
}