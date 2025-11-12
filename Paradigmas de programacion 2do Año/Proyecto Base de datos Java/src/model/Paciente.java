package model;

/**
 * Modelo (POJO) que representa a un Paciente.
 */
public class Paciente {

    private int dni;
    private String nombre;
    private String direccion;
    private String contacto;
    private String obraSocial;
    private String historialClinico;

    // Constructor vacío
    public Paciente() {
    }

    // Constructor para crear
    public Paciente(int dni, String nombre, String direccion, String contacto, String obraSocial,
            String historialClinico) {
        this.dni = dni;
        this.nombre = nombre;
        this.direccion = direccion;
        this.contacto = contacto;
        this.obraSocial = obraSocial;
        this.historialClinico = historialClinico;
    }

    // Getters y Setters
    public int getDni() {
        return dni;
    }

    public void setDni(int dni) {
        this.dni = dni;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getDireccion() {
        return direccion;
    }

    public void setDireccion(String direccion) {
        this.direccion = direccion;
    }

    public String getContacto() {
        return contacto;
    }

    public void setContacto(String contacto) {
        this.contacto = contacto;
    }

    public String getObraSocial() {
        return obraSocial;
    }

    public void setObraSocial(String obraSocial) {
        this.obraSocial = obraSocial;
    }

    public String getHistorialClinico() {
        return historialClinico;
    }

    public void setHistorialClinico(String historialClinico) {
        this.historialClinico = historialClinico;
    }

    @Override
    public String toString() {
        // Esto es lo que se mostrará en el JComboBox de Turnos
        return dni + " - " + nombre;
    }
}