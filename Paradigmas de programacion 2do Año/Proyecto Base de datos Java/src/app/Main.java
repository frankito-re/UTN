package app;

import java.sql.Date;
import java.sql.Time;
import java.util.List;
import java.util.Scanner;

import model.Medico;
import model.Paciente;
import model.Turno;
import service.MedicoService;
import service.PacienteService;
import service.TurnoService;
import util.JdbcUtil;

/**
 * Aplicación de consola para gestionar el Centro de Salud.
 * Este es el "Mesero" o "Interfaz de Usuario".
 */
public class Main {

    // Servicios (Los "Gerentes")
    private static final PacienteService pacienteService = new PacienteService();
    private static final MedicoService medicoService = new MedicoService();
    private static final TurnoService turnoService = new TurnoService();

    private static final Scanner scanner = new Scanner(System.in);

    public static void main(String[] args) {
        // Inicializar la conexión
        try (scanner) {
            // Inicializar la conexión
            JdbcUtil.getConnection();

            System.out.println("--- BIENVENIDO AL SISTEMA DE GESTIÓN DE TURNOS ---");

            int opcion = -1;
            while (opcion != 0) {
                mostrarMenuPrincipal();
                try {
                    // Manejo de línea vacía
                    String input = scanner.nextLine();
                    if (input.trim().isEmpty()) {
                        System.out.println("Por favor, ingrese una opción.");
                        continue;
                    }
                    opcion = Integer.parseInt(input);

                    switch (opcion) {
                        case 1 -> gestionarPacientes();
                        case 2 -> gestionarMedicos();
                        case 3 -> gestionarTurnos();
                        case 0 -> System.out.println("Saliendo del sistema...");
                        default -> System.out.println("Opción no válida.");
                    }
                } catch (NumberFormatException e) {
                    System.out.println("Error: Ingrese solo números.");
                }
            }

            // Cerrar conexión al salir
            JdbcUtil.closeConnection();
        }
    }

    private static void mostrarMenuPrincipal() {
        System.out.println("\n--- MENÚ PRINCIPAL ---");
        System.out.println("1. Gestionar Pacientes");
        System.out.println("2. Gestionar Médicos");
        System.out.println("3. Gestionar Turnos");
        System.out.println("0. Salir");
        System.out.print("Seleccione una opción: ");
    }

    // --- GESTIÓN DE PACIENTES (CRUD) ---
    private static void gestionarPacientes() {
        System.out.println("\n--- GESTIÓN DE PACIENTES ---");
        System.out.println("1. Registrar nuevo paciente");
        System.out.println("2. Listar todos los pacientes");
        System.out.print("Seleccione: ");
        int opcion = Integer.parseInt(scanner.nextLine());

        try {
            if (opcion == 1) {
                System.out.print("DNI: ");
                int dni = Integer.parseInt(scanner.nextLine());
                System.out.print("Nombre: ");
                String nombre = scanner.nextLine();
                System.out.print("Dirección: ");
                String dir = scanner.nextLine();
                System.out.print("Contacto: ");
                String cont = scanner.nextLine();
                System.out.print("Obra Social: ");
                String os = scanner.nextLine();
                Paciente p = new Paciente(dni, nombre, dir, cont, os, "");
                pacienteService.registrarPaciente(p);
                System.out.println("Paciente registrado con éxito.");
            } else if (opcion == 2) {
                List<Paciente> pacientes = pacienteService.listarPacientes();
                pacientes.forEach(System.out::println);
            }
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        }
    }

    // --- GESTIÓN DE MÉDICOS (CRUD) ---
    private static void gestionarMedicos() {
        System.out.println("\n--- GESTIÓN DE MÉDICOS ---");
        System.out.println("1. Registrar nuevo médico");
        System.out.println("2. Listar todos los médicos");
        System.out.print("Seleccione: ");
        int opcion = Integer.parseInt(scanner.nextLine());

        try {
            if (opcion == 1) {
                System.out.print("Matrícula: ");
                int mat = Integer.parseInt(scanner.nextLine());
                System.out.print("Nombre: ");
                String nombre = scanner.nextLine();

                System.out.println("Especialidades disponibles:");
                medicoService.listarEspecialidades().forEach(System.out::println);
                System.out.print("ID Especialidad: ");
                int espId = Integer.parseInt(scanner.nextLine());

                System.out.println("Consultorios disponibles:");
                medicoService.listarConsultorios().forEach(System.out::println);
                System.out.print("ID Consultorio: ");
                int conId = Integer.parseInt(scanner.nextLine());

                Medico m = new Medico(mat, nombre, espId, conId);
                medicoService.registrarMedico(m);
                System.out.println("Médico registrado con éxito.");

            } else if (opcion == 2) {
                List<Medico> medicos = medicoService.listarMedicos();
                medicos.forEach(System.out::println);
            }
        } catch (Exception e) {
            System.err.println("Error: " + e.getMessage());
        }
    }

    // --- GESTIÓN DE TURNOS (LÓGICA PRINCIPAL) ---
    private static void gestionarTurnos() {
        System.out.println("\n--- GESTIÓN DE TURNOS ---");
        System.out.println("1. Asignar nuevo turno");
        System.out.println("2. Listar todos los turnos");
        System.out.println("3. Cancelar turno");
        System.out.print("Seleccione: ");
        int opcion = Integer.parseInt(scanner.nextLine());

        try {
            switch (opcion) {
                case 1 -> {
                    System.out.println("--- Asignar Turno ---");
                    System.out.print("DNI del Paciente: ");
                    int dni = Integer.parseInt(scanner.nextLine());
                    System.out.println("Médicos disponibles:");
                    medicoService.listarMedicos().forEach(System.out::println);
                    System.out.print("Matrícula del Médico: ");
                    int mat = Integer.parseInt(scanner.nextLine());
                    System.out.print("Fecha (Formato AAAA-MM-DD): ");
                    Date fecha = Date.valueOf(scanner.nextLine());
                    System.out.print("Hora (Formato HH:MM:SS): ");
                    Time hora = Time.valueOf(scanner.nextLine());
                    Turno t = new Turno(fecha, hora, dni, mat, 0); // 0 temporal
                    turnoService.asignarTurno(t);
                    System.out.println("¡Turno asignado con éxito!");
                }
                case 2 -> {
                    List<Turno> turnos = turnoService.listarTurnos();
                    if (turnos.isEmpty())
                        System.out.println("No hay turnos registrados.");
                    turnos.forEach(System.out::println);
                }
                case 3 -> {
                    System.out.print("ID del turno a cancelar: ");
                    int idTurno = Integer.parseInt(scanner.nextLine());
                    turnoService.cancelarTurno(idTurno);
                    System.out.println("Turno cancelado.");
                }
                default -> {
                }
            }
        } catch (Exception e) {
            System.err.println("Error al gestionar turno: " + e.getMessage());
        }
    }
}