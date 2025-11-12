package model;

import java.sql.Date;
import java.sql.Time;

public class Turno {

    private int id;
    private Date fecha;
    private Time hora;
    private String estado;
    private int dniPaciente;
    private int matriculaMedico;
    private int consultorioId;

    // Referencias a los objetos completos
    private Paciente paciente;
    private Medico medico;

    public Turno() {
    }

    public Turno(Date fecha, Time hora, int dniPaciente, int matriculaMedico, int consultorioId) {
        this.fecha = fecha;
        this.hora = hora;
        this.dniPaciente = dniPaciente;
        this.matriculaMedico = matriculaMedico;
        this.consultorioId = consultorioId;
        this.estado = "pendiente"; // Estado por defecto
    }

    // Getters y Setters
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public Date getFecha() {
        return fecha;
    }

    public void setFecha(Date fecha) {
        this.fecha = fecha;
    }

    public Time getHora() {
        return hora;
    }

    public void setHora(Time hora) {
        this.hora = hora;
    }

    public String getEstado() {
        return estado;
    }

    public void setEstado(String estado) {
        this.estado = estado;
    }

    public int getDniPaciente() {
        return dniPaciente;
    }

    public void setDniPaciente(int dniPaciente) {
        this.dniPaciente = dniPaciente;
    }

    public int getMatriculaMedico() {
        return matriculaMedico;
    }

    public void setMatriculaMedico(int matriculaMedico) {
        this.matriculaMedico = matriculaMedico;
    }

    public int getConsultorioId() {
        return consultorioId;
    }

    public void setConsultorioId(int consultorioId) {
        this.consultorioId = consultorioId;
    }

    public Paciente getPaciente() {
        return paciente;
    }

    public void setPaciente(Paciente paciente) {
        this.paciente = paciente;
    }

    public Medico getMedico() {
        return medico;
    }

    public void setMedico(Medico medico) {
        this.medico = medico;
    }

    @Override
    public String toString() {
        String pacNombre = (paciente != null) ? paciente.getNombre() : "DNI(" + dniPaciente + ")";
        String medNombre = (medico != null) ? medico.getNombre() : "Mat(" + matriculaMedico + ")";
        return "Turno [ID=" + id + ", Fecha=" + fecha + ", Hora=" + hora + ", Estado=" + estado
                + ", Paciente=" + pacNombre + ", Medico=" + medNombre + "]";
    }
}
