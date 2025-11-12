package model;

public class Consultorio {

    private int id;
    private String ubicacion;

    public Consultorio() {
    }

    public Consultorio(int id, String ubicacion) {
        this.id = id;
        this.ubicacion = ubicacion;
    }

    // Getters y Setters
    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getUbicacion() {
        return ubicacion;
    }

    public void setUbicacion(String ubicacion) {
        this.ubicacion = ubicacion;
    }

    @Override
    public String toString() {
        // Esto se mostrará en el JComboBox de Médicos
        return id + " - " + ubicacion;
    }
}
