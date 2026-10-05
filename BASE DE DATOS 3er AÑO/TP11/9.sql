-- ============================================================
-- a. Roles para el esquema recursos_humanos
-- ============================================================

-- i. Rol de solo lectura CREATE ROLE rrhh_lectura NOLOGIN;
GRANT USAGE ON SCHEMA recursos_humanos TO rrhh_lectura;

GRANT
SELECT
    ON ALL TABLES IN SCHEMA recursos_humanos TO rrhh_lectura;
-- ii. Rol de gestión completa
CREATE ROLE rrhh_gestion NOLOGIN;

GRANT USAGE ON SCHEMA recursos_humanos TO rrhh_gestion;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA recursos_humanos TO rrhh_gestion;

-- ============================================================
-- b. Roles para el esquema proyectos
-- ============================================================

-- i. Rol de solo lectura
CREATE ROLE proyectos_lectura NOLOGIN;

GRANT USAGE ON SCHEMA proyectos TO proyectos_lectura;

GRANT SELECT ON ALL TABLES IN SCHEMA proyectos TO proyectos_lectura;
-- ii. Rol de gestión completa
CREATE ROLE proyectos_gestion NOLOGIN;

GRANT USAGE ON SCHEMA proyectos TO proyectos_gestion;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA proyectos TO proyectos_gestion;