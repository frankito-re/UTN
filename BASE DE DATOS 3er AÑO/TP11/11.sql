---------------------------------------------------------------
-- 1. Consultas desde  usuario_rrhh_lectura
---------------------------------------------------------------

-- a. Listar todos los empleados con sus respectivos departamentos y puestos.
SELECT e.empleado_id, e.nombre, e.apellido, d.nombre AS departamento, p.nombre AS puesto
FROM recursos_humanos.empleados e
    JOIN recursos_humanos.departamentos d ON e.departamento_id = d.departamento_id
    JOIN recursos_humanos.puestos p ON e.puesto_id = p.puesto_id;

-- b. Mostrar los nombres de los empleados que trabajan en el departamento de 'Desarrollo'.
SELECT e.nombre, e.apellido
FROM recursos_humanos.empleados e
    JOIN recursos_humanos.departamentos d ON e.departamento_id = d.departamento_id
WHERE
    d.nombre = 'Desarrollo';

-- c. El salario promedio de todos los empleados en el esquema recursos_humanos.
-- Nota: Se vincula la tabla de empleados con puestos para obtener el salario asignado a cada trabajador.
SELECT ROUND(AVG(p.salario), 2) AS salario_promedio
FROM recursos_humanos.empleados e
    JOIN recursos_humanos.puestos p ON e.puesto_id = p.puesto_id;

-- d. Listar todos los departamentos con la cantidad de empleados que tienen.
-- Se utiliza LEFT JOIN para incluir departamentos en caso de que alguno no tenga empleados asignados.
SELECT
    d.nombre AS departamento,
    COUNT(e.empleado_id) AS cantidad_empleados
FROM recursos_humanos.departamentos d
    LEFT JOIN recursos_humanos.empleados e ON d.departamento_id = e.departamento_id
GROUP BY
    d.departamento_id,
    d.nombre
ORDER BY cantidad_empleados DESC;

---------------------------------------------------------------
-- 2. Consultas y Operaciones desde usuario_rrhh_gestion (user_rrhh_gestion)
---------------------------------------------------------------

-- e. Actualizar el salario de todos los 'Desarrolladores Junior' en un 10%.
-- Nota: En el diseño del esquema, los salarios están definidos en la tabla 'puestos'.
UPDATE recursos_humanos.puestos
SET
    salario = salario * 1.10
WHERE
    nombre = 'Desarrollador Junior';

-- f. Crear una nueva tabla 'beneficios' en el esquema recursos_humanos.
CREATE TABLE recursos_humanos.beneficios (
    beneficios_id SERIAL PRIMARY KEY,
    empleado_id INT REFERENCES recursos_humanos.empleados (empleado_id),
    descripcion VARCHAR(255),
    fecha_otorgamiento DATE
);

---------------------------------------------------------------
-- 3. Consultas desde usuario_proyectos_lectura (proyectos_lectura1 / proyectos_lectura2)
---------------------------------------------------------------

-- g. Listar todos los proyectos con sus fechas de inicio y finalización.
SELECT nombre, fecha_inicio, fecha_fin FROM proyectos.proyectos;

-- h. Mostrar los nombres de las tareas asociadas al proyecto 'Sistema de Gestión'.
SELECT t.nombre AS tarea
FROM proyectos.tareas t
    JOIN proyectos.proyectos p ON t.proyecto_id = p.proyecto_id
WHERE
    p.nombre = 'Sistema de Gestión';

-- i. Obtener la cantidad total de tareas en el esquema proyectos.
SELECT COUNT(*) AS total_tareas FROM proyectos.tareas;

-- j. Listar todos los empleados asignados al proyecto 'Expansión de Ventas' con su rol.
SELECT e.nombre, e.apellido, ep.rol
FROM proyectos.empleados_proyectos ep
    JOIN proyectos.proyectos p ON ep.proyecto_id = p.proyecto_id
    JOIN recursos_humanos.empleados e ON ep.empleado_id = e.empleado_id
WHERE
    p.nombre = 'Expansión de Ventas';