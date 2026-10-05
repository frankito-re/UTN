-- Crear usuarios CON LOGIN y asignarles roles. Estos usuarios tendrán capacidad  de iniciar sesión. Asignarles uno o varios de los roles creados anteriormente.

---------------------------------------------------------------
-- a. Usuarios para el esquema recursos_humanos
---------------------------------------------------------------

-- i. Usuarios de solo lectura en recursos_humanos
CREATE USER rrhh_lectura1 WITH LOGIN PASSWORD 'rh1234';

GRANT rrhh_lectura TO rrhh_lectura1;

CREATE USER rrhh_lectura2 WITH LOGIN PASSWORD 'rh1234';

GRANT rrhh_lectura TO rrhh_lectura2;
-- ii. Usuario con permisos de gestión en recursos_humanos
CREATE USER user_rrhh_gestion WITH LOGIN PASSWORD 'grh1234';

GRANT rrhh_gestion TO user_rrhh_gestion;

---------------------------------------------------------------
-- b. Usuarios para el esquema proyectos
---------------------------------------------------------------

-- i. Usuarios de solo lectura en proyectos
CREATE USER proyectos_lectura1 WITH LOGIN PASSWORD 'proyecto1234';

GRANT proyectos_lectura TO proyectos_lectura1;

CREATE USER proyectos_lectura2 WITH LOGIN PASSWORD 'proyecto1234';

GRANT proyectos_lectura TO proyectos_lectura2;
-- ii. Usuario con permisos de gestión en proyectos
CREATE USER user_proyectos_gestion WITH LOGIN PASSWORD 'gestion1234';

GRANT proyectos_gestion TO user_proyectos_gestion;