package service;

import java.sql.SQLException;
import java.util.List;

import dao.ConsultorioDao;
import dao.EspecialidadDao;
import dao.MedicoDao;
import model.Consultorio;
import model.Especialidad;
import model.Medico;
import util.Validators;

/**
 * Servicio para Medico (Gerente).
 * Valida datos (incluyendo FKs) y llama al MedicoDao.
 */
public class MedicoService {

    private final MedicoDao medicoDao;
    private final EspecialidadDao especialidadDao; // Necesario para validar FK
    private final ConsultorioDao consultorioDao; // Necesario para validar FK

    public MedicoService() {
        this.medicoDao = new MedicoDao();
        this.especialidadDao = new EspecialidadDao();
        this.consultorioDao = new ConsultorioDao();
    }

    public void registrarMedico(Medico medico) throws Exception {
        if (!Validators.isPositive(medico.getMatricula()) || !Validators.isNotEmpty(medico.getNombre())) {
            throw new IllegalArgumentException("Matrícula y Nombre son obligatorios.");
        }

        try {
            if (medicoDao.buscarPorId(medico.getMatricula()) != null) {
                throw new IllegalArgumentException("Ya existe un médico con la matrícula " + medico.getMatricula());
            }

            if (especialidadDao.buscarPorId(medico.getEspecialidadId()) == null) {
                throw new IllegalArgumentException("La Especialidad ID " + medico.getEspecialidadId() + " no existe.");
            }
            if (consultorioDao.buscarPorId(medico.getConsultorioId()) == null) {
                throw new IllegalArgumentException("El Consultorio ID " + medico.getConsultorioId() + " no existe.");
            }

            medicoDao.guardar(medico);

        } catch (SQLException e) {
            throw new Exception("Error BD al registrar médico: " + e.getMessage());
        }
    }

    public Medico buscarMedico(int matricula) throws Exception {
        try {
            return medicoDao.buscarPorId(matricula);
        } catch (SQLException e) {
            throw new Exception("Error BD al buscar médico: " + e.getMessage());
        }
    }

    public List<Medico> listarMedicos() throws Exception {
        try {
            List<Medico> medicos = medicoDao.buscarTodos();
            for (Medico m : medicos) {
                Especialidad e = especialidadDao.buscarPorId(m.getEspecialidadId());
                if (e != null)
                    m.setEspecialidad(e);
            }
            return medicos;
        } catch (SQLException e) {
            throw new Exception("Error BD al listar médicos: " + e.getMessage());
        }
    }

    public void actualizarMedico(Medico medico) throws Exception {
        // ... (Validaciones similares)
        try {
            medicoDao.actualizar(medico);
        } catch (SQLException e) {
            throw new Exception("Error BD al actualizar médico: " + e.getMessage());
        }
    }

    public void eliminarMedico(int matricula) throws Exception {
        try {
            medicoDao.eliminar(matricula);
        } catch (SQLException e) {
            if (e.getErrorCode() == 1451) {
                throw new Exception("No se puede eliminar: el médico tiene turnos asociados.");
            }
            throw new Exception("Error BD al eliminar médico: " + e.getMessage());
        }
    }

    // --- Métodos de ayuda para la GUI ---
    public List<Especialidad> listarEspecialidades() throws Exception {
        try {
            return especialidadDao.buscarTodos();
        } catch (SQLException e) {
            throw new Exception("Error BD al listar especialidades: " + e.getMessage());
        }
    }

    public List<Consultorio> listarConsultorios() throws Exception {
        try {
            return consultorioDao.buscarTodos();
        } catch (SQLException e) {
            throw new Exception("Error BD al listar consultorios: " + e.getMessage());
        }
    }
}