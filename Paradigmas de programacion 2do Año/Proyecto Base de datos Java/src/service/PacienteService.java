package service;

import dao.PacienteDao;
import model.Paciente;
import util.Validators;

import java.sql.SQLException;
import java.util.List;

public class PacienteService {

    private PacienteDao pacienteDao;

    public PacienteService() {
        this.pacienteDao = new PacienteDao();
    }

    public void registrarPaciente(Paciente paciente) throws Exception {
        if (!Validators.isPositive(paciente.getDni()) || !Validators.isNotEmpty(paciente.getNombre())) {
            throw new IllegalArgumentException("DNI y Nombre son obligatorios.");
        }
        try {
            if (pacienteDao.buscarPorId(paciente.getDni()) != null) {
                throw new IllegalArgumentException("Ya existe un paciente con el DNI " + paciente.getDni());
            }
            pacienteDao.guardar(paciente);
        } catch (SQLException e) {
            throw new Exception("Error BD al registrar paciente: " + e.getMessage());
        }
    }

    public Paciente buscarPaciente(int dni) throws Exception {
        try {
            return pacienteDao.buscarPorId(dni);
        } catch (SQLException e) {
            throw new Exception("Error BD al buscar paciente: " + e.getMessage());
        }
    }

    public List<Paciente> listarPacientes() throws Exception {
        try {
            return pacienteDao.buscarTodos();
        } catch (SQLException e) {
            throw new Exception("Error BD al listar pacientes: " + e.getMessage());
        }
    }

    public void actualizarPaciente(Paciente paciente) throws Exception {
        if (!Validators.isPositive(paciente.getDni()) || !Validators.isNotEmpty(paciente.getNombre())) {
            throw new IllegalArgumentException("DNI y Nombre son obligatorios.");
        }
        try {
            if (pacienteDao.buscarPorId(paciente.getDni()) == null) {
                throw new IllegalArgumentException(
                        "No se puede actualizar. No existe paciente con DNI " + paciente.getDni());
            }
            pacienteDao.actualizar(paciente);
        } catch (SQLException e) {
            throw new Exception("Error BD al actualizar paciente: " + e.getMessage());
        }
    }

    public void eliminarPaciente(int dni) throws Exception {
        if (!Validators.isPositive(dni)) {
            throw new IllegalArgumentException("El DNI debe ser un número positivo.");
        }
        try {
            if (pacienteDao.buscarPorId(dni) == null) {
                throw new IllegalArgumentException("No se puede eliminar. No existe paciente con DNI " + dni);
            }
            pacienteDao.eliminar(dni);
        } catch (SQLException e) {
            if (e.getErrorCode() == 1451) { // Error de MySQL para FK constraint
                throw new Exception("No se puede eliminar: el paciente tiene turnos asociados.");
            }
            throw new Exception("Error BD al eliminar paciente: " + e.getMessage());
        }
    }
}