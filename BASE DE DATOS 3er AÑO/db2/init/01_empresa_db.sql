CREATE SCHEMA IF NOT EXISTS recursos_humanos;
CREATE SCHEMA IF NOT EXISTS proyectos;

-- Tablas para el esquema recursos.humanos

CREATE TABLE recursos_humanos.departamentos (
    departamento_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR(100)
);

CREATE TABLE recursos_humanos.puestos (
    puesto_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    salario NUMERIC(10,2) NOT NULL
);

CREATE TABLE recursos_humanos.empleados (
    empleado_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    departamento_id INT REFERENCES recursos_humanos.departamentos(departamento_id),
    puesto_id INT REFERENCES recursos_humanos.puestos(puesto_id)
);

-- Tablas para el esquema proyectos

CREATE TABLE proyectos.proyectos (
    proyecto_id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE
);

CREATE TABLE proyectos.tareas (
    tarea_id SERIAL PRIMARY KEY,
    proyecto_id INT REFERENCES proyectos.proyectos(proyecto_id),
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE
);

CREATE TABLE proyectos.empleados_proyectos (
    id SERIAL PRIMARY KEY,
    empleado_id INT REFERENCES recursos_humanos.empleados(empleado_id),
    proyecto_id INT REFERENCES proyectos.proyectos(proyecto_id),
    rol VARCHAR(50)
);


-- Esquema recursos_humanos

-- Tabla: departamentos

INSERT INTO recursos_humanos.departamentos (nombre, ubicacion) VALUES
('Recursos Humanos', 'Oficina Principal'),
('Desarrollo', 'Edificio A'),
('Ventas', 'Edificio B'),
('Marketing', 'Oficina Principal');


-- Tabla: puestos

INSERT INTO recursos_humanos.puestos (nombre, salario) VALUES
('Gerente de Recursos Humanos', 1200000.00),
('Desarrollador Senior', 850000.00),
('Vendedor', 480000.00),
('Especialista en Marketing', 650000.00),
('Desarrollador Junior', 600000.00),
('Asistente de Recursos Humanos', 550000.00);


-- Tabla: empleados

INSERT INTO recursos_humanos.empleados (nombre, apellido, departamento_id, puesto_id) VALUES
('Ana', 'García', 1, 1),
('Luis', 'Pérez', 2, 2),
('Marta', 'López', 3, 3),
('Carlos', 'Ramírez', 4, 4),
('Elena', 'Hernández', 2, 5),
('Sofía', 'Martínez', 1, 6);

-- Esquema proyectos

-- Tabla proyectos

INSERT INTO proyectos.proyectos (nombre, descripcion, fecha_inicio, fecha_fin) VALUES
('Sistema de Gestión', 'Desarrollo de un sistema interno de gestión', '2024-01-01', '2024-06-30'),
('Campaña de Marketing', 'Lanzamiento de una nueva campaña de marketing digital', '2024-02-15', '2024-05-15'),
('Expansión de Ventas', 'Proyecto para expandir las ventas a nuevos mercados', '2024-03-01', '2024-09-30');


-- Tabla tareas

INSERT INTO proyectos.tareas (proyecto_id, nombre, descripcion, fecha_inicio, fecha_fin) VALUES
(1, 'Análisis de Requisitos', 'Recopilación y análisis de requisitos para el sistema', '2024-01-01', '2024-01-31'),
(1, 'Desarrollo Backend', 'Desarrollo de la lógica de negocio del sistema', '2024-02-01', '2024-04-30'),
(1, 'Pruebas', 'Realización de pruebas unitarias e integradas', '2024-05-01', '2024-06-15'),
(2, 'Investigación de Mercado', 'Análisis de mercado y tendencias', '2024-02-15', '2024-03-15'),
(2, 'Diseño Creativo', 'Creación de material publicitario', '2024-03-16', '2024-04-15'),
(2, 'Lanzamiento de la Campaña', 'Publicación y distribución de la campaña', '2024-04-16', '2024-05-15'),
(3, 'Investigación de Nuevos Mercados', 'Identificación de mercados potenciales', '2024-03-01', '2024-04-30'),
(3, 'Desarrollo de Estrategia de Ventas', 'Planificación de estrategias para nuevos mercados', '2024-05-01', '2024-07-31'),
(3, 'Implementación de Estrategias', 'Ejecución de estrategias de ventas', '2024-08-01', '2024-09-30');


-- Tabla empleados_proyectos

INSERT INTO proyectos.empleados_proyectos (empleado_id, proyecto_id, rol) VALUES
(2, 1, 'Desarrollador Principal'),
(5, 1, 'Desarrollador Junior'),
(4, 2, 'Especialista en Marketing'),
(3, 3, 'Vendedor Senior'),
(1, 3, 'Coordinador de Recursos Humanos');
