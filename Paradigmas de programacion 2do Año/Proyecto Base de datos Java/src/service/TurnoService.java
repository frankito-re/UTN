package service;

import dao.MedicoDao;
import dao.PacienteDao;
import dao.TurnoDao;
import model.Medico;
import model.Paciente;
import model.Turno;

import java.sql.Date;
import java.sql.SQLException;
import java.sql.Time;
import java.util.List;

/**
 * Servicio para Turno (Gerente).
 * ESTA ES LA LÓGICA DE NEGOCIO MÁS IMPORTANTE.
 */
public class TurnoService {

    private TurnoDao turnoDao;
    private PacienteDao pacienteDao;
    private MedicoDao medicoDao;

    public TurnoService() {
        this.turnoDao = new TurnoDao();
        this.pacienteDao = new PacienteDao();
        this.medicoDao = new MedicoDao();
    }

    /**
     * Lógica principal: Asignar un turno validando todo.
     */
    public void asignarTurno(Turno turno) throws Exception {

        Paciente p = pacienteDao.buscarPorId(turno.getDniPaciente());
        if (p == null) {
            throw new IllegalArgumentException("El paciente con DNI " + turno.getDniPaciente() + " no existe.");
        }

        Medico m = medicoDao.buscarPorId(turno.getMatriculaMedico());
        if (m == null) {
            throw new IllegalArgumentException("El médico con matrícula " + turno.getMatriculaMedico() + " no existe.");
        }

        if (!verificarDisponibilidad(turno.getMatriculaMedico(), turno.getFecha(), turno.getHora())) {
            throw new IllegalArgumentException("El médico no está disponible en esa fecha y hora.");
        }

        turno.setConsultorioId(m.getConsultorioId());

        try {
            turnoDao.guardar(turno);
        } catch (SQLException e) {
            throw new Exception("Error BD al guardar el turno: " + e.getMessage());
        }
    }

    /**
     * Lógica clave: Verifica si un médico ya tiene un turno en una fecha/hora.
     */
    private boolean verificarDisponibilidad(int matriculaMedico, Date fecha, Time hora) throws SQLException {
        List<Turno> turnosDelDia = turnoDao.buscarPorMedicoYFecha(matriculaMedico, fecha);

        for (Turno turnoExistente : turnosDelDia) {
            // Comparamos si la hora del turno nuevo es igual a la de un turno existente
            // (Una lógica más avanzada compararía rangos, ej. 30 minutos)
            if (turnoExistente.getHora().equals(hora)) {
                return false; // ¡Conflicto!
            }
        }

        return true; // No hubo conflictos.
    }

    public List<Turno> listarTurnos() throws Exception {
        try {
            List<Turno> turnos = turnoDao.buscarTodos();
            for (Turno t : turnos) {
                // Enriquecemos el turno con los objetos Paciente y Medico
                Paciente p = pacienteDao.buscarPorId(t.getDniPaciente());
                if (p != null)
                    t.setPaciente(p);

                Medico m = medicoDao.buscarPorId(t.getMatriculaMedico());
                if (m != null)
                    t.setMedico(m);
            }
            return turnos;
        } catch (SQLException e) {
            throw new Exception("Error BD al listar turnos: " + e.getMessage());
        }
    }

    public void cancelarTurno(int idTurno) throws Exception {
        try {
            if (turnoDao.buscarPorId(idTurno) == null) {
                throw new IllegalArgumentException("No existe turno con ID " + idTurno);
            }
            turnoDao.cancelarTurno(idTurno);
        } catch (SQLException e) {
            throw new Exception("Error BD al cancelar turno: " + e.getMessage());
        }
    }
}