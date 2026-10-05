-- Configurar privilegios por defecto para futuras tablas de manera que el  usuario admin_empresa  herede los privilegios anteriores para poder acceder a cualquier  tabla que se cree posteriormente.
ALTER DEFAULT PRIVILEGES IN SCHEMA recursos_humanos,
proyectos
GRANT ALL PRIVILEGES ON TABLES TO admin_empresa;