package model;

public class Medico {

    private int matricula;
    private String nombre;
    private int especialidadId;
    private int consultorioId;

    // Referencias a los objetos completos
    private Especialidad especialidad;
    private Consultorio consultorio;

    public Medico() {
    }

    public Medico(int matricula, String nombre, int especialidadId, int consultorioId) {
        this.matricula = matricula;
        this.nombre = nombre;
        this.especialidadId = especialidadId;
        this.consultorioId = consultorioId;
    }

    // Getters y Setters
    public int getMatricula() {
        return matricula;
    }

    public void setMatricula(int matricula) {
        this.matricula = matricula;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public int getEspecialidadId() {
        return especialidadId;
    }

    public void setEspecialidadId(int especialidadId) {
        this.especialidadId = especialidadId;
    }

    public int getConsultorioId() {
        return consultorioId;
    }

    public void setConsultorioId(int consultorioId) {
        this.consultorioId = consultorioId;
    }

    public Especialidad getEspecialidad() {
        return especialidad;
    }

    public void setEspecialidad(Especialidad especialidad) {
        this.especialidad = especialidad;
    }

    public Consultorio getConsultorio() {
        return consultorio;
    }

    public void setConsultorio(Consultorio consultorio) {
        this.consultorio = consultorio;
    }

    @Override
    public String toString() {
        // Esto se mostrará en el JComboBox de Turnos
        return matricula + " - " + nombre + " ("
                + (especialidad != null ? especialidad.getNombre() : "Especialidad ID: " + especialidadId) + ")";
    }
}
